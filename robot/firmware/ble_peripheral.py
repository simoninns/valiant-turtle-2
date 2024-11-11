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

from log import log_debug, log_info, log_warn

import aioble
import bluetooth
import machine
import asyncio

class Ble_peripheral:
    def __init__(self):
        # Flags to show connected status
        self.connected = False
        self.alive = False

    async def scan_for_vt2_communicator(self):
        env_sense_uuid = bluetooth.UUID(0x1800) 
        # Scan for 5 seconds, in active mode, with very low interval/window (to
        # maximise detection rate).
        log_debug("ble_peripheral::scan_for_vt2_communicator - Scanning for VT2 communicator device...")
        async with aioble.scan(duration_ms = 5000, interval_us = 30000, window_us = 30000, active = True) as scanner:
            async for result in scanner:
                # See if it matches our name
                if result.name() == "vt2-robot":
                    log_debug("Ble_peripheral::scan_for_vt2_communicator - Found VT2 communicator device")
                    for item in result.services():
                        log_debug("Ble_peripheral::scan_for_vt2_communicator - Got service:", item)
                    if env_sense_uuid in result.services():
                        log_debug("Ble_peripheral::scan_for_vt2_communicator - VT2 device provides required service UUID")
                        return result.device

        return None

    # Property that is true when BLE is connected
    @property
    def is_connected(self) -> bool:
        return self.connected

    # Just a dummy for testing...
    def move_robot(self, command):
        if command == b'a':
            print("a button pressed")
        elif command == b'b':
            print("b button pressed")
        elif command == b'x':
            print("x button pressed")
        elif command == b'y':
            print("y button pressed")

    async def connect_to_vt2_communicator(self):
        # Bluetooth UUIDS can be found online at https://www.bluetooth.com/specifications/gatt/services/
        remote_uuid = bluetooth.UUID(0x1848)
        remote_characteristics_uuid = bluetooth.UUID(0x2A6E)
        
        self.connected = False
        device = await self.scan_for_vt2_communicator()
        if not device:
            log_debug("Ble_peripheral::connect_to_vt2_communicator - VT2 Communicator not found")
            return
        try:
            log_debug("Ble_peripheral::connect_to_vt2_communicator - VT2 Communicator with address", device.addr_hex(), "found.  Attempting to connect")
            connection = await device.connect()
            
        except asyncio.TimeoutError:
            log_debug("Ble_peripheral::connect_to_vt2_communicator - Connection attempt timed out!")
            return
        
        async with connection:
            log_debug("Ble_peripheral::connect_to_vt2_communicator - Connected to VT2 communicator")
            self.alive = True
            self.connected = True

            robot_service = await connection.service(remote_uuid)
            control_characteristic = await robot_service.characteristic(remote_characteristics_uuid)
            
            while True:
                try:
                    if robot_service == None:
                        log_debug("Ble_peripheral::connect_to_vt2_communicator - VT2 Communicator disconnected")
                        self.alive = False
                        break
                    
                except asyncio.TimeoutError:
                    log_debug("Ble_peripheral::connect_to_vt2_communicator - Timeout discovering services/characteristics")
                    self.alive = False
                    break
                
                if control_characteristic == None:
                    log_debug("Ble_peripheral::connect_to_vt2_communicator - no control characteristics found")
                    self.alive = False
                    break
            
                try:
                    data = await control_characteristic.read(timeout_ms = 1000)

                    await control_characteristic.subscribe(notify = True)
                    while True:
                        command = await control_characteristic.notified()
                        self.move_robot(command)
                                                                
                except Exception as e:
                    log_debug("Ble_peripheral::connect_to_vt2_communicator - Exception was flagged, device gone?")
                    self.connected = False
                    self.alive = False
                    break

            await connection.disconnected()
            log_debug("Ble_peripheral::connect_to_vt2_communicator - VT2 Communicator disconnected")
            self.alive = False

    async def ble_peripheral_task(self):
        log_debug("Ble_peripheral::ble_peripheral_task - Task started")
        while True:
            await self.connect_to_vt2_communicator()