#************************************************************************ 
#
#   vt2_mode.py
#
#   Valiant Turtle 2 Communicator mode
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

import logging

from machine import UART

from leds import Leds
from parallel_port import ParallelPort
from ble_central import BleCentral
from eeprom import Eeprom
from configuration import Configuration
from host_comms import HostComms

import asyncio

class Vt2Mode:
    """
    Class to manage the Valiant Turtle 2 Communicator mode.

    Attributes:
        _uart (UART): UART interface for communication.
        _parallel (Parallel_port): Parallel port interface.
        _leds (Leds): LED control interface.
        _eeprom (Eeprom): EEPROM interface for persistent storage.
        ble_central (Ble_central): BLE central interface.
    """

    def __init__(self, uart: UART, parallel: ParallelPort, leds: Leds, eeprom: Eeprom):
        """
        Initialize the Vt2_mode class.

        Args:
            uart (UART): The UART interface for communication.
            parallel (Parallel_port): The parallel port interface.
            leds (Leds): The LED control interface.
            eeprom (Eeprom): The EEPROM interface for persistent storage.
        """
        self._uart = uart
        self._parallel = parallel
        self._leds = leds
        self._eeprom = eeprom

        # Initialise BLE central
        self.ble_central = BleCentral()

        # Initialise host communication
        self.host_comms = HostComms(uart)

        # Make the two communication objects aware of each other
        self.host_comms.ble_central = self.ble_central
        self.ble_central.host_comms = self.host_comms

        # Initialise configuration 
        self.configuration = Configuration()

        # Read the configuration from EEPROM
        if not self.configuration.unpack(self._eeprom.read(0, self.configuration.pack_size)):
            # Current EEPROM image is invalid, write the default
            self._eeprom.write(0, self.configuration.pack())

    # Async task to update status LEDs depending on various states and times
    async def status_led_task(self):
        interval = 0
        self._leds.set_fade_speed(0, 25) # Green
        self._leds.set_fade_speed(1, 25) # Blue

        while True:
            # interval 0 =    0
            # interval 1 =  250
            # interval 2 =  500
            # interval 3 =  750
            # interval 4 = 1000
            # interval 5 = 1250

            # Power LED
            if interval == 0: self._leds.set_brightness(0, 255)
            if interval == 5: self._leds.set_brightness(0, 255)

            # Bluetooth status LED
            if self.ble_central.is_peripheral_connected:
                # Stay on when connected
                if interval == 0: self._leds.set_brightness(1, 255)
            else:
                # Flash quickly when disconnected
                if interval == 0: self._leds.set_brightness(1, 255)
                if interval == 1: self._leds.set_brightness(1, 0)
                if interval == 2: self._leds.set_brightness(1, 255)
                if interval == 3: self._leds.set_brightness(1, 0)
                if interval == 4: self._leds.set_brightness(1, 255)
                if interval == 5: self._leds.set_brightness(1, 0)

            # Increment interval
            interval += 1
            if interval == 6: interval = 0

            # Wait before next interval
            await asyncio.sleep_ms(250)

    # Async I/O task generation and launch
    async def aio_process(self):
        # Share the events between the host and BLE objects
        self.ble_central.host_event = self.host_comms.host_event
        self.host_comms.ble_command_service_event = self.ble_central.ble_command_service_event
        self.host_comms.ble_battery_service_event = self.ble_central.ble_battery_service_event

        tasks = [
            # General background tasks
            asyncio.create_task(self.status_led_task()),

            # Communication tasks
            asyncio.create_task(self.ble_central.ble_central_task()), # BLE
            asyncio.create_task(self.host_comms.host_task()), # Serial host
        ]
        await asyncio.gather(*tasks)

    # Method to kick-off async process
    def process(self):
        logging.info("Vt2Mode::process - Launching asynchronous tasks...")
        asyncio.run(self.aio_process())

if __name__ == "__main__":
    from main import main
    main()