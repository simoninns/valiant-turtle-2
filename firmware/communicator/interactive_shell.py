#************************************************************************ 
#
#   interactive_shell.py
#
#   A simple UART interactive command shell using asyncio streams
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
import library.picolog as picolog
from machine import UART

class InteractiveShell:
    def __init__(self, reader:  asyncio.StreamReader, writer: asyncio.StreamWriter, prompt: str = ">", intro: str = None, 
                 history_limit: int = 10) -> None:
        """A simple command shell using asyncio streams"""
        self.reader = reader
        self.writer = writer
        self.prompt = prompt
        self.intro = intro
        self.history = []
        self.history_index = None
        self.current_input = ""
        self.history_limit = history_limit
        self.current_display_length = 0  # Track the length of the current command display

    async def send_response(self, message: str, command_response: int = -1) -> None:
        """Send a response back over UART."""
        try:
            if command_response == -1:
                self.writer.write(f"{message}\r\n".encode())
                await self.writer.drain()
            else:
                self.writer.write(f"{message} {command_response}\r\n".encode())
                await self.writer.drain()
        except Exception as e:
            picolog.debug(f"InteractiveShell::send_response - Failed to send response: {e}")

    async def clear_line(self) -> None:
        """Clear the current line completely."""
        try:
            self.writer.write(('\r' + ' ' * 80 + '\r').encode())
            await self.writer.drain()
        except Exception as e:
            picolog.debug(f"InteractiveShell::clear_line - Failed to clear line: {e}")

    async def move_cursor_left(self, positions: int = 1) -> None:
        """Move the cursor to the left."""
        if positions > 0:
            try:
                self.writer.write(f'\x1b[{positions}D'.encode())
                await self.writer.drain()
            except Exception as e:
                picolog.debug(f"InteractiveShell::move_cursor_left - Failed to move cursor left: {e}")

    async def move_cursor_right(self, positions: int = 1) -> None:
        """Move the cursor to the right."""
        if positions > 0:
            try:
                self.writer.write(f'\x1b[{positions}C'.encode())
                await self.writer.drain()
            except Exception as e:
                picolog.debug(f"InteractiveShell::move_cursor_right - Failed to move cursor right: {e}")

    async def display_command(self, command: str, cursor_pos: int) -> None:
        """Display the command with the cursor at the correct position."""
        await self.clear_command_line()
        try:
            self.writer.write(f"\r{self.prompt}{''.join(command)}".encode())
            await self.writer.drain()
            await self.move_cursor_left(len(command) - cursor_pos)
            self.current_display_length = len(command)  # Update current display length
        except Exception as e:
            picolog.debug(f"InteractiveShell::display_command - Failed to display command: {e}")

    async def clear_command_line(self) -> None:
        """Clear the line based on the length of the previously displayed command."""
        try:
            self.writer.write(('\r' + ' ' * self.current_display_length + '\r').encode())
            await self.writer.drain()
        except Exception as e:
            picolog.debug(f"InteractiveShell::clear_command_line - Failed to clear command line: {e}")
        self.writer.write((' ' * (len(self.prompt) + self.current_display_length)).encode())
        self.writer.write('\r'.encode())
        await self.writer.drain()

    async def read_command(self):
        """Asynchronously read and edit a command from the UART stream with arrow key support and history."""
        command = []
        cursor_pos = 0
        self.history_index = None
        self.current_input = ""
        self.writer.write(self.prompt.encode())
        await self.writer.drain()

        def is_printable(char):
            """Check if a character is printable (basic ASCII range)."""
            return 32 <= ord(char) <= 126

        while True:
            char = await self.reader.read(1)
            if not char:
                continue

            char = char.decode('utf-8')

            # Handle Enter key
            if char == '\r' or char == '\n':
                self.writer.write("\r\n".encode())
                await self.writer.drain()
                break

            # Handle backspace
            elif char == '\x08' or char == '\x7f':
                if cursor_pos > 0:
                    cursor_pos -= 1
                    command.pop(cursor_pos)
                    await self.move_cursor_left(1)
                    self.writer.write((''.join(command[cursor_pos:]) + ' ').encode())
                    await self.writer.drain()
                    await self.move_cursor_left(len(command) - cursor_pos + 1)

            # Handle escape sequences for arrow keys
            elif char == '\x1b':  # Start of escape sequence
                seq = await self.reader.read(2)
                
                # Handle left/right arrows
                if seq == b'[D':  # Left arrow
                    if cursor_pos > 0:
                        cursor_pos -= 1
                        await self.move_cursor_left(1)
                elif seq == b'[C':  # Right arrow
                    if cursor_pos < len(command):
                        cursor_pos += 1
                        await self.move_cursor_right(1)

                # Handle up/down arrows for command history
                elif seq == b'[A':  # Up arrow
                    if self.history and (self.history_index is None or self.history_index > 0):
                        if self.history_index is None:
                            self.current_input = ''.join(command)
                        self.history_index = len(self.history) - 1 if self.history_index is None else self.history_index - 1
                        command = list(self.history[self.history_index])
                        cursor_pos = len(command)
                        await self.display_command(command, cursor_pos)
                elif seq == b'[B':  # Down arrow
                    if self.history_index is not None:
                        self.history_index += 1
                        if self.history_index >= len(self.history):
                            self.history_index = None
                            command = list(self.current_input)
                        else:
                            command = list(self.history[self.history_index])
                        cursor_pos = len(command)
                        await self.display_command(command, cursor_pos)

            # Handle printable characters
            elif is_printable(char):
                command.insert(cursor_pos, char)
                cursor_pos += 1
                self.writer.write(char.encode())
                self.writer.write(''.join(command[cursor_pos:]).encode())
                await self.writer.drain()
                await self.move_cursor_left(len(command) - cursor_pos)
                self.current_display_length = len(command)

        return ''.join(command).strip()

    def parse_command(self, input_line):
        """Parse the input line into a command and its parameters."""
        parts = input_line.split()
        if not parts:
            return None, []
        command = parts[0].lower()
        parameters = parts[1:]
        return command, parameters

    def add_to_history(self, command):
        """Add a command to the history with a limit."""
        if len(self.history) >= self.history_limit:
            self.history.pop(0)
        self.history.append(command)

    async def start_shell(self):
        """Perform the initial setup and start of the shell"""
        if self.intro:
            await self.send_response(self.intro)

        picolog.debug("InteractiveShell::start_shell - Host shell started")

    async def get_command(self):
        """Get a command from the user and return it"""
        try:
            command = None
            parameters = None
            while not command:
                input_line = await self.read_command()

                if input_line:
                    if input_line.strip():
                        self.add_to_history(input_line)

                    # Parse the command (into lower case) and parameters (into a list)
                    command, parameters = self.parse_command(input_line)
                        
        except Exception as e:
            await self.send_response(f"Error: {e}")
            picolog.debug(f"InteractiveShell::get_command - Error: {e}")

        return command, parameters

if __name__ == "__main__":
    from main import main
    main()