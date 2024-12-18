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

import dlogging as dlogging

from ble_central import BleCentral
from host_comms import HostComms

import asyncio

class Vt2Mode:
    """
    Class to manage the Valiant Turtle 2 Communicator mode.
    """

    def __init__(self):
        """
        Initialize the Vt2_mode class.
        """

        # Initialise BLE central
        self.ble_central = BleCentral()

        # Initialise host communication
        self.host_comms = HostComms()

        # Make the two communication objects aware of each other
        self.host_comms.ble_central = self.ble_central
        self.ble_central.host_comms = self.host_comms

    # Async I/O task generation and launch
    async def aio_process(self):
        # Share the events between the host and BLE objects
        self.ble_central.host_event = self.host_comms.host_event
        self.host_comms.ble_command_service_event = self.ble_central.ble_command_service_event

        tasks = [
            # Communication tasks
            asyncio.create_task(self.ble_central.ble_central_tasks()), # BLE
            asyncio.create_task(self.host_comms.host_task()), # Serial host
        ]
        await asyncio.gather(*tasks)

    # Method to kick-off async process
    def process(self):
        dlogging.info("Vt2Mode::process - Running VT2 mode asynchronous tasks")
        asyncio.run(self.aio_process())

if __name__ == "__main__":
    from main import main
    main()