#************************************************************************ 
#
#   host_comms.py
#
#   Host communication
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
import asyncio
from command_shell import CommandShell

class HostComms:
    """Class to manage host communication tasks"""
    def __init__(self, uart: UART):
        self._uart = uart
        self._ble_central = None
        self._ble_command_service_event = None
        self._ble_power_service_event = None
        self._host_event = asyncio.Event()

        # Create a command shell
        cli_prompt="VT2> "
        cli_intro="\r\nWelcome to the Valiant Turtle 2 Communicator\r\nType your commands below. Type 'help' for help."
        self.command_shell = CommandShell(self._uart, prompt=cli_prompt, intro=cli_intro, history_limit=10)

    @property
    def ble_central(self):
        return self._ble_central
    
    @ble_central.setter
    def ble_central(self, value):
        self._ble_central = value

    @property
    def ble_command_service_event(self):
        return self._ble_command_service_event

    @ble_command_service_event.setter
    def ble_command_service_event(self, value: asyncio.Event):
        self._ble_command_service_event = value

    @property
    def ble_power_service_event(self):
        return self._ble_power_service_event

    @ble_power_service_event.setter
    def ble_power_service_event(self, value: asyncio.Event):
        self._ble_power_service_event = value

    @property
    def host_event(self):
        return self._host_event

    async def ble_command_service_listener(self):
        logging.debug("HostComms::ble_event_listener_task - Task started")

        while True:
            # Check if BLE central is available
            if self._ble_central != None and self.ble_command_service_event != None:
                await self.ble_command_service_event.wait()
                self.command_shell.command_status = self._ble_central.get_command_service_response()
            else:
                await asyncio.sleep_ms(250)

    async def ble_power_service_listener(self):
        logging.debug("HostComms::ble_power_service_listener - Task started")

        while True:
            # Check if BLE central is available
            if self._ble_central != None and self.ble_power_service_event != None:
                await self.ble_power_service_event.wait()
                self.command_shell.power_monitor = self._ble_central.get_power_service_response()
            else:
                await asyncio.sleep_ms(250)

    async def cli_task(self):
        logging.debug("HostComms::cli_task - Task started")
        
        # Run the command shell
        while True:
            await self.command_shell.run_shell()

    async def host_task(self):
        logging.debug("HostComms::host_task - Starting async host communication tasks")

        tasks = [
            # Host communication CLI task
            asyncio.create_task(self.cli_task()),

            # Event listener tasks
            asyncio.create_task(self.ble_command_service_listener()),
            asyncio.create_task(self.ble_power_service_listener()),
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    from main import main
    main()