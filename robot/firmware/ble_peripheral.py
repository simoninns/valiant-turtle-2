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
from log import log_debug, log_info, log_warn

import aioble
import bluetooth
from machine import unique_id
import asyncio

class Ble_peripheral:
    def __init__(self):
        # Flags to show connected status
        self.connected = False
        self.connection = None

        # Get the local device's Unique ID
        self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Define the device we want to connect to:

        # Remote device advertising definitions
        self.vt2_communicator_advertising_uuid = bluetooth.UUID(0xF910) 
        self.vt2_communicator_advertising_name = "vt2-communicator"

    # Property that is true when VT2 Communicator is connected
    @property
    def is_vt2_communicator_connected(self) -> bool:
        return self.connected

    # Process commands received from the VT2 communicator
    def process_command(self, command):
        if command == b'a':
            log_debug("Ble_peripheral::process_command - Button A pressed")
        elif command == b'b':
            log_debug("Ble_peripheral::process_command - Button B pressed")
        elif command == b'x':
            log_debug("Ble_peripheral::process_command - Button X pressed")
        elif command == b'y':
            log_debug("Ble_peripheral::process_command - Button Y pressed")

    # Scan for a VT2 Communicator
    async def scan_for_vt2_communicator(self):
        # Scan for 5 seconds, in active mode, with very low interval/window (to
        # maximise detection rate).
        log_debug("Ble_peripheral::scan_for_vt2_communicator - Scanning for VT2 communicator device...")
        async with aioble.scan(duration_ms = 5000, interval_us = 30000, window_us = 30000, active = True) as scanner:
            async for result in scanner:
                # See if it matches our name
                if result.name() == self.vt2_communicator_advertising_name:
                    log_debug("Ble_peripheral::scan_for_vt2_communicator - Found VT2 communicator device with matching advertising name of", self.vt2_communicator_advertising_name)
                    for item in result.services():
                        log_debug("Ble_peripheral::scan_for_vt2_communicator - Got advertised UUID:", item)
                    if self.vt2_communicator_advertising_uuid in result.services():
                        log_debug("Ble_peripheral::scan_for_vt2_communicator - VT2 device advertises required UUID")
                        return result.device

        return None

    # Connect to a VT2 Communicator
    async def connect_to_vt2_communicator(self):
        self.connected = False
        device = await self.scan_for_vt2_communicator()
        if not device:
            log_debug("Ble_peripheral::connect_to_vt2_communicator - VT2 Communicator not found")
            return
        try:
            log_debug("Ble_peripheral::connect_to_vt2_communicator - VT2 Communicator with address", device.addr_hex(), "found.  Attempting to connect")
            self.connection = await device.connect()
            log_debug("Ble_peripheral::connect_to_vt2_communicator - Connection to VT2 Communicator successful")
            self.connected = True
            
        except asyncio.TimeoutError:
            log_debug("Ble_peripheral::connect_to_vt2_communicator - Connection attempt timed out!")
            return
    
    # Tasks when VT2 Communicator is connected
    async def connected_to_vt2_communicator(self):
        log_debug("Ble_peripheral::connected_to_vt2_communicator - Connected to VT2 communicator")

        generic_service_uuid = bluetooth.UUID(0x1848)
        generic_service_button_characteristic_uuid = bluetooth.UUID(0x2A6E)
        robot_service = await self.connection.service(generic_service_uuid)
        control_characteristic = await robot_service.characteristic(generic_service_button_characteristic_uuid)
        
        while True:
            try:
                if robot_service == None:
                    log_debug("Ble_peripheral::connected_to_vt2_communicator - VT2 Communicator providing no services!")
                    break
                
            except asyncio.TimeoutError:
                log_debug("Ble_peripheral::connected_to_vt2_communicator - Timeout discovering services/characteristics")
                break
            
            if control_characteristic == None:
                log_debug("Ble_peripheral::connected_to_vt2_communicator - VT2 Communicator providing no characteristics")
                break
        
            try:
                # VT2 Communicator connected - loop waiting for notifications
                #data = await control_characteristic.read(timeout_ms = 1000)

                await control_characteristic.subscribe(notify = True)
                while True:
                    command = await control_characteristic.notified()
                    self.process_command(command)
                                                            
            except Exception as e:
                log_debug("Ble_peripheral::connected_to_vt2_communicator - Exception was flagged (VT2 Communicator probably disappeared)")
                self.connected = False
                break

    # Wait for disconnection from the VT2 communicator
    async def wait_for_disconnection_from_vt2_communicator(self):
        await self.connection.disconnected()

        log_debug("Ble_peripheral::connect_to_vt2_communicator - VT2 Communicator disconnected")
        self.connection = None

    # Main BLE peripheral task
    async def ble_peripheral_task(self):
        log_debug("Ble_peripheral::ble_peripheral_task - Task started")
        while True:
            await self.connect_to_vt2_communicator()

            if self.connected:
                await self.connected_to_vt2_communicator()
                await self.wait_for_disconnection_from_vt2_communicator()