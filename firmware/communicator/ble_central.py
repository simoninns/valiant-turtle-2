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
import library.logging as logging
import aioble
import bluetooth
from machine import unique_id
import asyncio
import struct

from library.robot_comms import PowerMonitor, RobotCommand

class BleCentral:
    CONNECTION_CONFIRMATION_CODE = 12345
    ADVERTISING_NAME = "vt2-robot"

    def __init__(self):
        """Class to manage BLE central tasks"""
        # Flags to show connected status
        self.connected = False
        self.connection = None

        # asyncio events
        self._ble_command_service_event = asyncio.Event()
        self._ble_power_service_event = asyncio.Event()
        self._host_event = None

        self._host_comms = None

        # Responses
        self._command_service_response = 0
        self._power_service_response = PowerMonitor(0, 0, 0)

        # Get the local device's Unique ID
        self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Remote device advertising definitions
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910) 
        self.peripheral_advertising_name = BleCentral.ADVERTISING_NAME

        self.fixed_string_8_characteristic = None

        # Queue for commands to be sent to the peripheral
        self._command_queue = []
    
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
    def ble_power_service_event(self):
        """Get the BLE power service event"""
        return self._ble_power_service_event

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

    def power_service_notification(self, voltage, current, power):
        """Process power_service notifications from the peripheral"""
        self._power_service_response.status = (voltage, current, power)
        self._ble_power_service_event.set() # Flag the event
        logging.debug(f"BleCentral::power_service_notification - {self._power_service_response}")

    def get_power_service_response(self):
        """Provide the power service response and clear the event flag"""
        self._ble_power_service_event.clear()
        return self._power_service_response

    async def handle_power_service_task(self):
        """Task to handle power_service notifications"""
        logging.debug("BleCentral::handle_power_service_task - power_service notification handler running")

        try:
            # Loop waiting for service notifications
            while self.connected:
                power_voltage_data = await self.power_voltage_characteristic.notified()
                power_current_data = await self.power_current_characteristic.read()
                power_watts_data = await self.power_watts_characteristic.read()
                self.power_service_notification(
                    struct.unpack("<f", power_voltage_data)[0],
                    struct.unpack("<f", power_current_data)[0],
                    struct.unpack("<f", power_watts_data)[0],
                )
                                                            
        except Exception as e:
            logging.debug("BleCentral::handle_power_service_task - Exception was flagged (Peripheral probably disappeared)")
            self.connected = False

    def command_service_notification(self, value):
        """Process command_service notifications from the peripheral"""
        #logging.debug(f"BleCentral::command_service_notification - Command response from robot = {value}")
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
                self.command_service_notification(struct.unpack("<L", value)[0])

                # Check for any commands to send to the peripheral and, if there aren't any, send a nop command
                if len(self._command_queue) > 0:
                    # Send the next command in the queue
                    command = self._command_queue.pop(0)
                    if not isinstance(command, RobotCommand):
                        raise TypeError("Expected command to be of type RobotCommand")
                    logging.debug(f"BleCentral::handle_command_service_task - Sending {command}")
                    await self.rx_c2p_characteristic.write(command.get_packed_bytes())
                else:
                    # No commands queued, send a nop command
                    command = RobotCommand("nop")
                    #logging.debug("BleCentral::handle_command_service_task - No queued commands, sending nop command")
                    await self.rx_c2p_characteristic.write(command.get_packed_bytes())
                                                        
        except Exception as e:
            logging.debug("BleCentral::handle_command_service_task - Exception was flagged (Peripheral probably disappeared)")
            logging.debug(f"BleCentral::handle_command_service_task - Exception: {e}")
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
        
        # Power service setup
        power_service_uuid = bluetooth.UUID(0x180F) # Battery service
        power_service = await self.connection.service(power_service_uuid)
        
        try:
            if power_service == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral power_service is missing!")
                self.connected = False
                return
            
        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering service")
            self.connected = False
            return
        
        # Power service characteristics setup
        power_voltage_characteristic_uuid = bluetooth.UUID(0xFB10) # Custom
        power_current_characteristic_uuid = bluetooth.UUID(0xFB11) # Custom
        power_watts_characteristic_uuid = bluetooth.UUID(0xFB12) # Custom
        try:
            self.power_voltage_characteristic = await power_service.characteristic(power_voltage_characteristic_uuid)
            self.power_current_characteristic = await power_service.characteristic(power_current_characteristic_uuid)
            self.power_watts_characteristic = await power_service.characteristic(power_watts_characteristic_uuid)

            if self.power_voltage_characteristic == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral power_service characteristics missing!")
                self.connected = False
                return

        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            self.connected = False
            return

        # Subscribe to characteristic notifications
        await self.tx_p2c_characteristic.subscribe(notify = True)
        await self.power_voltage_characteristic.subscribe(notify = True)

        # Send a response of 12345 to the peripheral to show we are connected and ready
        await self.rx_c2p_characteristic.write(struct.pack("<L", int(BleCentral.CONNECTION_CONFIRMATION_CODE)))

        # Generate a task for each service and then run them
        central_tasks = [
            asyncio.create_task(self.handle_command_service_task()),
            asyncio.create_task(self.handle_power_service_task()),
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

    async def queue_command(self, command: RobotCommand):
        """Queue a command to be sent to the peripheral"""
        self._command_queue.append(command)

if __name__ == "__main__":
    from main import main
    main()