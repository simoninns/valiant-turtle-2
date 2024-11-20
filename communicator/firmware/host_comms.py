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
from robot_comms import PowerMonitor, StatusBitFlag

class HostComms:
    """Class to manage host communication tasks"""
    def __init__(self, uart: UART):
        self._uart = uart
        self._ble_central = None
        self._ble_command_service_event = None
        self._ble_power_service_event = None
        self._host_event = asyncio.Event()

        # Properties used by commands
        self._power_monitor = PowerMonitor(0,0,0)
        self._command_status = StatusBitFlag()

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
                self._command_status.flags = self._ble_central.get_command_service_response()
            else:
                await asyncio.sleep_ms(250)

    async def ble_power_service_listener(self):
        logging.debug("HostComms::ble_power_service_listener - Task started")

        while True:
            # Check if BLE central is available
            if self._ble_central != None and self.ble_power_service_event != None:
                await self.ble_power_service_event.wait()
                self._power_monitor = self._ble_central.get_power_service_response()
            else:
                await asyncio.sleep_ms(250)

    async def cli_task(self):
        logging.debug("HostComms::cli_task - Task started")
        await self.command_shell.start_shell()
        
        # Get commands and then process them
        while True:
            command, parameters = await self.command_shell.get_command()
            if command: await self.process_command(command, parameters)

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

    async def process_command(self, command, parameters):
        logging.debug(f"HostComms::process_command - Processing command {command} with parameters {parameters}")
        command_handled = False

        # Handle the commands
        if command == 'help':
            # Display the help text
            await self.command_shell.send_response("Help:")
            await self.command_shell.send_response("  help                        - show this help text")
            await self.command_shell.send_response("  forwards <distance in mm>   - move forwards")
            await self.command_shell.send_response("  backwards <distance in mm>  - move backwards")
            await self.command_shell.send_response("  left <rotation in degrees>  - turn left")
            await self.command_shell.send_response("  right <rotation in degress> - turn right")
            await self.command_shell.send_response("  status                      - show the robot's current status")
            await self.command_shell.send_response("  penup                       - lift the pen")
            await self.command_shell.send_response("  pendown                     - lower the pen")
            await self.command_shell.send_response("  power                       - show the power monitor status")
            command_handled = True

        if command == 'power':
            # Display the power monitor status
            await self.command_shell.send_response(f"   Supply voltage: {self._power_monitor.voltage_V_fstring}")
            await self.command_shell.send_response(f"     Current draw: {self._power_monitor.current_mA_fstring}")
            await self.command_shell.send_response(f"Power consumption: {self._power_monitor.power_mW_fstring}")
            command_handled = True

        if command == 'status':
            # Display the robot status
            await self.command_shell.send_response("Status:")
            if self._command_status.result:
                await self.command_shell.send_response("           Last command: Success")
            else:
                await self.command_shell.send_response("           Last command: Failure")

            if self._command_status.left_motor_busy:
                await self.command_shell.send_response("             Left motor: Busy")
            else:
                await self.command_shell.send_response("             Left motor: Idle")

            if self._command_status.right_motor_busy:
                await self.command_shell.send_response("            Right motor: Busy")
            else:
                await self.command_shell.send_response("            Right motor: Idle")

            if self._command_status.left_motor_direction:
                await self.command_shell.send_response("   Left motor direction: Forwards")
            else:
                await self.command_shell.send_response("   Left motor direction: Backwards")

            if self._command_status.right_motor_direction:
                await self.command_shell.send_response("  Right motor direction: Forwards")
            else:
                await self.command_shell.send_response("  Right motor direction: Backwards")

            if self._command_status.motor_power_enabled:
                await self.command_shell.send_response("            Motor power: Enabled")
            else:
                await self.command_shell.send_response("            Motor power: Disabled")

            if self._command_status.pen_servo_on:
                if self._command_status.pen_servo_up:
                    await self.command_shell.send_response("              Pen servo: Up")
                else:
                    await self.command_shell.send_response("              Pen servo: Down")
            else: await self.command_shell.send_response("              Pen servo: Off")

            command_handled = True

        # Was the command handled?
        if not command_handled:
            await self.command_shell.send_response(f"Unknown command ignored: {command}")

if __name__ == "__main__":
    from main import main
    main()