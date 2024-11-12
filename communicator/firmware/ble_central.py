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

from log import log_debug, log_info, log_warn

from machine import Pin, unique_id
from micropython import const

from status_led import Status_led

import sys
import aioble
import bluetooth
import asyncio

class Ble_central:
    def __init__(self, button_pin):
        # Define command buttons
        self.button_a = Pin(button_pin, Pin.IN, Pin.PULL_UP)

        # Get the local device's Unique ID (used as the serial number)
        self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Flags to show connected status
        self.connection = None
        self.connected = False

        # Advertising definitions
        self.__ble_advertising_definitions()

        # Service definitions
        self.__ble_service_command_definitions()
        self.__ble_service_device_info_definitions()
        self.__ble_service_battery_definition()

        # Register services with AIOBLE library
        aioble.register_services(self.command_service_info, self.device_info_service, self.battery_service_info)

    def __ble_advertising_definitions(self):
        # Definitions used for advertising via BLE

        # Set our advertising UUID
        self.vt2_communicator_advertising_uuid = bluetooth.UUID(0xF910)

        # Set our appearance to "Remote Control"
        # See: https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Assigned_Numbers/out/en/Assigned_Numbers.pdf
        # Page 28
        self.ble_appearance_generic_remote_control = const(0x0180)

        self.advertising_name = "vt2-communicator"
        self.manufacturer = (0xFFE1, b"www.waitingforfriday.com")

    # Define a service - command
    def __ble_service_command_definitions(self):
        # Create a command service and attach a button characteristic to it
        command_service_uuid = bluetooth.UUID(0xFA20) # Custom
        characteristic_uuid = bluetooth.UUID(0x2AF8) # Fixed-string 8

        self.command_service_info = aioble.Service(command_service_uuid)

        self.fixed_string_8_characteristic = aioble.Characteristic(self.command_service_info, characteristic_uuid, read=True, notify=True) # Subscribe

    # Define a service - device info with static characteristics
    def __ble_service_device_info_definitions(self):
        # Device information service definitions
        device_information_service_uuid = bluetooth.UUID(0x180A)
        manufacturer_id_characteristic_uuid = bluetooth.UUID(0x02A29)
        model_number_id_characteristic_uuid = bluetooth.UUID(0x2A24)
        serial_number_id_characteristic_uuid = bluetooth.UUID(0x2A25)
        hardware_revision_id_characteristic_uuid = bluetooth.UUID(0x2A26)
        ble_version_id_characteristic_uuid = bluetooth.UUID(0x2A28)

        self.device_info_service = aioble.Service(device_information_service_uuid)
     
        self.manufacturer_id_characteristic = aioble.Characteristic(self.device_info_service, manufacturer_id_characteristic_uuid, read = True, initial = self.manufacturer[1])
        self.model_number_id_characteristic = aioble.Characteristic(self.device_info_service, model_number_id_characteristic_uuid, read = True, initial = "1.0")
        self.serial_number_id_characteristic = aioble.Characteristic(self.device_info_service, serial_number_id_characteristic_uuid, read = True, initial = self.uid)
        self.hardware_revision_id_characteristic = aioble.Characteristic(self.device_info_service, hardware_revision_id_characteristic_uuid, read = True, initial = sys.version)
        self.ble_version_id_characteristic = aioble.Characteristic(self.device_info_service, ble_version_id_characteristic_uuid, read = True, initial = "1.0")

    # Define a service - battery information
    def __ble_service_battery_definition(self):
        battery_service_uuid = bluetooth.UUID(0x180F) # Battery service

        battery_level_characteristic_uuid = bluetooth.UUID(0x2A19) # Battery level
        battery_voltage_characteristic_uuid = bluetooth.UUID(0xFB10) # Custom
        battery_power_characteristic_uuid = bluetooth.UUID(0xFB11) # Custom
        battery_current_characteristic_uuid = bluetooth.UUID(0xFB12) # Custom

        self.battery_service_info = aioble.Service(battery_service_uuid)

        self.battery_level_characteristic = aioble.Characteristic(self.battery_service_info, battery_level_characteristic_uuid, read=True, notify=True)
        self.battery_voltage_characteristic = aioble.Characteristic(self.battery_service_info, battery_voltage_characteristic_uuid, read=True, notify=True)
        self.battery_power_characteristic = aioble.Characteristic(self.battery_service_info, battery_power_characteristic_uuid, read=True, notify=True)
        self.battery_current_characteristic = aioble.Characteristic(self.battery_service_info, battery_current_characteristic_uuid, read=True, notify=True)

    # Process commands task
    async def process_commands_task(self):
        while True:
            if not self.connected:
                # Not connected - wait a second and try again
                await asyncio.sleep_ms(1000)
                continue

            if self.button_a.value() == 0:
                log_info("Ble_central::process_commands_task - Button A pressed")   
                self.fixed_string_8_characteristic.notify(self.connection,b"a")
            # elif button_b.read():
            #     print('Button B pressed')
            #     # button_characteristic.write(b"b")
            #     button_characteristic.notify(connection,b"b")
            # elif button_x.read():
            #     print('Button X pressed')
            #     # button_characteristic.write(b"x")
            #     button_characteristic.notify(connection,b"x")
            # elif button_y.read():
            #     print('Button Y pressed')
            #     # button_characteristic.write(b"y")
            #     button_characteristic.notify(connection,b"x")
            # else:
            #     button_characteristic.notify(connection,b"!")

            await asyncio.sleep_ms(10)
                
    # Serially wait for connections. Don't advertise while a central is connected.    
    async def ble_peripheral_task(self):
        log_debug("Ble_central::peripheral_task - Task started")

        # BLE Advertising frequency
        ble_advertising_frequency_us = const(250000)

        while True:
            # Wait for something to connect
            log_debug("Ble_central::peripheral_task - Advertising service and waiting for connection...")
            self.connection = await aioble.advertise(
                    ble_advertising_frequency_us,
                    name = self.advertising_name,
                    services = [self.vt2_communicator_advertising_uuid],
                    appearance = self.ble_appearance_generic_remote_control,
                    manufacturer = self.manufacturer,
                )
            log_info("Ble_central::peripheral_task - Advertising stopped - BLE connection from", self.connection.device.addr_hex())
            self.connected = True

            # Wait for the connected device to disconnect
            await self.connection.disconnected()
            self.connected = False
            self.connection = None
            log_info("Ble_central::peripheral_task - BLE disconnected")
            
    # Task to blink the blue status LED
    # 1 second blink = connected
    # 1/4 second blink = not connected
    async def connection_status_task(self, status_led: Status_led):
        log_debug("Ble_central::connection_status_task - Task started")
        led_level = 255
        while True:
            status_led.set_brightness(led_level)
            if led_level == 255: led_level = 10
            else: led_level = 255

            blink_delay_ms = 1000
            if not self.connected: blink_delay_ms = 250

            await asyncio.sleep_ms(blink_delay_ms)