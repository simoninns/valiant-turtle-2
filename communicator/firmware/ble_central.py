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

import data_encode

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
    
    # Process command_service notifications from the peripheral
    def command_service_notification(self, data):
        if data == b'a':
            log_debug("Ble_central::command_service_notification - Button A pressed")
        elif data == b'b':
            log_debug("Ble_central::command_service_notification - Button B pressed")
        elif data == b'x':
            log_debug("Ble_central::command_service_notification - Button X pressed")
        elif data == b'y':
            log_debug("Ble_central::command_service_notification - Button Y pressed")
        else:
            log_debug("Ble_central::command_service_notification - Unknown button pressed")

    # Process battery_service notifications from the peripheral
    def battery_service_notification(self, voltage, current, power):
        log_debug("Ble_central::battery_service_notification - mV =" , voltage, "/ mA =", current, "/ mW =", power)

    # Task to handle battery_service notifications
    async def handle_battery_service_task(self, battery_voltage_characteristic, battery_current_characteristic, battery_power_characteristic):
        log_debug("Ble_central::handle_battery_service_task - battery_service notification handler running")

        try:
            # Loop waiting for service notifications
            while self.connected:
                battery_voltage_data = await battery_voltage_characteristic.notified()
                battery_current_data = await battery_current_characteristic.read()
                battery_power_data = await battery_power_characteristic.read()
                self.battery_service_notification(data_encode.from_float(battery_voltage_data), data_encode.from_float(battery_current_data), data_encode.from_float(battery_power_data))
                                                            
        except Exception as e:
            log_debug("Ble_central::handle_battery_service_task - Exception was flagged (Peripheral probably disappeared)")
            self.connected = False

    # Task to handle command_service notifications
    async def handle_command_service_task(self, fixed_string_8_characteristic):
        log_debug("Ble_central::handle_command_service_task - command_service notification handler running")

        try:
            # Loop waiting for service notifications
            while self.connected:
                data = await fixed_string_8_characteristic.notified()
                self.command_service_notification(data)
                                                        
        except Exception as e:
            log_debug("Ble_central::handle_command_service_task - Exception was flagged (Peripheral probably disappeared)")
            self.connected = False

    # Tasks when a peripheral is connected
    async def connected_to_peripheral(self):
        log_debug("Ble_central::connected_to_peripheral - Connected to peripheral")

        # Command service setup
        command_service_uuid = bluetooth.UUID(0xFA20)
        fixed_string_8_characteristic_uuid = bluetooth.UUID(0x2AF8)
        command_service = await self.connection.service(command_service_uuid)
        fixed_string_8_characteristic = await command_service.characteristic(fixed_string_8_characteristic_uuid)

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
        
        # Battery service setup
        battery_service_uuid = bluetooth.UUID(0x180F) # Battery service

        battery_voltage_characteristic_uuid = bluetooth.UUID(0xFB10) # Custom
        battery_current_characteristic_uuid = bluetooth.UUID(0xFB12) # Custom
        battery_power_characteristic_uuid = bluetooth.UUID(0xFB11) # Custom

        battery_service = await self.connection.service(battery_service_uuid)
        battery_voltage_characteristic = await battery_service.characteristic(battery_voltage_characteristic_uuid)
        battery_current_characteristic = await battery_service.characteristic(battery_current_characteristic_uuid)
        battery_power_characteristic = await battery_service.characteristic(battery_power_characteristic_uuid)

        try:
            if battery_service == None:
                log_debug("Ble_central::connected_to_peripheral - Peripheral battery_service is missing!")
                RuntimeError("Peripheral BLE is broken - bettery_service is missing!")
            
        except asyncio.TimeoutError:
            log_debug("Ble_central::connected_to_peripheral - Timeout discovering services/characteristics")
            RuntimeError("Peripheral BLE is broken - Timeout discovering services/characteristics!")
        
        if battery_voltage_characteristic == None:
            log_debug("Ble_central::connected_to_peripheral - Peripheral battery_service battery_level_characteristic missing!")
            RuntimeError("Peripheral BLE is broken - bettery_service battery_voltage_characteristic missing!")

        # Subscribe to characteristic notifications
        await fixed_string_8_characteristic.subscribe(notify = True)
        await battery_voltage_characteristic.subscribe(notify = True)

        # Generate a task for each service and then run them
        central_tasks = [
            asyncio.create_task(self.handle_command_service_task(fixed_string_8_characteristic)),
            asyncio.create_task(self.handle_battery_service_task(battery_voltage_characteristic, battery_current_characteristic, battery_power_characteristic)),
        ]
        await asyncio.gather(*central_tasks)

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