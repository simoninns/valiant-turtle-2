#************************************************************************ 
#
#   ble_central.py
#
#   BLE Central role (BLEak library)
#   Valiant Turtle 2 - Communicator firmware
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

import asyncio
import logging

from bleak import BleakScanner, BleakClient
from bleak.uuids import normalize_uuid_16
from bleak.backends.characteristic import BleakGATTCharacteristic

class BleCentral:
    __ADVERTISING_NAME = "vt2-robot"
    __ADVERTISING_UUID = 0xF910

    def __init__(self):
        # Remote device advertising definitions
        self._peripheral_advertising_uuid = BleCentral.__ADVERTISING_UUID
        self._peripheral_advertising_name = BleCentral.__ADVERTISING_NAME

        # Command service characteristics setup
        self._tx_p2c_characteristic_uuid = normalize_uuid_16(0xFBA0)
        self._rx_c2p_characteristic_uuid = normalize_uuid_16(0xFBA1)

        # Flag to show connected status
        self._connected = False

        # Maximum number of elements to store in the queues (note: maximum is 128 since command sequence is 8 bits)
        # Note: Queue elements are 20 bytes long
        self._max_queue_elements = 50

        # Transmission queue for sending service data from central
        self._c2p_queue = []

        # Reception queue for receiving service data to central
        self._p2c_queue = []
        self._p2c_queue_event = None

        # Notification event for when data is received from the peripheral
        self._p2c_notification_event = None

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
            logging.info("C2P queue is full - data not added")

    def disconnect(self):
        logging.info("Disconnecting from BLE peripheral")
        self._connected = False

    async def run(self):
        logging.info("Running BLE central async tasks") 

        self._p2c_queue_event = asyncio.Event()
        self._p2c_notification_event = asyncio.Event()

        tasks = [
            asyncio.create_task(self.__maintain_connection()),
            asyncio.create_task(self.__handle_commands()),
        ]
        await asyncio.gather(*tasks)

    async def __maintain_connection(self):
        logging.info("Running maintain connection task")
        while True:
            # If we are not connected, advertise and wait for connection
            if not self._connected:
                # Clear the queues
                self._c2p_queue.clear()
                self._p2c_queue.clear()

                # Scan for the peripheral
                logging.info("Scanning for BLE peripheral...")
                scanner = BleakScanner()
                self._device = await scanner.find_device_by_name(self._peripheral_advertising_name, timeout=5, return_adv=True)
                if self._device:
                    logging.info(f"BLE peripheral found with address {self._device.address}")

                    # Attempt to connect to the peripheral
                    try:
                        async with BleakClient(self._device.address) as self._client:
                            if self._client.is_connected:
                                # We should probably pair here... but bleak doesn't support programmatic pairing

                                # Subscribe to notifications on the tx_p2c_characteristic
                                await self._client.start_notify(self._tx_p2c_characteristic_uuid, self.__p2c_notification_handler)
                                logging.info("Subscribed to P2C notifications")
                                self._connected = True

                                # Wait for disconnection
                                while self._client.is_connected and self._connected:
                                    await asyncio.sleep(0.25)
                    except BleakError as e:
                        logging.error(f"Failed to connect or discover services: {e}")
                        await asyncio.sleep(1)  # Wait before retrying
                else:
                    logging.info("BLE peripheral not found")
                    self._connected = False

            # Wait for 1 second before checking again
            await asyncio.sleep(1)

    async def __handle_commands(self):
        logging.info("Running handle commands task")
        while True:
            while self._connected:
                # Wait for a notification to be received
                #logging.info("Waiting for P2C notification event")
                await self._p2c_notification_event.wait()
                #logging.info("P2C notification event received")
    
                # Send any data in the c2p queue to the peripheral
                if len(self._c2p_queue) > 0:
                    # Send all waiting data
                    while len(self._c2p_queue) > 0:
                        data_packet = self._c2p_queue.pop(0)
                        #logging.info(f"Sending data to peripheral: {data_packet}")
                        await self._client.write_gatt_char(self._rx_c2p_characteristic_uuid, data_packet, response=False)
                else:
                    # If the queue is empty, send a nop
                    data_packet = bytearray(20)
                    await self._client.write_gatt_char(self._rx_c2p_characteristic_uuid, data_packet, response=False)

                # Clear the notification event
                self._p2c_notification_event.clear()
            else:
                # If we are not connected, wait for 250ms
                await asyncio.sleep(0.25)

    def __p2c_notification_handler(self, characteristic: BleakGATTCharacteristic, service_data: bytearray):
        """Handle notifications from the peripheral."""
        if len(service_data) == 20:
            # Check the first byte to see if it is a valid commmand response
            # If the first byte is 0x00, then it is a NOP response
            if service_data[0] != 0x00:
                # Queue the data packet for processing
                if len(self._p2c_queue) < self._max_queue_elements:
                    self._p2c_queue.append(service_data)
                    #logging.info(f"Received data from peripheral: {service_data}, appended to queue ({len(self._p2c_queue)} elements)")
                    self._p2c_queue_event.set()
        else:
            logging.info(f"Received data from peripheral: {service_data} - invalid length")

        # Notify the main async task that data has been received
        self._p2c_notification_event.set()

if __name__ == "__main__":
    from vt2_cmdtest import main
    main()