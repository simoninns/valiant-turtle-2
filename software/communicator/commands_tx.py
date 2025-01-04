#************************************************************************ 
#
#   commands_tx.py
#
#   Command Tx handling
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
import picolog
import struct
from ble_central import BleCentral

# Note: The commands are defined in the BLE peripheral firmware
# and the ControlRx class must match the ControlTx class otherwise
# bad things will happen :)

class CommandsTx:
    def __init__(self, ble_central: BleCentral):
        self._ble_central = ble_central
        self._command_sequence = 1

        self._short_timeout = 5.0
        self._long_timeout = 60.0

    def __next_seq(self) -> int:
        self._command_sequence += 1
        if self._command_sequence > 255:
            self._command_sequence = 1
        return self._command_sequence
    
    async def __wait_for_command_response(self, seq_id: int):
        while True:
            await self._ble_central._p2c_queue_event.wait()
            try:
                data = self._ble_central._p2c_queue.pop(0)
            except IndexError:
                picolog.error("CommandsTx::_wait_for_command_response - Got P2C queue event but the queue was empty?")
                seq_id_rx = 0
                return None

            self._ble_central._p2c_queue_event.clear()
            seq_id_rx = data[0]

            # Check if the sequence ID matches
            if seq_id_rx == seq_id:
                #picolog.info(f"CommandsTx::_wait_for_command_response - Sequence ID = {seq_id_rx} matched")
                return data
            else:
                picolog.info(f"CommandsTx::_wait_for_command_response - Sequence ID = {seq_id_rx} did not match received sequence ID = {seq_id}")

    @property
    def connected(self):
        return self._ble_central.connected
    
    # Asynchronous methods to send commands to the BLE peripheral -----------------------------------------------------

    async def motors(self, enable: bool) -> bool:
        if not self._ble_central.connected:
            picolog.info("CommandsTx::motors - Not connected to a robot")
            return False
        
        command_id = 1

        # Command to enable or disable the motors
        if enable:
            parameter = 1
        else:
            parameter = 0

        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBB", seq_id, command_id, parameter)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::motors - Command ID = {command_id}, Sequence ID = {seq_id}, enable = {enable}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::motors - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True

    async def forward(self, distance_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::forward - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 2

        # Command to move the robot forward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::forward - Command ID = {command_id}, Sequence ID = {seq_id}, distance = {distance_mm}")

        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::forward - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::forward - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::forward - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def backward(self, distance_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::backward - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 3

        # Command to move the robot backward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::backward - Command ID = {command_id}, Sequence ID = {seq_id}, distance = {distance_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::backward - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::backward - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::backward - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def left(self, angle_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::left - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 4

        # Command to turn the robot left
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::left - Command ID = {command_id}, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::left - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::left - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::left - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def right(self, angle_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::right - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 5

        # Command to turn the robot right
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::right - Command ID = {command_id}, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::right - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::right - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::right - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def circle(self, radius_mm: float, extent_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::circle - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 6

        # Command to turn the robot left on an arc
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, command_id, radius_mm, extent_degrees)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::circle - Command ID = {command_id}, Sequence ID = {seq_id}, radius = {radius_mm}, extent = {extent_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::circle - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::circle - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::circle - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading

    async def setheading(self, angle_degrees: float) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::setheading - Not connected to a robot")
            return False
        
        command_id = 7

        # Command to set the robot heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::setheading - Command ID = {command_id}, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::setheading - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def setx(self, x_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::setx - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 8

        # Command to set the robot X position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, x_mm)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::setx - Command ID = {command_id}, Sequence ID = {seq_id}, x = {x_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::setx - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::setx - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::setx - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def sety(self, y_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::sety - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 9

        # Command to set the robot Y position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::sety - Command ID = {command_id}, Sequence ID = {seq_id}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::sety - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::sety - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::sety - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def goto(self, x_mm: float, y_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::setposition - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 10

        # Command to set the robot position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, command_id, x_mm, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::setposition - Command ID = {command_id}, Sequence ID = {seq_id}, x = {x_mm}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::setposition - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::setposition - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::setposition - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def towards(self, x_mm: float, y_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::towards - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 11

        # Command to move the robot towards a point
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, command_id, x_mm, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::towards - Command ID = {command_id}, Sequence ID = {seq_id}, x = {x_mm}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::towards - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::towards - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::towards - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def reset_origin(self) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::reset_origin - Not connected to a robot")
            return False
        
        command_id = 12

        # Command to reset the x,y origin and heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::reset_origin - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::reset_origin - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def heading(self) -> tuple[bool, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::heading - Not connected to a robot")
            return False, 0.0
        
        command_id = 13

        # Command to get the robot heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::heading - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::heading - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0

        # Extract the heading from the response
        try:
            seq_id, heading = struct.unpack("<Bf", response[:5])
        except ValueError as e:
            picolog.error(f"CommandsTx::heading - Error unpacking response: {e}")
            return False, 0.0
        
        heading = round(heading, 2)
        picolog.info(f"CommandsTx::heading - Heading = {heading}")
        return True, heading
    
    async def position(self) -> tuple[bool, float, float]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::position - Not connected to a robot")
            return False, 0.0, 0.0
        
        command_id = 14

        # Command to get the robot position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::position - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::position - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0

        # Extract the position from the response
        try:
            seq_id, x, y = struct.unpack("<Bff", response[:9])
        except ValueError as e:
            picolog.error(f"CommandsTx::position - Error unpacking response: {e}")
            return False, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        picolog.info(f"CommandsTx::position - X = {x}, Y = {y}")
        return True, x, y
    
    async def penup(self) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::penup - Not connected to a robot")
            return False
        
        command_id = 15

        # Command to raise the pen
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::penup - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::penup - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def pendown(self) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::pendown - Not connected to a robot")
            return False
        
        command_id = 16

        # Command to raise the pen
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::pendown - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::pendown - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def eyes(self, eye_id, red, green, blue) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::eyes - Not connected to a robot")
            return False
        
        command_id = 17

        # Command to set the eye colour
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBBBBB", seq_id, command_id, eye_id, red, green, blue)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::eyes - Command ID = {command_id}, Sequence ID = {seq_id}, eye_id = {eye_id}, red = {red}, green = {green}, blue = {blue}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::eyes - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def power(self) -> tuple[bool, int, int, int]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::power - Not connected to a robot")
            return False, 0, 0, 0
        
        command_id = 18

        # Command to get the robot power
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::power - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::power - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0, 0, 0

        # Extract the power from the response
        try:
            seq_id, mv, ma, mw = struct.unpack("<Blll", response[:13])
        except ValueError as e:
            picolog.error(f"CommandsTx::power - Error unpacking response: {e}")
            return False, 0, 0, 0
        picolog.info(f"CommandsTx::power - mV = {mv}, mA = {ma}, mW = {mw}")
        return True, mv, ma, mw 
    
    async def isdown(self) -> tuple[bool, bool]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::isdown - Not connected to a robot")
            return False, False
        
        command_id = 19

        # Command to get the pen status (True = down, False = up)
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::isdown - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::isdown - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, False

        # Extract the pen status from the response
        try:
            seq_id, pen_down = struct.unpack("<BB", response[:2])
        except ValueError as e:
            picolog.error(f"CommandsTx::isdown - Error unpacking response: {e}")
            return False, False
        picolog.info(f"CommandsTx::isdown - Pen down = {pen_down}")
        return True, pen_down
    
    async def set_linear_velocity(self, target_speed: int, acceleration: int) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::set_linear_velocity - Not connected to a robot")
            return False
        
        command_id = 20

        # Command to set the linear velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBll", seq_id, command_id, target_speed, acceleration)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::set_linear_velocity - Command ID = {command_id}, Sequence ID = {seq_id}, target_speed = {target_speed}, acceleration = {acceleration}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::set_linear_velocity - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def set_rotational_velocity(self, target_speed: int, acceleration: int) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::set_rotational_velocity - Not connected to a robot")
            return False
        
        command_id = 21

        # Command to set the rotational velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBll", seq_id, command_id, target_speed, acceleration)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::set_rotational_velocity - Command ID = {command_id}, Sequence ID = {seq_id}, target_speed = {target_speed}, acceleration = {acceleration}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::set_rotational_velocity - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def get_linear_velocity(self) -> tuple[bool, int, int]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::get_linear_velocity - Not connected to a robot")
            return False, 0, 0
        
        command_id = 22

        # Command to get the linear velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::get_linear_velocity - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::get_linear_velocity - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0, 0

        # Extract the linear velocity from the response
        try:
            seq_id, target_speed, acceleration = struct.unpack("<Bll", response[:9])
        except ValueError as e:
            picolog.error(f"CommandsTx::get_linear_velocity - Error unpacking response: {e}")
            return False, 0, 0
        picolog.info(f"CommandsTx::get_linear_velocity - Target speed = {target_speed}, Acceleration = {acceleration}")
        return True, target_speed, acceleration
    
    async def get_rotational_velocity(self) -> tuple[bool, int, int]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::get_rotational_velocity - Not connected to a robot")
            return False, 0, 0
        
        command_id = 23

        # Command to get the rotational velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::get_rotational_velocity - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::get_rotational_velocity - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0, 0

        # Extract the rotational velocity from the response
        try:
            seq_id, target_speed, acceleration = struct.unpack("<Bll", response[:9])
        except ValueError as e:
            picolog.error(f"CommandsTx::get_rotational_velocity - Error unpacking response: {e}")
            return False, 0, 0
        picolog.info(f"CommandsTx::get_rotational_velocity - Target speed = {target_speed}, Acceleration = {acceleration}")
        return True, target_speed, acceleration

    async def set_wheel_diameter_calibration(self, wheel_diameter: int) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::set_wheel_diameter_calibration - Not connected to a robot")
            return False
        
        command_id = 24

        # Command to set the wheel diameter calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BBi", seq_id, command_id, wheel_diameter)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::set_wheel_diameter_calibration - Command ID = {command_id}, Sequence ID = {seq_id}, wheel_diameter = {wheel_diameter}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::set_wheel_diameter_calibration - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def set_axel_distance_calibration(self, axel_distance: int) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::set_axel_distance_calibration - Not connected to a robot")
            return False
        
        command_id = 25

        # Command to set the axel distance calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BBi", seq_id, command_id, axel_distance)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::set_axel_distance_calibration - Command ID = {command_id}, Sequence ID = {seq_id}, axel_distance = {axel_distance}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::set_axel_distance_calibration - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def get_wheel_diameter_calibration(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::get_wheel_diameter_calibration - Not connected to a robot")
            return False, 0
        
        command_id = 26

        # Command to get the wheel diameter calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::get_wheel_diameter_calibration - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::get_wheel_diameter_calibration - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0

        try:
            seq_id, cali_wheel = struct.unpack("<Bi", response[:5])
        except ValueError as e:
            picolog.error(f"CommandsTx::get_wheel_diameter_calibration - Error unpacking response: {e}")
            return False, 0
        picolog.info(f"CommandsTx::get_wheel_diameter_calibration - Calibration wheel diameter = {cali_wheel}")
        return True, cali_wheel

    async def get_axel_distance_calibration(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::get_axel_distance_calibration - Not connected to a robot")
            return False, 0
        
        command_id = 27

        # Command to get the axel distance calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::get_axel_distance_calibration - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::get_axel_distance_calibration - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0

        try:
            seq_id, cali_axel = struct.unpack("<Bi", response[:5])
        except ValueError as e:
            picolog.error(f"CommandsTx::get_axel_distance_calibration - Error unpacking response: {e}")
            return False, 0
        picolog.info(f"CommandsTx::get_axel_distance_calibration - Calibration axel distance = {cali_axel}")
        return True, cali_axel

    async def set_turtle_id(self, turtle_id: int) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::set_turtle_id - Not connected to a robot")
            return False
        
        command_id = 28

        # Command to set the turtle ID
        seq_id = self.__next_seq()
        data = struct.pack("<BBB", seq_id, command_id, turtle_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::set_turtle_id - Command ID = {command_id}, Sequence ID = {seq_id}, turtle_id = {turtle_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::set_turtle_id - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def get_turtle_id(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::get_turtle_id - Not connected to a robot")
            return False, 0
        
        command_id = 29

        # Command to get the turtle ID
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::get_turtle_id - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::get_turtle_id - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0

        try:
            seq_id, turtle_id = struct.unpack("<BB", response[:2])
        except ValueError as e:
            picolog.error(f"CommandsTx::get_turtle_id - Error unpacking response: {e}")
            return False, 0
        picolog.info(f"CommandsTx::get_turtle_id - Turtle ID = {turtle_id}")
        return True, turtle_id

    async def load_config(self) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::load_config - Not connected to a robot")
            return False
        
        command_id = 30

        # Command to load the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::load_config - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::load_config - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def save_config(self) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::save_config - Not connected to a robot")
            return False
        
        command_id = 31

        # Command to save the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::save_config - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::save_config - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def reset_config(self) -> bool:
        if not self._ble_central.connected:
            picolog.error("CommandsTx::reset_config - Not connected to a robot")
            return False
        
        command_id = 32

        # Command to reset the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        picolog.info(f"CommandsTx::reset_config - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            picolog.error(f"CommandsTx::reset_config - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True
    
if __name__ == "__main__":
    from main import main
    main()