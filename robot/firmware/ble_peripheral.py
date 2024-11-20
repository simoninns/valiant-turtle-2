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

import logging

from machine import Pin, unique_id
from micropython import const

import aioble
import bluetooth
import asyncio
import data_encode
from robot_comms import StatusBitFlag, RobotCommand

class BlePeripheral:
    MANUFACTURER_DATA = (0xFFE1, b"www.waitingforfriday.com")
    CONNECTION_CONFIRMATION_CODE = 12345
    ADVERTISING_NAME = "vt2-robot"

    def __init__(self):
        # Get the local device's Unique ID (used as the serial number)
        self.__uid = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*unique_id())

        # Connection to central
        self.__connection = None

        # Flag to show connected status
        self.__connected = False

        # Advertising definitions
        self.__ble_advertising_definitions()

        # Service definitions
        self.__ble_service_command_definitions()
        self.__ble_service_power_definition()

        # Register services with aioBLE library
        aioble.register_services(self.command_service, self.power_service)

    def __ble_advertising_definitions(self):
        # Definitions used for advertising via BLE

        # Set our advertising UUID
        self.peripheral_advertising_uuid = bluetooth.UUID(0xF910)

        # Set our appearance to "Remote Control"
        self.peripheral_appearance_generic_remote_control = const(0x0180)
        self.peripheral_manufacturer = BlePeripheral.MANUFACTURER_DATA
        self.peripheral_advertising_name = BlePeripheral.ADVERTISING_NAME

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

    # Define a service - power information
    def __ble_service_power_definition(self):
        power_service_uuid = bluetooth.UUID(0x180F) # Battery service
        power_voltage_characteristic_uuid = bluetooth.UUID(0xFB10) # Custom
        power_current_characteristic_uuid = bluetooth.UUID(0xFB11) # Custom
        power_watts_characteristic_uuid = bluetooth.UUID(0xFB12) # Custom

        self.power_service = aioble.Service(power_service_uuid)

        self.power_voltage_characteristic = aioble.Characteristic(self.power_service, power_voltage_characteristic_uuid, read=True, notify=True)
        self.power_current_characteristic = aioble.Characteristic(self.power_service, power_current_characteristic_uuid, read=True, notify=False)
        self.power_watts_characteristic = aioble.Characteristic(self.power_service, power_watts_characteristic_uuid, read=True, notify=False)

    # Property that is true when central (VT2 Communicator) is connected
    @property
    def is_central_connected(self) -> bool:
        return self.__connected

    async def wait_for_data(self, characteristic, t_ms=5000):
        try:
            _, data = await characteristic.written(timeout_ms=t_ms)
            return data
        except asyncio.TimeoutError:
            logging.debug("BlePeripheral::wait_for_data - Data timed-out - (Central probably disappeared)")
            self.__connected = False
            return None

    # Send power service characteristics update
    def power_service_update(self, voltage, current, power):
        if self.__connected and self.__connection:
            logging.debug(f"BlePeripheral::power_service_update - mV = {voltage} / mA = {current} / mW = {power}")
            try:
                self.power_voltage_characteristic.notify(self.__connection, data_encode.to_float(voltage))
                self.power_current_characteristic.write(data_encode.to_float(current))
                self.power_watts_characteristic.write(data_encode.to_float(power))
            
            except Exception as e:
                logging.debug("BlePeripheral::power_service_update - Exception was flagged (Central probably disappeared)")
                self.__connected = False
    
    # Send command service characteristics update
    def command_service_update(self, status_bit_flag: StatusBitFlag):
        if self.__connected and self.__connection:
            #logging.debug(f"BlePeripheral::command_service_update - Status Bit Flags = {status_bit_flag.display_flags()}")
            try:
                # Send from p2c
                self.tx_p2c_characteristic.notify(self.__connection, data_encode.to_uint32(status_bit_flag.flags))
                
            except Exception as e:
                logging.debug("BlePeripheral::command_service_update - Exception was flagged (Central probably disappeared)")
                self.__connected = False

    # Here we send the status flags to the central which 
    # will then send a response back to us.  This is because
    # only the peripheral can initiate a notification to the central
    async def command_service_update_task(self):
        status_bit_flag = StatusBitFlag()
        status_bit_flag.flags = 70000
        while self.__connected:
            self.command_service_update(status_bit_flag)
            status_bit_flag.flags += 1
            if status_bit_flag.flags == 256: status_bit_flag.flags = 0

            # Command service update time out can cause disconnection - only wait for reply if still connected...
            if self.__connected:
                # Receive from c2p
                command_data = await self.wait_for_data(self.rx_c2p_characteristic)
                if command_data != None:
                    if len(command_data) != 20:
                        logging.debug("BlePeripheral::command_service_update_task - Invalid reply data length")
                        self.__connected = False
                        continue
                    else:
                        # Process the command contained in the reply
                        command = RobotCommand.from_packed_bytes(command_data)
                    if command.command_id != 0: logging.debug(f"BlePeripheral::command_service_update_task - Command received = {command}")

            if self.__connected: await asyncio.sleep_ms(250)

    # Tasks to run whilst connected to central  
    async def connected_to_central(self):
        # Generate a task for each service and then run them
        peripheral_tasks = [
            asyncio.create_task(self.command_service_update_task()),
        ]
        logging.info("BlePeripheral::connected_to_central - Running connected tasks")
        await asyncio.gather(*peripheral_tasks)

    async def wait_for_disconnection_from_central(self):
        await self.__connection.disconnected()
        self.__connected = False
        self.__connection = None
        logging.info("BlePeripheral::wait_for_disconnection_from_central - Central disconnected")

    # Advertise peripheral to central
    async def advertise_to_central(self):
        # BLE Advertising frequency
        ble_advertising_frequency_us = const(250000)

        # Wait for something to connect
        logging.debug("BlePeripheral::advertise_to_central - Advertising and waiting for connection from central...")
        self.__connection = await aioble.advertise(
            ble_advertising_frequency_us,
            name=self.peripheral_advertising_name,
            services=[self.peripheral_advertising_uuid],
            appearance=self.peripheral_appearance_generic_remote_control,
            manufacturer=self.peripheral_manufacturer,
        )
        logging.info(f"BlePeripheral::advertise_to_central - Central with address {self.__connection.device.addr_hex()} has connected - advertising stopped")

        # It takes a while for the central to really connect.  So, to avoid data dropping into a black hole
        # the central will start by sending us a byte of data.  Once received, we can mark it as connected for real
        logging.debug("BlePeripheral::advertise_to_central - Waiting for central to confirm connection...")
        reply_data = await self.wait_for_data(self.rx_c2p_characteristic)
        if reply_data != None:
            if data_encode.from_int16(reply_data) == BlePeripheral.CONNECTION_CONFIRMATION_CODE:
                logging.debug("BlePeripheral::advertise_to_central - Central has confirmed as connected")
                self.__connected = True
            else:
                logging.debug("BlePeripheral::advertise_to_central - Central did not respond with 12345 - Reverting to disconnected state")
                self.__connected = False
        else:
            logging.debug("BlePeripheral::advertise_to_central - Central did not respond - Reverting to disconnected state")
            self.__connected = False

    # Main BLE peripheral task
    async def ble_peripheral_task(self):
        logging.debug("BlePeripheral::ble_peripheral_task - Task started")
        while True:
            await self.advertise_to_central()

            if self.__connected:
                await self.connected_to_central()
                await self.wait_for_disconnection_from_central()

if __name__ == "__main__":
    from main import main
    main()