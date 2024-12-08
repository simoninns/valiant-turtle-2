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
    __CONNECTION_CONFIRMATION_CODE = 12345
    __ADVERTISING_NAME = "vt2-robot"

    def __init__(self):
        """Class to manage BLE central tasks"""
        # Flags to show connected status
        self._connected = False
        self._connection = None

        # asyncio events
        self._ble_command_service_event = asyncio.Event()
        self._host_event = None
        self._host_comms = None

        # Get the local device's Unique ID
        self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Remote device advertising definitions
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910) 
        self.peripheral_advertising_name = BleCentral.__ADVERTISING_NAME

        # Queue for commands to be sent to the peripheral
        self._command_queue = []
        self._last_processed_command_uid = 0
        self._last_processed_command_response = 0
    
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
        return self._connected
    
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

    async def scan_for_peripheral(self):
        """Scan for a BLE peripheral
        Scan for 5 seconds, in active mode, with very low interval/window (to maximize detection rate)."""

        logging.debug("BleCentral::scan_for_peripheral - Scanning for peripheral...")
        async with aioble.scan(duration_ms = 5000, interval_us = 30000, window_us = 30000, active = True) as scanner:
            async for result in scanner:
                # See if it matches our name
                if result.name() == self.peripheral_advertising_name:
                    logging.debug(f"BleCentral::scan_for_peripheral - Found peripheral with matching advertising name of {self.peripheral_advertising_name}")
                    if self.peripheral_advertising_uuid in result.services():
                        logging.debug("BleCentral::scan_for_peripheral - Peripheral advertises expected BLE UUID")
                        return result.device

        return None

    async def connect_to_peripheral(self):
        """Connect to a BLE peripheral by performing a scan and then connecting to the first one found with the correct name and UUID"""
        self._connected = False
        device = await self.scan_for_peripheral()
        if not device:
            logging.debug("BleCentral::connect_to_peripheral - Peripheral not found")
            return
        try:
            logging.debug(f"BleCentral::connect_to_peripheral - Peripheral with address {device.addr_hex()} found.  Attempting to connect")
            self._connection = await device.connect()
            logging.info(f"BleCentral::connect_to_peripheral - Connected to peripheral with address {device.addr_hex()}")
            self._connected = True
            
        except asyncio.TimeoutError:
            logging.debug("BleCentral::connect_to_peripheral - Connection attempt timed out!")
            return

    def command_service_notification(self, last_processed_command_response, last_processed_command_uid):
        """Process command_service notifications from the peripheral"""
        self._last_processed_command_response = last_processed_command_response
        self._last_processed_command_uid = last_processed_command_uid
        self._ble_command_service_event.set() # Flag the event

    def acknowledge_command_service_response(self):
        """Acknowledge the command_service response"""
        self._ble_command_service_event.clear()

    def get_command_response(self) -> int:
        """Get the last command response"""
        return self._last_processed_command_response

    async def handle_command_service_task(self):
        """
        Task to handle command_service notifications.

        Since we are using BLE a polling mechanism is used where the peripheral sends a notification
        and, if we have a waiting command, we sent it back to the peripheral.  If there are no waiting
        commands then a nop command is sent to the peripheral.  In addition, the polling notification from
        the peripheral is used to update the last processed command UID as well as a status byte of flags
        that show the peripheral's current state.
        """
        
        logging.debug("BleCentral::handle_command_service_task - command_service notification handler running")

        try:
            # Loop waiting for service notifications
            while self._connected:
                value = await self.tx_p2c_characteristic.notified()
                last_processed_command_response, last_processed_command_uid = struct.unpack("<hH", value)
                self.command_service_notification(last_processed_command_response, last_processed_command_uid)

                # Check for any commands to send to the peripheral and, if there aren't any, send a nop command
                if len(self._command_queue) > 0:
                    # Send the next command in the queue
                    command = self._command_queue.pop(0)
                    if not isinstance(command, RobotCommand):
                        raise TypeError("Expected command to be of type RobotCommand")
                    logging.info(f"BleCentral::handle_command_service_task - Sending {command}")
                    await self.rx_c2p_characteristic.write(command.get_packed_bytes())
                else:
                    # No commands queued, send a nop command
                    command = RobotCommand("nop")
                    #logging.debug("BleCentral::handle_command_service_task - No queued commands, sending nop command")
                    await self.rx_c2p_characteristic.write(command.get_packed_bytes())
                                                        
        except Exception as e:
            logging.debug("BleCentral::handle_command_service_task - Exception was flagged (Peripheral probably disappeared)")
            logging.debug(f"BleCentral::handle_command_service_task - Exception: {e}")
            self._connected = False

    async def connected_to_peripheral(self):
        """Tasks to perform when connected to a peripheral"""
        logging.debug("BleCentral::connected_to_peripheral - Connected to peripheral")

        # Command service setup
        command_service_uuid = bluetooth.UUID(0xFA20)

        try:
            command_service = await self._connection.service(command_service_uuid)
            if command_service == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral command_service is missing!")
                self._connected = False
                return
            
        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering services/characteristics")
            self._connected = False
            return

        # Command service characteristics setup
        tx_p2c_characteristic_uuid = bluetooth.UUID(0xFBA0) # Custom
        rx_c2p_characteristic_uuid = bluetooth.UUID(0xFBA1) # Custom
        try:
            self.tx_p2c_characteristic = await command_service.characteristic(tx_p2c_characteristic_uuid)
            
            if self.tx_p2c_characteristic == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral command_service tx_p2c_characteristic missing!")
                self._connected = False
                return

        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            self._connected = False
            return

        try:
            self.rx_c2p_characteristic = await command_service.characteristic(rx_c2p_characteristic_uuid)
            
            if self.rx_c2p_characteristic == None:
                logging.debug("BleCentral::connected_to_peripheral - FATAL: Peripheral command_service rx_c2p_characteristic missing!")
                self._connected = False
                return

        except asyncio.TimeoutError:
            logging.debug("BleCentral::connected_to_peripheral - FATAL: Timeout discovering characteristics")
            self._connected = False
            return

        # Subscribe to characteristic notifications
        await self.tx_p2c_characteristic.subscribe(notify = True)

        # Send a response of 12345 to the peripheral to show we are connected and ready
        await self.rx_c2p_characteristic.write(struct.pack("<L", int(BleCentral.__CONNECTION_CONFIRMATION_CODE)))

        # Generate a task for each service and then run them
        central_tasks = [
            asyncio.create_task(self.handle_command_service_task()),
        ]
        await asyncio.gather(*central_tasks)

    async def wait_for_disconnection_from_peripheral(self):
        """Wait for disconnection from the peripheral"""
        try:
            await self.flush_command_queue()
            await self._connection.disconnected(timeout_ms=2000)
            logging.info("BleCentral::wait_for_disconnection_from_peripheral - Peripheral disconnected")
        except asyncio.TimeoutError:
            logging.info("BleCentral::wait_for_disconnection_from_peripheral - Disconnection timeout")

        self._connection = None
        self._connected = False

    async def ble_central_task(self):
        """Main BLE central task"""
        logging.debug("BleCentral::ble_central_task - Task started")

        while True:
            await self.connect_to_peripheral()

            if self._connected:
                await self.connected_to_peripheral()
                await self.wait_for_disconnection_from_peripheral()

    async def queue_command(self, command: RobotCommand):
        """Queue a command to be sent to the peripheral"""
        self._command_queue.append(command)

    async def flush_command_queue(self):
        """Clear the command queue"""
        self._command_queue = []

    async def wait_for_command_complete(self, command: RobotCommand) -> int:
        """Wait for the command with the specified UID to be processed
        Returns 0 on success, 1 on timeout and 2 on peripheral disconnect"""
        sleep_time_ms = 100
        timeout_ms = 1000 * 60 * 2 # 2 minutes until timeout reported
        current_wait_duration_ms = 0
        while self._last_processed_command_uid < command.command_uid and self._connected == True and current_wait_duration_ms < timeout_ms:
            await asyncio.sleep_ms(sleep_time_ms)
            current_wait_duration_ms += sleep_time_ms

        # Timeout?
        # Note: Since the command connection is polled a timeout is very unlikely but captured here
        # just in case.  Unless there are bugs the BLE should disconnect before this timeout is reached.
        if current_wait_duration_ms >= timeout_ms:
            return 1
        
        # Disconnected?
        if not self._connected:
            return 2
        
        # Successful
        return 0

if __name__ == "__main__":
    from main import main
    main()