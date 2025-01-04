#************************************************************************ 
#
#   serial_comms.py
#
#   Serial to host communications
#   Valiant Turtle 2 - Communicator firmware
#   Copyright (C) 2025 Simon Inns
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
import picolog
from machine import UART
import struct
from commands_tx import CommandsTx

class SerialComms:
    def __init__(self, uart: UART, command_tx: CommandsTx):
            """A simple command shell using asyncio streams via UART"""
            self._commands_tx = command_tx

            # Use the UART stream
            self.reader = asyncio.StreamReader(uart)
            self.writer = asyncio.StreamWriter(uart)

    async def run(self):
        while True:
            command = None
            parameters = None

            try:
                while not command:
                    command_bytes = await self.__read_command_bytes()

                    if command_bytes:
                        # Parse the command and parameters (into a list)
                        valid, command_id, parameters = self.__parse_command(command_bytes)

                        # Send the command using commands_tx to the robot
                        result_code, command_response = await self.__dispatch_command(command_id, parameters)

                        # Send the response back to the host
                        await self.__send_response(result_code, command_response)
                            
            except Exception as e:
                picolog.debug(f"SerialComms::run - Error: {e}")
                return None, None, False

    async def __read_command_bytes(self) -> bytearray:
        """Read bytes from the UART until the host sends 0x0D (CR) or the command is too long"""
        command_bytes = bytearray()
        while True and len(command_bytes) < 32:
            data = await self.reader.read(1)
            if data == b'\x0D':
                break
            command_bytes.extend(data)

        picolog.debug(f"HostShell::read_command - Host mode command bytes = {command_bytes}")
        return command_bytes
    
    # Parse the command data into a command and parameters
    # Returns command_valid_flag, command_id and a list of parameters
    def __parse_command(self, command_data: bytearray) -> tuple[bool, int, list[int]]:
        # Command data must be at least 2 bytes long
        if len(command_data) < 2:
            picolog.debug(f"HostShell::parse_command - Command data was too short to be valid")
            return False, -1, []

        # The first two bytes are the command ID
        command_id = struct.unpack("<h", command_data[:2])[0]
        parameters = []

        # If there are more bytes, they are parameters
        for i in range(2, len(command_data), 2):
            if i + 1 < len(command_data):
                param = struct.unpack("<h", command_data[i:i+2])[0]
                parameters.append(param)

            if len(parameters) > 4:
                picolog.debug(f"HostShell::parse_command - Command data was too long to be valid {command_data} - {len(parameters)} parameters")
                return False, -1, []

        return True, command_id, parameters
    
    async def __dispatch_command(self, command_id: int, parameters: list[int]) -> tuple[int, int]:
        command_response = 0
        result_code = 0

        # Note: Command IDs start from 32 to avoid clashing with ASCII control characters

        # Command ID 32: Motors [0=Off, 1=On]
        # Command ID 33: Forward [mm]
        # Command ID 34: Backward [mm]
        # Command ID 35: Left [degrees]
        # Command ID 36: Right [degrees]
        # Command ID 37: Penup
        # Command ID 38: Pendown
        # Command ID 39: Eyes [red] [green] [blue]
        # Command ID 40: Is pen up?
        # Command ID 41: power_mv
        # Command ID 42: power_ma
        # Command ID 43: power_mw

        # Result codes:
        # -1: Error
        #  0: OK 

        # How will this send a negative command response?  it won't...

        if command_id == 32: # Motors
            if parameters[0] == 0:
                if not await self._commands_tx.motors(False):
                    result_code = 1
            else:
                if not await self._commands_tx.motors(True):
                    result_code = 1
        elif command_id == 33: # Forward
            success_flag,_,_,_ = await self._commands_tx.forward(parameters[0])
            if not success_flag:
                result_code = 1
        elif command_id == 34: # Backward
            success_flag,_,_,_ = await self._commands_tx.backward(parameters[0])
            if not success_flag:
                result_code = 1
        elif command_id == 35: # Left
            success_flag,_,_,_ = await self._commands_tx.left(parameters[0])
            if not success_flag:
                result_code = 1
        elif command_id == 36: # Right
            success_flag,_,_,_ = await self._commands_tx.right(parameters[0])
            if not success_flag:
                result_code = 1
        elif command_id == 37: # Penup
            if not await self._commands_tx.penup():
                result_code = 1
        elif command_id == 38: # Pendown
            if not await self._commands_tx.pendown():
                result_code = 1
        elif command_id == 39: # Eyes
            if not await self._commands_tx.eyes(parameters[0], parameters[1], parameters[2], parameters[3]):
                result_code = 1
        elif command_id == 40: # is pen up?
            success_flag, pen_state = await self._commands_tx.isdown()
            if not success_flag:
                result_code = 1
            if pen_state:
                command_response = 0 # Pen is down
            else:
                command_response = 1 # Pen is up
        elif command_id == 41: # power_mv
            success_flag, power_mv, power_ma, power_mw = await self._commands_tx.power()
            if not success_flag:
                result_code = 1
            else:
                command_response = power_mv
        elif command_id == 42: # power_ma
            success_flag, power_mv, power_ma, power_mw = await self._commands_tx.power()
            if not success_flag:
                result_code = 1
            else:
                command_response = power_ma
        elif command_id == 43: # power_mw
            success_flag, power_mv, power_ma, power_mw = await self._commands_tx.power()
            if not success_flag:
                result_code = 1
            else:
                command_response = power_mw

        return result_code, command_response
    
    async def __send_response(self, result_code: int, command_response: int) -> None:
        if not isinstance(result_code, int) or result_code < 0 or result_code > 255:
            raise ValueError("Result code must be an unsigned byte (0-255)")
        
        if not isinstance(command_response, int) or command_response < -1 or command_response > 32767:
            raise ValueError("Command response must be a signed 16-bit integer (0 to 32767)")

        response_bytes = struct.pack("<Bh", result_code, command_response)
        picolog.debug(f"HostShell::__send_response - Responding with {response_bytes}")

        try:
            self.writer.write(response_bytes)
            await self.writer.drain()
        except Exception as e:
            picolog.debug(f"HostShell::__send_response - Failed to send response: {e}")

if __name__ == "__main__":
    from main import main
    main()