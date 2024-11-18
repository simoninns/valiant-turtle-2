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
from command_shell import Command_shell

class Host_comms:
    def __init__(self, uart: UART):
        self._uart = uart
        self._ble_central = None
        self._ble_event = None
        self._host_event = asyncio.Event()

    @property
    def ble_central(self):
        return self._ble_central
    
    @ble_central.setter
    def ble_central(self, value):
        self._ble_central = value

    @property
    def ble_event(self):
        return self._ble_event

    @ble_event.setter
    def ble_event(self, value: asyncio.Event):
        self._ble_event = value

    @property
    def host_event(self):
        return self._host_event

    async def rx_task(self):
        logging.debug("Host_comms::rx_task - Task started")
        # Add stream reader to Rx buffer
        serial_reader = asyncio.StreamReader(self._uart)

        while True:
            data = await serial_reader.read(128)
            logging.debug("Host_comms::rx_task - Serial Rx =", list(data))

    async def tx_task(self):
        logging.debug("Host_comms::tx_task - Task started")
        # Add stream writer to Tx buffer
        serial_writer = asyncio.StreamWriter(self._uart)

        while True:
            if self.ble_event != None and self._ble_central != None:
                await self.ble_event.wait()
                data = self._ble_central.get_command_response()
                serial_writer.write(str(data)) # Note: str is just for testing - should be raw byte value
                logging.debug("Host_comms::tx_task - Serial Tx =", str(data))
                await serial_writer.drain()
            else:
                # No event or BLE object attached - just pause and loop
                await asyncio.sleep_ms(250)

    async def cli_task(self):
        cli_prompt="VT2>"
        cli_intro="\r\nWelcome to Valiant Turtle 2 Communicator!\r\nType your commands below. Type 'exit' to quit."
        command_shell = Command_shell(self._uart, prompt=cli_prompt, intro=cli_intro, history_limit=10)

        # Gather a command terminated with <CR>
        while True:
            await command_shell.run_shell()

    async def host_task(self):
        logging.debug("Host_comms::host_task - Starting async host communication tasks")

        tasks = [
            # Communication tasks
            #asyncio.create_task(self.tx_task()),
            #asyncio.create_task(self.rx_task()),
            asyncio.create_task(self.cli_task()),
        ]
        await asyncio.gather(*tasks)