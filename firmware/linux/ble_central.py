#************************************************************************ 
#
#   ble_central.py
#
#   BLE Central role (BLEak library)
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

import library.picolog as picolog
import asyncio
import struct

from bleak import BleakScanner, BleakClient
from bleak.uuids import normalize_uuid_16
from bleak.backends.characteristic import BleakGATTCharacteristic

from library.robot_comms import RobotCommand

class BleCentral:
    __CONNECTION_CONFIRMATION_CODE = 12345
    __ADVERTISING_NAME = "vt2-robot"

    # def __init__(self):
    #     """Class to manage BLE central tasks"""
    #     # Flags to show connected status
    #     self._connected = False
    #     self._connection = None

    #     # asyncio events
    #     self._ble_command_service_event = asyncio.Event()
    #     self._host_event = None
    #     self._host_comms = None

    #     # Get the local device's Unique ID
    #     self.uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

    #     # Remote device advertising definitions
    #     self.peripheral_advertising_uuid = bluetooth.UUID(0xF910) 
    #     self.peripheral_advertising_name = BleCentral.__ADVERTISING_NAME

    #     # Queue for commands to be sent to the peripheral
    #     self._command_queue = []
    #     self._last_processed_command_uid = 0
    #     self._last_processed_command_response = 0

    __CONNECTION_CONFIRMATION_CODE = 12345
    __ADVERTISING_NAME = "vt2-robot"
    __ADVERTISING_UUID = 0xF910

    def __init__(self):
        # Remote device advertising definitions
        self._peripheral_advertising_uuid = BleCentral.__ADVERTISING_UUID
        self._peripheral_advertising_name = BleCentral.__ADVERTISING_NAME

        # Command service characteristics setup
        self._tx_p2c_characteristic_uuid = normalize_uuid_16(0xFBA0)
        self._rx_c2p_characteristic_uuid = normalize_uuid_16(0xFBA1)

        # Robot details
        self._device = None
        self._client = None
        self._connected = False

        # Asyncio events
        self._ble_command_service_event = asyncio.Event()
        self._notification_event = asyncio.Event()
        self._host_event = None
        self._host_comms = None

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
 
    def command_service_notification(self, last_processed_command_response, last_processed_command_uid):
        """Process command_service notifications from the peripheral"""
        self._last_processed_command_response = last_processed_command_response
        self._last_processed_command_uid = last_processed_command_uid
        self._ble_command_service_event.set() # Flag the event

    def notification_handler(self, characteristic: BleakGATTCharacteristic, data: bytearray):
        """Handle notifications from the peripheral."""
        self._last_processed_command_response, self._last_processed_command_uid = struct.unpack("<hH", data)

        # Set the notification received event
        self._notification_event.set()

    def acknowledge_command_service_response(self):
        """Acknowledge the command_service response"""
        self._ble_command_service_event.clear()

    def get_command_response(self) -> int:
        """Get the last command response"""
        return self._last_processed_command_response

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
            await asyncio.sleep(sleep_time_ms / 1000)
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
    
    async def scan_for_peripheral(self):
        """Scan for a peripheral."""
        while self._device is None:
            picolog.info("BleCentral::scan_for_peripheral - Performing BLE scan for peripheral...")
            scanner = BleakScanner()
            self._device = await scanner.find_device_by_name(self._peripheral_advertising_name, timeout=5, return_adv=True)
            if self._device:
                picolog.info(f"BleCentral::scan_for_peripheral - peripheral found with address {self._device.address}.")
            else:
                picolog.info("BleCentral::scan_for_peripheral - peripheral not found.")
                await asyncio.sleep(1)

    async def connect_to_peripheral(self):
        picolog.info("BleCentral::connect_to_peripheral - Attempting to connect to peripheral...")
        try:
            async with BleakClient(self._device.address) as self._client:
                if self._client.is_connected:
                    # We should probably pair here... but bleak doesn't support pairing correctly yet
                    picolog.info("BleCentral::connect_to_peripheral - Connected to peripheral.")
                    self._connected = True

                    # Show the available services and characteristics
                    for service in self._client.services:
                        picolog.info(f"BleCentral::connect_to_peripheral - [Service] {service}")

                        for char in service.characteristics:
                            if "read" in char.properties:
                                try:
                                    value = await self._client.read_gatt_char(char.uuid)
                                    extra = f", Value: {value}"
                                except Exception as e:
                                    extra = f", Error: {e}"
                            else:
                                extra = ""

                            if "write-without-response" in char.properties:
                                extra += f", Max write w/o rsp size: {char.max_write_without_response_size}"

                            picolog.info(f"BleCentral::connect_to_peripheral -   [Characteristic] {char} ({','.join(char.properties)}){extra}")

                            for descriptor in char.descriptors:
                                try:
                                    value = await self._client.read_gatt_descriptor(descriptor.handle)
                                    picolog.info(f"BleCentral::connect_to_peripheral -     [Descriptor] {descriptor}, Value: {value}")
                                except Exception as e:
                                    picolog.error(f"BleCentral::connect_to_peripheral -     [Descriptor] {descriptor}, Error: {e}")

                # Send the connection confirmation code to the peripheral on rx_c2p_characteristic
                await self._client.write_gatt_char(self._rx_c2p_characteristic_uuid, struct.pack("<L", int(BleCentral.__CONNECTION_CONFIRMATION_CODE)), response=False)

                # Subscribe to notifications on the tx_p2c_characteristic
                await self._client.start_notify(self._tx_p2c_characteristic_uuid, self.notification_handler)

                # We are connected, wait for disconnection
                while self._client.is_connected:
                    # Wait for a notification to be received
                    await self._notification_event.wait()
                    #picolog.info("BleCentral::connect_to_peripheral - Got notification event")

                    # Check for any commands to send to the peripheral and, if there aren't any, send a nop command
                    if len(self._command_queue) > 0:
                        # Send the next command in the queue
                        command = self._command_queue.pop(0)
                        if not isinstance(command, RobotCommand):
                            raise TypeError("Expected command to be of type RobotCommand")
                        picolog.info(f"BleCentral::connect_to_peripheral - Sending {command}")
                        await self._client.write_gatt_char(self._rx_c2p_characteristic_uuid, command.get_packed_bytes(), response=False)
                    else:
                        # No commands queued, send a nop command
                        command = RobotCommand("nop")
                        #picolog.info("BleCentral::connect_to_peripheral - No queued commands, sending nop command")
                        await self._client.write_gatt_char(self._rx_c2p_characteristic_uuid, command.get_packed_bytes(), response=False)

                    # Clear the notification event
                    self._notification_event.clear()
                picolog.info("BleCentral::connect_to_peripheral - Client has disconnected.")
                self._connected = False

                # Unsubscribe from notifications on the tx_p2c_characteristic
                await self._client.stop_notify(self._tx_p2c_characteristic_uuid)
        except Exception as e:
            picolog.info(f"{e}")

    async def disconnect_from_peripheral(self):
        picolog.info("BleCentral::disconnect_from_peripheral - Disconnecting from peripheral...")
        pass

    async def ble_central_tasks(self):
        """Task to scan for a peripheral, connect to it, communicate with it, and disconnect from it."""
        while True:
            await self.scan_for_peripheral()
            await self.connect_to_peripheral()
            await self.disconnect_from_peripheral()
            await asyncio.sleep(1)

if __name__ == "__main__":
    from main import main
    main()