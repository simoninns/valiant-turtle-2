#************************************************************************ 
#
#   host_shell.py
#
#   A simple UART command shell using asyncio streams
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

import asyncio
import library.logging as logging
from machine import UART
from library.robot_comms import RobotCommand

class HostShell:
    """
    The host shell is a simple command shell for communicating with a computer
    rather than a person. It is used to interact with hosts using a data-based
    protocol rather than a human-readable one.
    """
    def __init__(self, uart: UART, prompt: str = ">", intro: str = None, 
                    history_limit: int = 10) -> None:
            """A simple command shell using asyncio streams via UART"""
            self.reader = asyncio.StreamReader(uart)
            self.writer = asyncio.StreamWriter(uart)

    async def read_command(self) -> bytearray:
        """Read bytes from the UART until the host sends 0x0D (CR) or the command is too long"""
        command_bytes = bytearray()
        while True and len(command_bytes) < 32:
            data = await self.reader.read(1)
            if data == b'\x0D':
                break
            command_bytes.extend(data)

        logging.debug(f"HostShell::read_command - Host mode command bytes = {command_bytes}")
        return command_bytes
    
    def parse_command(self, command_data: bytearray) -> tuple:
        """Parse the command data into a command and parameters
        Returns a tuple of command, parameters and a boolean flag which is True if the
        host is requesting to switch back to interactive mode"""

        # Command data must be at least 2 bytes long
        if len(command_data) < 2:
            logging.debug(f"HostShell::parse_command - Command data was too short to be valid")
            return None, None, False

        # The first two bytes are the command ID
        command_id = int.from_bytes(command_data[:2], 'little')
        parameters = []

        # If there are more bytes, they are parameters
        for i in range(2, len(command_data), 2):
            if i + 1 < len(command_data):
                param = int.from_bytes(command_data[i:i+2], 'little')
                parameters.append(param)

            if len(parameters) > 3:
                logging.debug(f"HostShell::parse_command - Command data was too long to be valid {command_data}")
                return None, None, False

        # Check to see if this is a local command to switch back to interactive mode (host sends ii<CR> or 0x69, 0x69, 0x0D or
        # 0x49, 0x49, 0x0D (II<CR>)). This is used to switch back to interactive mode from a terminal.
        # Note: this code is used so a human can type ii<CR> from a terminal.

        # Check to see if the magic word "shell" or "SHELL" has been sent.
        # This is used to switch back to interactive mode from a terminal.
        if command_data == b'shell' or command_data == b'SHELL':
            logging.debug(f"HostShell::parse_command - Switching back to interactive mode")
            return RobotCommand(), None, True
        
        # If the host issues "HOST" or "host" when we are already in host mode, we ignore it
        # This is to prevent the host from getting confused if it sends "HOST" when we are already in host mode
        if command_data == b'host' or command_data == b'HOST':
            logging.debug(f"HostShell::parse_command - Got 'host' command when already in host mode - ignoring")
            return RobotCommand(), None, False

        # To keep this compatible with the InteractiveShell class we convert the command_id to a command string
        try:
            command = RobotCommand.id_to_command(command_id)
        except ValueError:
            logging.debug(f"HostShell::parse_command - Command ID {command_id} not recognised")
            return None, None, False

        return command, parameters, False

    async def get_command(self):
        """Get a command from the host and return it"""
        try:
            command = None
            parameters = None
            switch_mode = False
            while not command:
                command_data = await self.read_command()

                if command_data:
                    # Parse the command and parameters (into a list)
                    command, parameters, switch_mode = self.parse_command(command_data)
                        
        except Exception as e:
            logging.debug(f"HostShell::get_command - Error: {e}")
            return None, None, False

        return command, parameters, switch_mode
    
    async def send_response(self, response: int) -> None:
        """Send a one-byte response back over UART."""
        if not isinstance(response, int) or response < 0 or response > 255:
            raise ValueError("Response must be an unsigned byte (0-255)")

        response_byte = response.to_bytes(1, 'little')
        logging.debug(f"HostShell::send_response - Responding with {response_byte}")

        try:
            await self.writer.awrite(response_byte)
        except Exception as e:
            logging.debug(f"HostShell::send_response - Failed to send response: {e}")

if __name__ == "__main__":
    from main import main
    main()