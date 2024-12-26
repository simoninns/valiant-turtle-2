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

import picolog
import aioble
import bluetooth
import asyncio

from machine import unique_id
from micropython import const

class BlePeripheral:
    __MANUFACTURER_DATA = (0xFFE1, b"www.waitingforfriday.com")
    __ADVERTISING_NAME = "vt2-robot"

    def __init__(self):
        # Get the local device's Unique ID (used as the serial number)
        self._uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

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
            picolog.debug("BlePeripheral::add_to_p2c_queue - Queue is full - data not added")

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
            if not self._connected:
                # Clear the queues
                self._c2p_queue.clear()
                self._p2c_queue.clear()

                # BLE Advertising frequency
                ble_advertising_frequency_us = const(250000)

                # Wait for something to connect
                picolog.debug("BlePeripheral::__maintain_connection - Advertising and waiting for connection from central...")
                self.__connection = await aioble.advertise(
                    ble_advertising_frequency_us,
                    name=self.peripheral_advertising_name,
                    services=[self.peripheral_advertising_uuid],
                    appearance=self.peripheral_appearance_generic_remote_control,
                    manufacturer=self.peripheral_manufacturer,
                )
                picolog.info(f"BlePeripheral::__maintain_connection - Central with address {self.__connection.device.addr_hex()} has connected - advertising stopped")
            else:
                # If we are connected, wait for disconnection
                asyncio.sleep_ms(250)

    async def __wait_for_data(self, characteristic, t_ms=5000):
        try:
            _, data = await characteristic.written(timeout_ms=t_ms)
            return data
        except asyncio.TimeoutError:
            picolog.debug("BlePeripheral::wait_for_data - Data timed-out - (Central probably disappeared)")
            self.__connected = False
            return None

    async def __handle_commands(self):
        picolog.debug("BlePeripheral::__handle_commands - running")
        while True:
            # If we are connected, poll central for data
            if self._connected:
                # Send a command service update (which causes central to reply)
                try:
                    # Check the p2c queue and send any data to central (send blank data if no data)
                    if len(self._p2c_queue) == 0:
                        data_packet = bytearray(20)
                        self.tx_p2c_characteristic.notify(self.__connection, data_packet)
                    else:
                        data_packet = self._p2c_queue.pop(0)
                        self.tx_p2c_characteristic.notify(self.__connection, data_packet)
                        
                except Exception as e:
                    picolog.debug("BlePeripheral::__handle_commands - Exception was flagged (Central has probably disappeared)")
                    self.__connected = False

                # Since disconnection is asynchronous, we need to check if we are still connected
                if self.__connected:
                    # Wait for poll response from central
                    service_data = await self.__wait_for_data(self.rx_c2p_characteristic)
                    if service_data != None:
                        # Check the length of the data packet - if it is not 20 bytes, then it is a nop command
                        if len(service_data) == 20:
                            # Queue the data packet for processing
                            if len(self._c2p_queue) < self._max_queue_elements:
                                self._c2p_queue.append(service_data)
                                self._c2p_queue_event.set()
                            else:
                                picolog.debug("BlePeripheral::__handle_commands - c2p queue is full - data not added")

                # Poll central 5 times a second
                if self.__connected: await asyncio.sleep_ms(200)
            
            # If we are not connected, wait for 250ms
            asyncio.sleep_ms(250)

if __name__ == "__main__":
    from main import main
    main()