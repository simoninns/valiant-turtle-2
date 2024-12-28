#************************************************************************ 
#
#   ble_peripheral.py
#
#   BLE Peripheral Role
#   Valiant Turtle 2 - Robot firmware
#   Copyright (C) 2024 Simon Inns
#
#   This file is part of Valiant Turtle 2
#
#   This is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Email: simon.inns@gmail.com
#
#************************************************************************

import aioble.device
import picolog
import aioble
import bluetooth
import asyncio
import struct

from machine import unique_id
from micropython import const

class BlePeripheral:
    __MANUFACTURER_DATA = (0xFFE1, b"www.waitingforfriday.com")
    __ADVERTISING_NAME = "vt2-robot"

    def __init__(self):
        # Get the local device's Unique ID (used as the serial number)
        self._uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Advertising flag
        self._is_advertising = True

        # Flag to show connected status
        self._connected = False

        # Advertising definitions
        self.__ble_advertising_definitions()

        # Service definitions
        self.__ble_service_definitions()

        # Register services with aioBLE library
        aioble.register_services(self.command_service)

        # Maximum number of elements to store in the queues (note: maximum is 128 since command sequence is 8 bits)
        # Note: Queue elements are 20 bytes long
        self._max_queue_elements = 50

        # Reception queue for received service data from central
        self._c2p_queue = []
        self._c2p_queue_event = asyncio.Event()

        # Transmission queue for sending service data to central
        self._p2c_queue = []

    @property
    def is_connected(self):
        return self._connected
    
    @property
    def c2p_queue(self):
        return self._c2p_queue
    
    def add_to_p2c_queue(self, data):
        if len(self._p2c_queue) < self._max_queue_elements:
            self._p2c_queue.append(data)
        else:
            picolog.debug("BlePeripheral::add_to_p2c_queue - P2C queue is full - data not added")

    def __ble_advertising_definitions(self):
        # Definitions used for advertising via BLE

        # Set our advertising UUID
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910)

        # Set our appearance to "Remote Control"
        self.peripheral_appearance_generic_remote_control = const(0x0180)
        self.peripheral_manufacturer = BlePeripheral.__MANUFACTURER_DATA
        self.peripheral_advertising_name = BlePeripheral.__ADVERTISING_NAME

    def __ble_service_definitions(self):
        # Create a service and attach characteristics to it
        service_uuid = bluetooth.UUID(0xFA20) # Custom
        tx_p2c_characteristic_uuid = bluetooth.UUID(0xFBA0) # Custom
        rx_c2p_characteristic_uuid = bluetooth.UUID(0xFBA1) # Custom

        self.command_service = aioble.Service(service_uuid)

        # TX: Peripheral -> Central (maximum supported length by BLE is 20 bytes)
        self.tx_p2c_characteristic = aioble.BufferedCharacteristic(self.command_service, tx_p2c_characteristic_uuid, notify=True, max_len=20)
        # RX: Central -> Peripheral
        self.rx_c2p_characteristic = aioble.Characteristic(self.command_service, rx_c2p_characteristic_uuid, write=True, write_no_response=True, capture=True)

    async def run(self):
        picolog.debug("BlePeripheral::run - Running")

        tasks = [
            asyncio.create_task(self.__maintain_connection()),
            asyncio.create_task(self.__handle_commands()),
        ]
        await asyncio.gather(*tasks)

    async def __maintain_connection(self):
        picolog.debug("BlePeripheral::__maintain_connection - running")
        while True:
            # If we are not connected, clear the queues then advertise and wait for connection
            if self._is_advertising:
                # Clear the queues
                self._c2p_queue.clear()
                self._p2c_queue.clear()

                # BLE Advertising frequency
                ble_advertising_frequency_us = const(250000)

                # Wait for something to connect
                picolog.debug("BlePeripheral::__maintain_connection - Advertising and waiting for connection from central...")
                self._ble_connection = await aioble.advertise(
                    ble_advertising_frequency_us,
                    name=self.peripheral_advertising_name,
                    services=[self.peripheral_advertising_uuid],
                    appearance=self.peripheral_appearance_generic_remote_control,
                    manufacturer=self.peripheral_manufacturer,
                )
                picolog.info(f"BlePeripheral::__maintain_connection - Central with address {self._ble_connection.device.addr_hex()} has connected - advertising stopped")
                self._is_advertising = False
                self._connected = True
            else:
                # If we are connected, wait for disconnection
                await asyncio.sleep(0.25)

    async def send_data_p2c(self, p2c_data_packet: bytearray):
        try:
            if p2c_data_packet is not None:
                self.tx_p2c_characteristic.notify(self._ble_connection, p2c_data_packet)
            else:
                TypeError("BlePeripheral::send_data_p2c - p2c_data_packet is None")
        except Exception as e:
            picolog.error(f"BlePeripheral::send_data_p2c - Exception {e}")
            RuntimeError(f"BlePeripheral::send_data_p2c - Exception {e}")

    async def get_data_c2p(self, characteristic, timeout_ms=2000):
        try:
            _, c2p_data_packet = await characteristic.written(timeout_ms=timeout_ms)
            return c2p_data_packet
        except asyncio.TimeoutError:
            picolog.debug(f"BlePeripheral::get_data_c2p - Timed-out")
            return None

    # Note: We use an atomic exchange of data with the central to ensure that the data is received and processed
    # as, after the initial connection, the central can sometimes miss data packets
    async def exchange_data(self, p2c_data_packet) -> tuple[bytearray, bool]:
        for attempt in range(1, 4):
            await self.send_data_p2c(p2c_data_packet)
            c2p_data_packet = await self.get_data_c2p(self.rx_c2p_characteristic)
            if c2p_data_packet is not None:
                return c2p_data_packet, True
            picolog.debug(f"BlePeripheral::exchange_data - No response from central after attempt {attempt}")

        picolog.error("BlePeripheral::exchange_data - All 3 attempts failed")
        return bytearray(20), False

    async def __poll_central(self):
        # If a response is available, send it to central, otherwise send a NOP
        p2c_data_packet = bytearray(20)
        if len(self._p2c_queue) > 0:
            p2c_data_packet = self._p2c_queue.pop(0)

            # Just temporarily log the sequence number for testing
            p2c_sequence = struct.unpack("<B", p2c_data_packet[0:1])[0]
            picolog.debug(f"BlePeripheral::__poll_central - Sending data to central with sequence = {p2c_sequence}")

        # Exchange data with central
        success = False
        c2p_data_packet, success = await self.exchange_data(p2c_data_packet)

        if success:
            # If we have received data from central, add it to the queue
            if c2p_data_packet is not None:
                # Only add data to the queue if the first byte is not 0 (NOP)
                if c2p_data_packet[0] != 0:
                    if len(self._c2p_queue) < self._max_queue_elements:
                        self._c2p_queue.append(c2p_data_packet)
                        self._c2p_queue_event.set()
                    else:
                        picolog.debug("BlePeripheral::__poll_central - c2p queue is full - data not added")
            else:
                self._connected = False
                self._is_advertising = True
                picolog.info("BlePeripheral::__poll_central - Empty response from central... Flagged as disconnected")
        else:
            self._connected = False
            self._is_advertising = True
            picolog.info("BlePeripheral::__poll_central - No response from central... Flagged as disconnected")

    async def __handle_commands(self):
        picolog.debug("BlePeripheral::__handle_commands - running")
        while True:
            # If we are connected, poll central for data
            if self._connected:
                await self.__poll_central()

                # Limit polling to a maximum of 5 times per second
                await asyncio.sleep(0.2)
            else:
                # Disconnected - Wait before checking again
                await asyncio.sleep(0.5)

if __name__ == "__main__":
    from main import main
    main()