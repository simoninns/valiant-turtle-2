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
import sys

class Ble_central:
    def __init__(self):
        # Flags to show connected status
        self.connected = False
        self.connection = None

        # Get the local device's Unique ID
        self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Remote device advertising definitions
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910) 
        self.peripheral_advertising_name = "vt2-robot"

        self.fixed_string_8_characteristic = None

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

    # Process battery_service notifications from the peripheral
    def battery_service_notification(self, voltage, current, power):
        log_debug("Ble_central::battery_service_notification - mV =" , voltage, "/ mA =", current, "/ mW =", power)

    # Task to handle battery_service notifications
    async def handle_battery_service_task(self):
        log_debug("Ble_central::handle_battery_service_task - battery_service notification handler running")

        try:
            # Loop waiting for service notifications
            while self.connected:
                battery_voltage_data = await self.battery_voltage_characteristic.notified()
                battery_current_data = await self.battery_current_characteristic.read()
                battery_power_data = await self.battery_power_characteristic.read()
                self.battery_service_notification(data_encode.from_float(battery_voltage_data), data_encode.from_float(battery_current_data), data_encode.from_float(battery_power_data))
                                                            
        except Exception as e:
            log_debug("Ble_central::handle_battery_service_task - Exception was flagged (Peripheral probably disappeared)")
            self.connected = False

    # Process command_service notifications from the peripheral
    def command_service_notification(self, value):
        log_debug("Ble_central::command_service_notification - value =" , value)

    # Task to handle command_service notifications
    async def handle_command_service_task(self):
        log_debug("Ble_central::handle_command_service_task - command_service notification handler running")

        try:
            # Loop waiting for service notifications
            while self.connected:
                value = await self.tx_p2c_characteristic.notified()
                self.command_service_notification(data_encode.from_int16(value))

                # Respond
                response = data_encode.from_int16(value)
                response = response + 2
                log_debug("Ble_central::handle_command_service_task - response =" , response)
                await self.rx_c2p_characteristic.write(data_encode.to_int16(response))
                                                        
        except Exception as e:
            log_debug("Ble_central::handle_command_service_task - Exception was flagged (Peripheral probably disappeared)")
            self.connected = False

    # Tasks when a peripheral is connected
    async def connected_to_peripheral(self):
        log_debug("Ble_central::connected_to_peripheral - Connected to peripheral")

        # Command service setup
        command_service_uuid = bluetooth.UUID(0xFA20)

        try:
            command_service = await self.connection.service(command_service_uuid)
            if command_service == None:
                log_debug("Ble_central::connected_to_peripheral - FATAL: Peripheral command_service is missing!")
                sys.exit()
            
        except asyncio.TimeoutError:
            log_debug("Ble_central::connected_to_peripheral - FATAL: Timeout discovering services/characteristics")
            sys.exit()

        # Command service characteristics setup
        tx_p2c_characteristic_uuid = bluetooth.UUID(0xFBA0) # Custom
        rx_c2p_characteristic_uuid = bluetooth.UUID(0xFBA1) # Custom
        try:
            self.tx_p2c_characteristic = await command_service.characteristic(tx_p2c_characteristic_uuid)
            
            if self.tx_p2c_characteristic == None:
                log_debug("Ble_central::connected_to_peripheral - FATAL: Peripheral command_service tx_p2c_characteristic missing!")
                sys.exit()

        except asyncio.TimeoutError:
            log_debug("Ble_central::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            sys.exit()

        try:
            self.rx_c2p_characteristic = await command_service.characteristic(rx_c2p_characteristic_uuid)
            
            if self.rx_c2p_characteristic == None:
                log_debug("Ble_central::connected_to_peripheral - FATAL: Peripheral command_service rx_c2p_characteristic missing!")
                sys.exit()

        except asyncio.TimeoutError:
            log_debug("Ble_central::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            sys.exit()
        
        # Battery service setup
        battery_service_uuid = bluetooth.UUID(0x180F) # Battery service
        battery_service = await self.connection.service(battery_service_uuid)
        
        try:
            if battery_service == None:
                log_debug("Ble_central::connected_to_peripheral - FATAL: Peripheral battery_service is missing!")
                sys.exit()
            
        except asyncio.TimeoutError:
            log_debug("Ble_central::connected_to_peripheral - FATAL: Timeout discovering service")
            sys.exit()
        
        # Battery service characteristics setup
        battery_voltage_characteristic_uuid = bluetooth.UUID(0xFB10) # Custom
        battery_current_characteristic_uuid = bluetooth.UUID(0xFB12) # Custom
        battery_power_characteristic_uuid = bluetooth.UUID(0xFB11) # Custom
        try:
            self.battery_voltage_characteristic = await battery_service.characteristic(battery_voltage_characteristic_uuid)
            self.battery_current_characteristic = await battery_service.characteristic(battery_current_characteristic_uuid)
            self.battery_power_characteristic = await battery_service.characteristic(battery_power_characteristic_uuid)

            if self.battery_voltage_characteristic == None:
                log_debug("Ble_central::connected_to_peripheral - FATAL: Peripheral battery_service characteristics missing!")
                sys.exit()

        except asyncio.TimeoutError:
            log_debug("Ble_central::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            sys.exit()

        # Subscribe to characteristic notifications
        await self.tx_p2c_characteristic.subscribe(notify = True)
        await self.battery_voltage_characteristic.subscribe(notify = True)

        # Send a response of 12345 to the peripheral to show we are connected and ready
        await self.rx_c2p_characteristic.write(data_encode.to_int16(12345))

        # Generate a task for each service and then run them
        central_tasks = [
            asyncio.create_task(self.handle_command_service_task()),
            asyncio.create_task(self.handle_battery_service_task()),
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