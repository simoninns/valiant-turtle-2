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

import dlogging as dlogging
import asyncio
from interactive_shell import InteractiveShell
from host_shell import HostShell
from library.robot_comms import RobotCommand
import sys, os

class CommandResult:
    """Class to store the result of a command"""

    # Consts to make code more readable
    result_nop = (-1)
    result_ok = (0)
    result_timeout = (1)
    result_disconnected = (2)
    result_error = (3)
    result_toofew = (4)
    result_toomany = (5)
    result_invalid = (6)
    result_unknown = (7)

    _result_dictionary = {
        # Dictionary of command results:
        "nop":          (result_nop, "NOP"),                   # No operation
        "ok":           (result_ok, "OK"),                     # Command completed successfully
        "timeout":      (result_timeout, "TIMEOUT"),           # Command timed out
        "disconnected": (result_disconnected, "DISCONNECTED"), # Robot disconnected
        "error":        (result_error, "ERROR"),               # Command failed
        "toofew":       (result_toofew, "TOOFEW"),             # Too few parameters
        "toomany":      (result_toomany, "TOOMANY"),           # Too many parameters
        "invalid":      (result_invalid, "INVALID"),           # Invalid parameters
        "unknown":      (result_unknown, "UNKNOWN"),           # Unknown command
    }

    def __init__(self, resultCode: int = -1, resultDesc: str = "", response: int = -1):
        # Check if the result code is valid   
        if not any(resultCode == value[0] for value in self._result_dictionary.values()):
            raise ValueError(f"Invalid result code: {resultCode}")
        
        self._resultCode = resultCode
        self._resultDesc = resultDesc
        self._response = response

    @property
    def error_code(self) -> int:
        return self._resultCode
    
    @property
    def error_name(self) -> str:
        """Return the error name such as OK, TIMEOUT, etc."""
        for key, value in self._result_dictionary.items():
            if value[0] == self._resultCode:
                return value[1]
        return "UNKNOWN"

    @property
    def error_description(self) -> str:
        return self._resultDesc
    
    @property
    def response(self) -> int:
        return self._response
    
    @response.setter
    def response(self, response: int):
        self._response = response

class HostComms:
    """Class to manage host communication tasks"""
    def __init__(self):
        self._ble_central = None
        self._ble_command_service_event = None
        self._host_event = asyncio.Event()

        # Create an interactive command shell
        self._interactive_shell = None

        # Create a host shell
        self._host_shell = None

        # Flag to track current shell mode (interactive or host)
        self._is_shell_interactive = True

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
    def host_event(self):
        return self._host_event

    async def ble_command_service_listener(self):
        dlogging.debug("HostComms::ble_event_listener_task - Task started")

        while True:
            # Check if BLE central is available
            if self._ble_central != None and self.ble_command_service_event != None:
                await self.ble_command_service_event.wait()
                self._ble_central.acknowledge_command_service_response()
            else:
                await asyncio.sleep_ms(250)

    async def cli_task(self):
        dlogging.debug("HostComms::cli_task - Task started")

        # Create the streams
        self.reader, self.writer = await self.initialise_streams()

        # Create an interactive command shell
        cli_prompt="VT2> "
        cli_intro="\r\nWelcome to the Valiant Turtle 2 Communicator\r\nType your commands below. Type 'help' for help."
        self._interactive_shell = InteractiveShell(self.reader, self.writer, prompt=cli_prompt, intro=cli_intro, history_limit=10)

        # Create a host shell
        self._host_shell = HostShell(self.reader, self.writer)

        # Start the interactive shell
        await self._interactive_shell.start_shell()
        
        # Get commands and then process them
        while True:
            if self._is_shell_interactive:
                # Interactive shell mode (for human interaction)
                command, parameters = await self._interactive_shell.get_command()

                if command and command != "nop":
                    send_command_result = await self.send_command(command, parameters)
                    
                    if send_command_result.error_code == CommandResult.result_ok or send_command_result.error_code == CommandResult.result_nop:
                        # Just OK or NOP, so don't display any description
                        await self._interactive_shell.send_response(send_command_result.error_name, send_command_result.response)
                    else:
                        # Display the error name and description
                        await self._interactive_shell.send_response(f"{send_command_result.error_name} - {send_command_result.error_description}", send_command_result.response)
            else:
                # Host shell mode (for data-based communication)
                command, parameters, switch_mode = await self._host_shell.get_command()
                
                if switch_mode:
                    # Switch back to interactive shell mode
                    dlogging.debug("HostComms::cli_task - Switching back to interactive shell mode")
                    self._is_shell_interactive = True
                    await self._interactive_shell.start_shell()
                else:
                    # Process the command (if it's not a NOP)
                    if command != "nop":
                        send_command_result = await self.send_command(command, parameters)
                        await self._host_shell.send_response(send_command_result.error_code, send_command_result.response)
                    else:
                        dlogging.debug("HostComms::cli_task - Got NOP command - ignoring")

    async def host_task(self):
        dlogging.debug("HostComms::host_task - Starting async host communication tasks")

        tasks = [
            # Host communication CLI task
            asyncio.create_task(self.cli_task()),

            # Event listener tasks
            asyncio.create_task(self.ble_command_service_listener()),
        ]
        await asyncio.gather(*tasks)

    async def send_command(self, command, parameters) -> CommandResult:
        """Process a command from the host"""

        # Local commands (not sent to the robot) when in interactive shell mode
        if self._is_shell_interactive:
            # Display the help text (local command)
            if command == 'help':
                await self._interactive_shell.send_response("Help:")
                await self._interactive_shell.send_response("  Local commands:")
                await self._interactive_shell.send_response("    help - show this help text")
                await self._interactive_shell.send_response("    host - switch to host shell mode")
                await self._interactive_shell.send_response("")
                await self._interactive_shell.send_response("  Robot commands:")
                await self._interactive_shell.send_response(RobotCommand.help_text())
                return CommandResult(CommandResult.result_ok, "OK")
            
            # Switch to host shell mode (local command)
            # Note: This works even if the robot isn't connected
            if command == 'host':
                # Switch to host shell mode (data-based communication)
                dlogging.debug("HostComms::process_command - Switching to host shell mode")
                self._is_shell_interactive = False
                return CommandResult(CommandResult.result_ok, "OK")

            # Is the robot connected?
            if not self._ble_central.is_peripheral_connected:
                return CommandResult(CommandResult.result_disconnected, "Robot is not connected")

        # Robot commands (uses the RobotCommand class for validation)
        if RobotCommand.is_command_valid(command):
            # Does the command have the required number of parameters?
            if len(parameters) != RobotCommand.num_parameters(command):
                if (self._is_shell_interactive):
                    # In interactive shell mode we want exactly the right number of parameters always
                    if RobotCommand.num_parameters(command) == 1:
                        return CommandResult(CommandResult.result_toofew, f"Command requires {RobotCommand.num_parameters(command)} parameter")
                    elif RobotCommand.num_parameters(command) == 0:
                        return CommandResult(CommandResult.result_toomany, f"Command does not require any parameters")
                    else:
                        if (len(parameters) < RobotCommand.num_parameters(command)):
                            return CommandResult(CommandResult.result_toofew, f"Command requires {RobotCommand.num_parameters(command)} parameters")
                        else:
                            return CommandResult(CommandResult.result_toomany, f"Command requires {RobotCommand.num_parameters(command)} parameters")
                else:
                    # In host shell mode we can have any number of parameters as long as it's the minimum or more
                    if len(parameters) < RobotCommand.num_parameters(command):
                        return CommandResult(CommandResult.result_toofew, f"Command requires {RobotCommand.num_parameters(command)} parameters")
            
            # Ensure the parameters are integers
            for n in range(len(parameters)):
                try:
                    parameters[n] = int(parameters[n])
                except ValueError:
                    return CommandResult(CommandResult.result_invalid, f"Invalid parameter - {parameters[n]} must be an integer")
            
            # Range check the required parameters
            for n in range(len(parameters)):
                if not (RobotCommand.parameter_range(command, n)[0] <= parameters[n] <= RobotCommand.parameter_range(command, n)[1]):
                    dlogging.debug(f"HostComms::process_command - Got out of range parameter {parameters[n]} for command {command}")
                    return CommandResult(CommandResult.result_invalid, f"Invalid parameter - {parameters[n]} must be between {RobotCommand.parameter_range(command, n)[0]} and {RobotCommand.parameter_range(command, n)[1]}")
                
            # Queue the command
            robot_command = RobotCommand(command, parameters)
            await self.ble_central.queue_command(robot_command)
            command_result = await self.ble_central.wait_for_command_complete(robot_command)

            # Show the result of the command processing
            if command_result == 1:
                return CommandResult(CommandResult.result_timeout, "Timed out waiting for response from robot")
            elif command_result == 2:
                return CommandResult(CommandResult.result_disconnected, "Robot has disconnected")

            # Return the command result including the response from the robot
            return CommandResult(CommandResult.result_ok, "OK", self.ble_central.get_command_response())
        
        # The command was not recognised
        dlogging.debug(f"HostComms::process_command - Command [{command}] was not recognised")
        return CommandResult(CommandResult.result_unknown, f"Unknown command: {command}")
    
    async def initialise_streams(self, limit=asyncio.streams._DEFAULT_LIMIT, loop=None):
        """Initialise the asyncio connection for reader and writer."""
        if loop is None:
            loop = asyncio.get_event_loop()

        reader = asyncio.StreamReader(limit=limit, loop=loop)
        await loop.connect_read_pipe(
            lambda: asyncio.StreamReaderProtocol(reader, loop=loop), sys.stdin)

        writer_transport, writer_protocol = await loop.connect_write_pipe(
            lambda: asyncio.streams.FlowControlMixin(loop=loop),
            os.fdopen(sys.stdout.fileno(), 'wb'))
        writer = asyncio.streams.StreamWriter(
            writer_transport, writer_protocol, None, loop)
        
        return reader, writer

if __name__ == "__main__":
    from main import main
    main()