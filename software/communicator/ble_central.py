#************************************************************************ 
#
#   ble_central.py
#
#   BLE Central role (aioBLE library)
#   Valiant Turtle 2 - Communicator firmware
#   Copyright (C) 2025 Simon Inns
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

import asyncio
import picolog

from aioble import scan
import bluetooth

class BleCentral:
    __ADVERTISING_NAME = "vt2-robot"
    __ADVERTISING_UUID = 0xF910

    def __init__(self):
        # Remote device advertising definitions
        self._peripheral_advertising_uuid = bluetooth.UUID(BleCentral.__ADVERTISING_UUID)
        self._peripheral_advertising_name = BleCentral.__ADVERTISING_NAME

        # Command service characteristics setup
        self._tx_p2c_characteristic_uuid = bluetooth.UUID(0xFBA0)
        self._rx_c2p_characteristic_uuid = bluetooth.UUID(0xFBA1)

        # Flag to show connected status
        self._discovered = False
        self._connected = False

        # Maximum number of elements to store in the queues (note: maximum is 128 since command sequence is 8 bits)
        # Note: Queue elements are 20 bytes long
        self._max_queue_elements = 50

        # Transmission queue for sending service data from central
        self._c2p_queue = []

        # Reception queue for receiving service data to central
        self._p2c_queue = []

        # Events to signal queue and notification events
        self._p2c_queue_event = asyncio.Event()
        self._p2c_notification_event = asyncio.Event()

        # Tx/Rx characteristic objects
        self._tx_p2c_characteristic = None
        self._rx_c2p_characteristic = None

    @property
    def connected(self):
        return self._connected
    
    @property
    def p2c_queue(self):
        return self._c2p_queue
    
    def add_to_c2p_queue(self, data):
        if len(self._c2p_queue) < self._max_queue_elements:
            self._c2p_queue.append(data)
        else:
            picolog.info("BleCentral::add_to_c2p_queue - C2P queue is full - data not added")

    def disconnect(self):
        picolog.info("BleCentral::disconnect - Disconnecting from BLE peripheral")
        self._connected = False
        self._discovered = False

    async def run(self):
        picolog.info("BleCentral::run - Running BLE central async tasks") 

        tasks = [
            asyncio.create_task(self.__maintain_connection()),
            asyncio.create_task(self.__handle_commands()),
        ]
        await asyncio.gather(*tasks)

    async def __scan_for_peripheral(self):
        async with scan(duration_ms = 5000, interval_us = 30000, window_us = 30000, active = True) as scanner:
            async for result in scanner:
                # See if it matches our name
                if result.name() == self._peripheral_advertising_name:
                    picolog.debug(f"BleCentral::__scan_for_peripheral - Found peripheral with matching advertising name of {self._peripheral_advertising_name}")
                    if self._peripheral_advertising_uuid in result.services():
                        picolog.debug("BleCentral::__scan_for_peripheral - Peripheral advertises expected service UUID")
                        return result.device
        # Nothing found after specified scanning duration
        return None 

    async def __on_discovery(self):
        picolog.debug("BleCentral::__on_connected - Connected to peripheral")

        # Command service setup
        command_service_uuid = bluetooth.UUID(0xFA20)

        try:
            command_service = await self._connection.service(command_service_uuid)
            if command_service == None:
                picolog.debug("BleCentral::__on_connected - FATAL: Peripheral command_service is missing!")
                self._discovered = False
                self._connected = False
                return
            
        except asyncio.TimeoutError:
            picolog.debug("BleCentral::__on_connected - FATAL: Timeout discovering services/characteristics")
            self._discovered = False
            self._connected = False
            return

        # Command service characteristics setup
        tx_p2c_characteristic_uuid = bluetooth.UUID(0xFBA0) # Custom
        rx_c2p_characteristic_uuid = bluetooth.UUID(0xFBA1) # Custom
        try:
            self._tx_p2c_characteristic = await command_service.characteristic(tx_p2c_characteristic_uuid)
            
            if self._tx_p2c_characteristic == None:
                picolog.debug("BleCentral::__on_connected - FATAL: Peripheral command_service tx_p2c_characteristic missing!")
                self._discovered = False
                self._connected = False
                return

        except asyncio.TimeoutError:
            picolog.debug("BleCentral::__on_connected - FATAL: Timeout discovering characteristics")
            self._discovered = False
            self._connected = False
            return

        try:
            self._rx_c2p_characteristic = await command_service.characteristic(rx_c2p_characteristic_uuid)
            
            if self._rx_c2p_characteristic == None:
                picolog.debug("BleCentral::__on_connected - FATAL: Peripheral command_service rx_c2p_characteristic missing!")
                self._discovered = False
                self._connected = False
                return

        except asyncio.TimeoutError:
            picolog.debug("BleCentral::__on_connected - FATAL: Timeout discovering characteristics")
            self._discovered = False
            self._connected = False
            return

        # Subscribe to characteristic notifications
        await self._tx_p2c_characteristic.subscribe(notify = True)
        self._connected = True

    async def __maintain_connection(self):
        picolog.info("BleCentral::__maintain_connection - Running maintain connection task")
        while True:
            # If we are not connected, advertise and wait for connection
            if not self._connected:
                # Clear the queues
                self._c2p_queue.clear()
                self._p2c_queue.clear()

                # Scan for the peripheral
                picolog.info("BleCentral::__maintain_connection - Scanning for BLE peripheral...")

                device = await self.__scan_for_peripheral()
                if not device:
                    picolog.debug("BleCentral::__maintain_connection - Peripheral not found")
                else:
                    try:
                        picolog.debug(f"BleCentral::__maintain_connection - Peripheral with address {device.addr_hex()} discovered.  Attempting to connect")
                        self._connection = await device.connect()
                        picolog.info(f"BleCentral::__maintain_connection - Connected to peripheral with address {device.addr_hex()}")
                        self._discovered = True

                        # Perform any connection setup
                        await self.__on_discovery()
                        
                    except asyncio.TimeoutError:
                        picolog.debug("BleCentral::__maintain_connection - Connection attempt timed out!")
                        self._discovered = False
                        self._connected = False

                # Wait for 1 second before checking again
                await asyncio.sleep(1)
            else:
                # Wait for disconnection
                await asyncio.sleep(1)

    async def __handle_commands(self):
        picolog.info("BleCentral::__handle_commands - Running handle commands task")
        while True:
            while self._connected:
                # Wait for a notification to be received
                # Note: With BLEak, the notification triggers an interrupt, but with aioBLE we have to
                # await the notification
                try:
                    service_data = await self._tx_p2c_characteristic.notified()
                except Exception:
                    picolog.info("BleCentral::__handle_commands - Device disconnected")
                    self.disconnect()

                if self._connected:
                    if len(service_data) == 20:
                        # Check the first byte to see if it is a valid commmand response
                        # If the first byte is 0x00, then it is a NOP response
                        if service_data[0] != 0x00:
                            # Queue the data packet for processing
                            if len(self._p2c_queue) < self._max_queue_elements:
                                self._p2c_queue.append(service_data)
                                #picolog.info(f"Received data from peripheral: {service_data}, appended to queue ({len(self._p2c_queue)} elements)")
                                self._p2c_queue_event.set()
                    else:
                        picolog.info(f"BleCentral::__handle_commands - Received data from peripheral: {service_data} - invalid length")

                    # Notify the main async task that data has been received
                    self._p2c_notification_event.set()
    
                    # Send any data in the c2p queue to the peripheral
                    if len(self._c2p_queue) > 0:
                        # Send all waiting data
                        while len(self._c2p_queue) > 0:
                            data_packet = self._c2p_queue.pop(0)
                            #picolog.info(f"Sending data to peripheral: {data_packet}")
                            await self._rx_c2p_characteristic.write(data_packet)
                    else:
                        # If the queue is empty, send a nop
                        data_packet = bytearray(20)
                        await self._rx_c2p_characteristic.write(data_packet)

                    # Clear the notification event
                    self._p2c_notification_event.clear()
            else:
                # If we are not connected, wait for 250ms
                await asyncio.sleep(0.25)

if __name__ == "__main__":
    from main import main
    main()