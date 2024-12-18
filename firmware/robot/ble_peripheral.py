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

import library.picolog as picolog

from machine import Pin, unique_id
from micropython import const

import aioble
import bluetooth
import asyncio
import struct
from library.robot_comms import RobotCommand

class BlePeripheral:
    __MANUFACTURER_DATA = (0xFFE1, b"www.waitingforfriday.com")
    __CONNECTION_CONFIRMATION_CODE = 12345
    __ADVERTISING_NAME = "vt2-robot"

    __DEBUG_LOG_POWER = False # Set to True to log power service data notifications

    def __init__(self):
        # Get the local device's Unique ID (used as the serial number)
        self.__uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Connection to central
        self.__connection = None

        # Flag to show connected status
        self.__connected = False

        # Advertising definitions
        self.__ble_advertising_definitions()

        # Service definitions
        self.__ble_service_command_definitions()

        # Register services with aioBLE library
        aioble.register_services(self.command_service)

        # Command queue for received commands from central
        self._command_queue = []
        self._command_queue_event = asyncio.Event()
        self._last_processed_command_uid = 0
        self._last_processed_command_response = 0

    @property
    def command_queue_event(self):
        """Get the command queue event"""
        return self._command_queue_event
    
    @property
    def command_queue(self):
        """Get the command queue"""
        return self._command_queue

    @property
    def last_processed_command_uid(self):
        """Get the last processed command UID"""
        return self._last_processed_command_uid
    
    @last_processed_command_uid.setter
    def last_processed_command_uid(self, uid: int):
        """Set the last processed command UID"""
        self._last_processed_command_uid = uid

    @property
    def last_processed_command_response(self):
        """Get the last processed command response"""
        return self._last_processed_command_response
    
    @last_processed_command_response.setter
    def last_processed_command_response(self, response: int):
        """Set the last processed command response"""
        self._last_processed_command_response = response

    def __ble_advertising_definitions(self):
        # Definitions used for advertising via BLE

        # Set our advertising UUID
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910)

        # Set our appearance to "Remote Control"
        self.peripheral_appearance_generic_remote_control = const(0x0180)
        self.peripheral_manufacturer = BlePeripheral.__MANUFACTURER_DATA
        self.peripheral_advertising_name = BlePeripheral.__ADVERTISING_NAME

    # Define a service - command
    def __ble_service_command_definitions(self):
        # Create a command service and attach a button characteristic to it
        command_service_uuid = bluetooth.UUID(0xFA20) # Custom
        tx_p2c_characteristic_uuid = bluetooth.UUID(0xFBA0) # Custom
        rx_c2p_characteristic_uuid = bluetooth.UUID(0xFBA1) # Custom

        self.command_service = aioble.Service(command_service_uuid)

        # TX: Peripheral -> Central
        self.tx_p2c_characteristic = aioble.BufferedCharacteristic(self.command_service, tx_p2c_characteristic_uuid, notify=True, max_len=RobotCommand.byte_length())
        # RX: Central -> Peripheral
        self.rx_c2p_characteristic = aioble.Characteristic(self.command_service, rx_c2p_characteristic_uuid, write=True, write_no_response=True, capture=True)

    # Property that is true when central (VT2 Communicator) is connected
    @property
    def is_central_connected(self) -> bool:
        return self.__connected

    async def wait_for_data(self, characteristic, t_ms=5000):
        try:
            _, data = await characteristic.written(timeout_ms=t_ms)
            return data
        except asyncio.TimeoutError:
            picolog.debug("BlePeripheral::wait_for_data - Data timed-out - (Central probably disappeared)")
            self.__connected = False
            return None
    
    # Send command service characteristics update
    def command_service_update(self):
        if self.__connected and self.__connection:
            # try:
            # Send from p2c - int16_t last processed command response and uint16_t last processed command UID
            self.tx_p2c_characteristic.notify(self.__connection, struct.pack("<hH", self._last_processed_command_response, self._last_processed_command_uid))
                
            # except Exception as e:
            #     picolog.debug("BlePeripheral::command_service_update - Exception was flagged (Central probably disappeared)")
            #     self.__connected = False

    # Advertise peripheral to central
    async def advertise_to_central(self):
        # BLE Advertising frequency
        ble_advertising_frequency_us = const(250000)

        # Wait for something to connect
        picolog.debug("BlePeripheral::advertise_to_central - Advertising and waiting for connection from central...")
        self.__connection = await aioble.advertise(
            ble_advertising_frequency_us,
            name=self.peripheral_advertising_name,
            services=[self.peripheral_advertising_uuid],
            appearance=self.peripheral_appearance_generic_remote_control,
            manufacturer=self.peripheral_manufacturer,
        )
        picolog.info(f"BlePeripheral::advertise_to_central - Central with address {self.__connection.device.addr_hex()} has connected - advertising stopped")

        # It takes a while for the central to really connect.  So, to avoid data dropping into a black hole
        # the central will start by sending us a byte of data.  Once received, we can mark it as connected for real
        picolog.debug("BlePeripheral::advertise_to_central - Waiting for central to confirm connection...")
        reply_data = await self.wait_for_data(self.rx_c2p_characteristic)
        if reply_data != None:
            # Get the 32-bit unsigned integer from the reply data and check it
            if struct.unpack("<L", reply_data)[0] == BlePeripheral.__CONNECTION_CONFIRMATION_CODE:
                picolog.debug("BlePeripheral::advertise_to_central - Central has confirmed as connected")
                self.__connected = True
            else:
                picolog.debug("BlePeripheral::advertise_to_central - Central did not respond with 12345 - Reverting to disconnected state")
                self.__connected = False
        else:
            picolog.debug("BlePeripheral::advertise_to_central - Central did not respond - Reverting to disconnected state")
            self.__connected = False

    # Task to run whilst connected to central
    async def connected_to_central(self):
        while self.__connected:
            # Send a command service update (which causes central to reply)
            self.command_service_update()

            # Command service update timeout can cause disconnection - only wait for reply if still connected...
            if self.__connected:
                # Receive from c2p
                command_data = await self.wait_for_data(self.rx_c2p_characteristic)
                if command_data != None:
                    if len(command_data) != RobotCommand.byte_length():
                        picolog.debug("BlePeripheral::connected_to_central - Invalid reply data length")
                        self.__connected = False
                        continue
                    else:
                        # Process the command data contained in the reply
                        robot_command = RobotCommand.from_packed_bytes(command_data)

                    # nop commands are not logged as they are used to keep the peripheral polling the central
                    if robot_command.command != "nop":
                        picolog.debug(f"BlePeripheral::connected_to_central - Received {robot_command}")
                        self._command_queue.append(robot_command)
                        self._command_queue_event.set()

            # Poll central 5 times a second
            if self.__connected: await asyncio.sleep_ms(200)

    async def handle_disconnection_from_central(self):
        await self.__connection.disconnected()
        self.__connected = False
        self.__connection = None
        picolog.info("BlePeripheral::wait_for_disconnection_from_central - Central disconnected")

    # Main BLE peripheral task
    async def ble_peripheral_task(self):
        picolog.debug("BlePeripheral::ble_peripheral_task - Task started")
        while True:
            await self.advertise_to_central() # Advertise and wait for connection

            # If we are connected, run the connected task
            if self.__connected:
                await self.connected_to_central() # Returns if we are disconnected
                await self.handle_disconnection_from_central() # Handle disconnection

if __name__ == "__main__":
    from main import main
    main()