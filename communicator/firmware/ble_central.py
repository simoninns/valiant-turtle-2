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
import logging
import aioble
import bluetooth
from machine import unique_id
import asyncio
import data_encode

from robot_comms import PowerMonitor

class BleCentral:
    def __init__(self):
        """Class to manage BLE central tasks"""
        # Flags to show connected status
        self.connected = False
        self.connection = None

        # asyncio events
        self._ble_command_service_event = asyncio.Event()
        self._ble_battery_service_event = asyncio.Event()
        self._host_event = None

        self._host_comms = None

        # Responses
        self._command_service_response = 0
        self._battery_service_response = PowerMonitor(0, 0, 0)

        # Get the local device's Unique ID
        self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Remote device advertising definitions
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910) 
        self.peripheral_advertising_name = "vt2-robot"

        self.fixed_string_8_characteristic = None
    
    @property
    def host_comms(self):
        """Get the host communication object"""
        return self._host_comms
    
    @host_comms.setter
    def host_comms(self, value):
        """Set the host communication object"""
        self._host_comms = value

    @property
    def is_peripheral_connected(self) -> bool:
        """Property that is true when BLE peripheral is connected"""
        return self.connected
    
    @property
    def host_event(self):
        """Get the host event"""
        return self._host_event

    @host_event.setter
    def host_event(self, value: asyncio.Event):
        """Set the host event"""
        self._host_event = value

    @property
    def ble_command_service_event(self):
        """Get the BLE command service event"""
        return self._ble_command_service_event
    
    @property
    def ble_battery_service_event(self):
        """Get the BLE battery service event"""
        return self._ble_battery_service_event

    async def scan_for_peripheral(self):
        """Scan for a BLE peripheral
        Scan for 5 seconds, in active mode, with very low interval/window (to maximize detection rate)."""

        logging.debug("BleCentral::scan_for_peripheral - Scanning for peripheral...")
        async with aioble.scan(duration_ms = 5000, interval_us = 30000, window_us = 30000, active = True) as scanner:
            async for result in scanner:
                # See if it matches our name
                if result.name() == self.peripheral_advertising_name:
                    logging.debug(f"BleCentral::scan_for_peripheral - Found peripheral with matching advertising name of {self.peripheral_advertising_name}")
                    for item in result.services():
                        logging.debug("BleCentral::scan_for_peripheral - Got advertised UUID:", item)
                    if self.peripheral_advertising_uuid in result.services():
                        logging.debug("BleCentral::scan_for_peripheral - Peripheral advertises required UUID")
                        return result.device

        return None

    async def connect_to_peripheral(self):
        """Connect to a BLE peripheral by performing a scan and then connecting to the first one found with the correct name and UUID"""
        self.connected = False
        device = await self.scan_for_peripheral()
        if not device:
            logging.debug("BleCentral::connect_to_peripheral - Peripheral not found")
            return
        try:
            logging.debug(f"BleCentral::connect_to_peripheral - Peripheral with address {device.addr_hex()} found.  Attempting to connect")
            self.connection = await device.connect()
            logging.info(f"BleCentral::connect_to_peripheral - Connected to peripheral with address {device.addr_hex()}")
            self.connected = True
            
        except asyncio.TimeoutError:
            logging.debug("BleCentral::connect_to_peripheral - Connection attempt timed out!")
            return

    def battery_service_notification(self, voltage, current, power):
        """Process battery_service notifications from the peripheral"""
        self._battery_service_response.status = (voltage, current, power)
        self._ble_battery_service_event.set() # Flag the event
        logging.debug(f"BleCentral::battery_service_notification - {self._battery_service_response.voltage_mV_fstring} / {self._battery_service_response.current__mA_fstring} / {self._battery_service_response.power__mW_fstring}")

    def get_battery_service_response(self):
        """Provide the battery service response and clear the event flag"""
        self._ble_battery_service_event.clear()
        return self._battery_service_response

    async def handle_battery_service_task(self):
        """Task to handle battery_service notifications"""
        logging.debug("BleCentral::handle_battery_service_task - battery_service notification handler running")

        try:
            # Loop waiting for service notifications
            while self.connected:
                battery_voltage_data = await self.battery_voltage_characteristic.notified()
                battery_current_data = await self.battery_current_characteristic.read()
                battery_power_data = await self.battery_power_characteristic.read()
                self.battery_service_notification(data_encode.from_float(battery_voltage_data), data_encode.from_float(battery_current_data), data_encode.from_float(battery_power_data))
                                                            
        except Exception as e:
            logging.debug("BleCentral::handle_battery_service_task - Exception was flagged (Peripheral probably disappeared)")
            self.connected = False

    def command_service_notification(self, value):
        """Process command_service notifications from the peripheral"""
        logging.debug(f"BleCentral::command_service_notification - Command response from robot = {value}")
        self._command_service_response = value
        self._ble_command_service_event.set() # Flag the event

    def get_command_service_response(self):
        """Provide the command service response and clear the event flag"""
        self._ble_command_service_event.clear()
        return self._command_service_response

    async def handle_command_service_task(self):
        """Task to handle command_service notifications"""
        logging.debug("BleCentral::handle_command_service_task - command_service notification handler running")

        try:
            # Loop waiting for service notifications
            while self.connected:
                value = await self.tx_p2c_characteristic.notified()
                self.command_service_notification(data_encode.from_int16(value))

                # Respond
                response = data_encode.from_int16(value)
                response = response + 2
                logging.debug(f"BleCentral::handle_command_service_task - response = {response}")
                await self.rx_c2p_characteristic.write(data_encode.to_int16(response))
                                                        
        except Exception as e:
            logging.debug("BleCentral::handle_command_service_task - Exception was flagged (Peripheral probably disappeared)")
            self.connected = False

    async def connected_to_peripheral(self):
        """Tasks to perform when connected to a peripheral"""
        logging.debug("BleCentral::connected_to_peripheral - Connected to peripheral")

        # Command service setup
        command_service_uuid = bluetooth.UUID(0xFA20)

        try:
            command_service = await self.connection.service(command_service_uuid)
            if command_service == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral command_service is missing!")
                self.connected = False
                return
            
        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering services/characteristics")
            self.connected = False
            return

        # Command service characteristics setup
        tx_p2c_characteristic_uuid = bluetooth.UUID(0xFBA0) # Custom
        rx_c2p_characteristic_uuid = bluetooth.UUID(0xFBA1) # Custom
        try:
            self.tx_p2c_characteristic = await command_service.characteristic(tx_p2c_characteristic_uuid)
            
            if self.tx_p2c_characteristic == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral command_service tx_p2c_characteristic missing!")
                self.connected = False
                return

        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            self.connected = False
            return

        try:
            self.rx_c2p_characteristic = await command_service.characteristic(rx_c2p_characteristic_uuid)
            
            if self.rx_c2p_characteristic == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral command_service rx_c2p_characteristic missing!")
                self.connected = False
                return

        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            self.connected = False
            return
        
        # Battery service setup
        battery_service_uuid = bluetooth.UUID(0x180F) # Battery service
        battery_service = await self.connection.service(battery_service_uuid)
        
        try:
            if battery_service == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral battery_service is missing!")
                self.connected = False
                return
            
        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering service")
            self.connected = False
            return
        
        # Battery service characteristics setup
        battery_voltage_characteristic_uuid = bluetooth.UUID(0xFB10) # Custom
        battery_current_characteristic_uuid = bluetooth.UUID(0xFB11) # Custom
        battery_power_characteristic_uuid = bluetooth.UUID(0xFB12) # Custom
        try:
            self.battery_voltage_characteristic = await battery_service.characteristic(battery_voltage_characteristic_uuid)
            self.battery_current_characteristic = await battery_service.characteristic(battery_current_characteristic_uuid)
            self.battery_power_characteristic = await battery_service.characteristic(battery_power_characteristic_uuid)

            if self.battery_voltage_characteristic == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral battery_service characteristics missing!")
                self.connected = False
                return

        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            self.connected = False
            return

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

    async def wait_for_disconnection_from_peripheral(self):
        """Wait for disconnection from the peripheral"""
        try:
            await self.connection.disconnected(timeout_ms=2000)
            logging.info("BleCentral::wait_for_disconnection_from_peripheral - Peripheral disconnected")
        except asyncio.TimeoutError:
            logging.info("BleCentral::wait_for_disconnection_from_peripheral - Disconnection timeout")

        self.connection = None
        self.connected = False

    async def ble_central_task(self):
        """Main BLE central task"""
        logging.debug("BleCentral::ble_central_task - Task started")

        while True:
            await self.connect_to_peripheral()

            if self.connected:
                await self.connected_to_peripheral()
                await self.wait_for_disconnection_from_peripheral()

if __name__ == "__main__":
    from main import main
    main()