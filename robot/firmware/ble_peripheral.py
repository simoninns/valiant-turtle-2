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

from machine import Pin, unique_id
from micropython import const

import aioble
import bluetooth
import asyncio

import data_encode
import sys

class Ble_peripheral:
    def __init__(self):
        # Get the local device's Unique ID (used as the serial number)
        self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Flags to show connected status
        self.connection = None
        self.connected = False

        # Advertising definitions
        self.__ble_advertising_definitions()

        # Service definitions
        self.__ble_service_command_definitions()
        self.__ble_service_battery_definition()

        # Register services with aioBLE library
        aioble.register_services(self.command_service, self.battery_service)

    def __ble_advertising_definitions(self):
        # Definitions used for advertising via BLE

        # Set our advertising UUID
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910)

        # Set our appearance to "Remote Control"
        self.peripheral_appearance_generic_remote_control = const(0x0180)

        self.peripheral_advertising_name = "vt2-robot"
        self.peripheral_manufacturer = (0xFFE1, b"www.waitingforfriday.com")

    # Define a service - command
    def __ble_service_command_definitions(self):
        # Create a command service and attach a button characteristic to it
        command_service_uuid = bluetooth.UUID(0xFA20) # Custom
        tx_p2c_characteristic_uuid = bluetooth.UUID(0xFBA0) # Custom
        rx_c2p_characteristic_uuid = bluetooth.UUID(0xFBA1) # Custom

        self.command_service = aioble.Service(command_service_uuid)

        # TX: Peripheral -> Central
        self.tx_p2c_characteristic = aioble.BufferedCharacteristic(self.command_service, tx_p2c_characteristic_uuid, notify=True, max_len=20)
        # RX: Central -> Peripheral
        self.rx_c2p_characteristic = aioble.Characteristic(self.command_service, rx_c2p_characteristic_uuid, write=True, write_no_response=True, capture=True)

    # Define a service - battery information
    def __ble_service_battery_definition(self):
        battery_service_uuid = bluetooth.UUID(0x180F) # Battery service
        battery_voltage_characteristic_uuid = bluetooth.UUID(0xFB10) # Custom
        battery_current_characteristic_uuid = bluetooth.UUID(0xFB12) # Custom
        battery_power_characteristic_uuid = bluetooth.UUID(0xFB11) # Custom

        self.battery_service = aioble.Service(battery_service_uuid)

        self.battery_voltage_characteristic = aioble.Characteristic(self.battery_service, battery_voltage_characteristic_uuid, read=True, notify=True)
        self.battery_current_characteristic = aioble.Characteristic(self.battery_service, battery_current_characteristic_uuid, read=True, notify=False)
        self.battery_power_characteristic = aioble.Characteristic(self.battery_service, battery_power_characteristic_uuid, read=True, notify=False)

    # Property that is true when central (VT2 Communicator) is connected
    @property
    def is_central_connected(self) -> bool:
        return self.connected

    async def wait_for_data(self, characteristic, t_ms=5000):
        try:
            _, data = await characteristic.written(timeout_ms=t_ms)
            return data
        except asyncio.TimeoutError:
            log_debug("Ble_peripheral::wait_for_data - Data timed-out - (Central probably disappeared)")
            self.connected = False
            return None

    # Send battery service characteristics update
    def battery_service_update(self, voltage, current, power):
        if self.connected:
            log_debug("Ble_peripheral::battery_service_update - mV =" , voltage, "/ mA =", current, "/ mW =", power)
            try:
                self.battery_voltage_characteristic.notify(self.connection, data_encode.to_float(voltage))
                self.battery_current_characteristic.write(data_encode.to_float(current))
                self.battery_power_characteristic.write(data_encode.to_float(power))
            
            except Exception as e:
                log_debug("Ble_peripheral::battery_service_update - Exception was flagged (Central probably disappeared)")
                self.connected = False
    
    # Send command service characteristics update
    def command_service_update(self, value):
        if self.connected:
            log_debug("Ble_peripheral::command_service_update - value =", value)
            try:
                # Send from p2c
                self.tx_p2c_characteristic.notify(self.connection, data_encode.to_int16(value))
                
            except Exception as e:
                log_debug("Ble_peripheral::command_service_update - Exception was flagged (Central probably disappeared)")
                self.connected = False

    # This is just for testing purposes
    async def command_service_update_task(self):
        value = 0
        while self.connected:
            self.command_service_update(value)
            value += 1
            if value == 256: value = 0

            # Command service update time out can cause disconnection - only wait for reply if still connected...
            if self.connected:
                # Receive from c2p
                reply_data = await self.wait_for_data(self.rx_c2p_characteristic)
                log_debug("Ble_peripheral::command_service_update - Reply data =", data_encode.from_int16(reply_data))

                await asyncio.sleep_ms(1000)

    # Tasks to run whilst connected to central  
    async def connected_to_central(self):
        # Generate a task for each service and then run them
        peripheral_tasks = [
            asyncio.create_task(self.command_service_update_task()),
        ]
        log_info("Ble_peripheral::connected_to_central - Running tasks during connection")
        await asyncio.gather(*peripheral_tasks)

    async def wait_for_disconnection_from_central(self):
        await self.connection.disconnected()
        self.connected = False
        self.connection = None
        log_info("Ble_peripheral::wait_for_disconnection_from_central - Central disconnected")

    # Advertise peripheral to central
    async def advertise_to_central(self):
        # BLE Advertising frequency
        ble_advertising_frequency_us = const(250000)

        # Wait for something to connect
        log_debug("Ble_peripheral::advertise_to_central - Advertising and waiting for connection from central...")
        self.connection = await aioble.advertise(
                ble_advertising_frequency_us,
                name = self.peripheral_advertising_name,
                services = [self.peripheral_advertising_uuid],
                appearance = self.peripheral_appearance_generic_remote_control,
                manufacturer = self.peripheral_manufacturer,
            )
        log_info("Ble_peripheral::advertise_to_central - Central with address", self.connection.device.addr_hex(), "has connected - advertising stopped")

        # It takes a while for the central to really connect.  So, to avoid data dropping into a black hole
        # the central will start by sending us a byte of data.  Once received, we can mark it as connected for real
        log_debug("Ble_peripheral::advertise_to_central - Waiting for central to confirm connection...")
        reply_data = await self.wait_for_data(self.rx_c2p_characteristic)
        if reply_data != None:
            if data_encode.from_int16(reply_data) == 12345:
                log_debug("Ble_peripheral::advertise_to_central - Central has confirmed as connected")
                self.connected = True
            else:
                log_debug("Ble_peripheral::advertise_to_central - Central did not respond with 12345 - Reverting to disconnected state")
                self.connected = False
        else:
            log_debug("Ble_peripheral::advertise_to_central - Central did not respond - Reverting to disconnected state")
            self.connected = False

    # Main BLE peripheral task
    async def ble_peripheral_task(self):
        log_debug("Ble_peripheral::ble_peripheral_task - Task started")
        while True:
            await self.advertise_to_central()

            if self.connected:
                await self.connected_to_central()
                await self.wait_for_disconnection_from_central()