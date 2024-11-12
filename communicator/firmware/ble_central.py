#************************************************************************ 
#
#   ble_central.py
#
#   BLE Central role
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

import aioble.device
from log import log_debug, log_info, log_warn

import aioble
import bluetooth
from machine import unique_id
import asyncio

class Ble_central:
    def __init__(self):
        # Flags to show connected status
        self.connected = False
        self.connection = None

        # Get the local device's Unique ID
        self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Define the device we want to connect to:

        # Remote device advertising definitions
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910) 
        self.peripheral_advertising_name = "vt2-robot"

    # Property that is true when peripheral is connected
    @property
    def is_peripheral_connected(self) -> bool:
        return self.connected

    # Process commands received from the VT2 robot
    def process_command(self, command):
        if command == b'a':
            log_debug("Ble_central::process_command - Button A pressed")
        elif command == b'b':
            log_debug("Ble_central::process_command - Button B pressed")
        elif command == b'x':
            log_debug("Ble_central::process_command - Button X pressed")
        elif command == b'y':
            log_debug("Ble_central::process_command - Button Y pressed")

    # Scan for a peripheral
    async def scan_for_peripheral(self):
        # Scan for 5 seconds, in active mode, with very low interval/window (to
        # maximise detection rate).
        log_debug("Ble_central::scan_for_peripheral - Scanning for peripheral...")
        async with aioble.scan(duration_ms = 5000, interval_us = 30000, window_us = 30000, active = True) as scanner:
            async for result in scanner:
                # See if it matches our name
                if result.name() == self.peripheral_advertising_name:
                    log_debug("Ble_central::scan_for_peripheral - Found peripheral with matching advertising name of", self.peripheral_advertising_name)
                    for item in result.services():
                        log_debug("Ble_central::scan_for_peripheral - Got advertised UUID:", item)
                    if self.peripheral_advertising_uuid in result.services():
                        log_debug("Ble_central::scan_for_peripheral - Peripheral advertises required UUID")
                        return result.device

        return None

    # Connect to a peripheral
    async def connect_to_peripheral(self):
        self.connected = False
        device = await self.scan_for_peripheral()
        if not device:
            log_debug("Ble_central::connect_to_peripheral - Peripheral not found")
            return
        try:
            log_debug("Ble_central::connect_to_peripheral - Peripheral with address", device.addr_hex(), "found.  Attempting to connect")
            self.connection = await device.connect()
            log_debug("Ble_central::connect_to_peripheral - Connection to peripheral successful")
            self.connected = True
            
        except asyncio.TimeoutError:
            log_debug("Ble_central::connect_to_peripheral - Connection attempt timed out!")
            return
    
    # Tasks when a peripheral is connected
    async def connected_to_peripheral(self):
        log_debug("Ble_central::connected_to_peripheral - Connected to peripheral")

        # Command service
        command_service_uuid = bluetooth.UUID(0xFA20)
        fixed_string_8_characteristic_uuid = bluetooth.UUID(0x2AF8)
        command_service = await self.connection.service(command_service_uuid)
        fixed_string_8_characteristic = await command_service.characteristic(fixed_string_8_characteristic_uuid)

        # Ensure that we connected correctly to the service and characteristics...
        try:
            if command_service == None:
                log_debug("Ble_central::connected_to_peripheral - Peripheral command_service is missing!")
                RuntimeError("Peripheral BLE is broken - command_service is missing!")
            
        except asyncio.TimeoutError:
            log_debug("Ble_central::connected_to_peripheral - Timeout discovering services/characteristics")
            RuntimeError("Peripheral BLE is broken - Timeout discovering services/characteristics!")
        
        if fixed_string_8_characteristic == None:
            log_debug("Ble_central::connected_to_peripheral - Peripheral command_service fixed_string_8_characteristic missing!")
            RuntimeError("Peripheral BLE is broken - command_service fixed_string_8_characteristic missing!")
        
        # Enter a loop waiting for BLE notifications
        while True:
            try:
                # VT2 Robot connected - loop waiting for notifications
                #data = await control_characteristic.read(timeout_ms = 1000)

                await fixed_string_8_characteristic.subscribe(notify = True)
                while True:
                    command = await fixed_string_8_characteristic.notified()
                    self.process_command(command)
                                                            
            except Exception as e:
                log_debug("Ble_central::connected_to_peripheral - Exception was flagged (Peripheral probably disappeared)")
                self.connected = False
                break

    # Wait for disconnection from the peripheral
    async def wait_for_disconnection_from_peripheral(self):
        await self.connection.disconnected()

        log_debug("Ble_central::wait_for_disconnection_from_peripheral - Peripheral disconnected")
        self.connection = None

    # Main BLE central task
    async def ble_central_task(self):
        log_debug("Ble_central::ble_central_task - Task started")
        while True:
            await self.connect_to_peripheral()

            if self.connected:
                await self.connected_to_peripheral()
                await self.wait_for_disconnection_from_peripheral()