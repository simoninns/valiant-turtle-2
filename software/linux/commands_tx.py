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
import logging
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
    
    async def __wait_for_command_response(self, seq_id: int) -> bytes:
        while True:
            await self._ble_central._p2c_queue_event.wait()
            try:
                data = self._ble_central._p2c_queue.pop(0)
            except IndexError:
                logging.error("CommandsTx::__wait_for_command_response - Got P2C queue event but the queue was empty?")
                seq_id_rx = 0
                return None

            self._ble_central._p2c_queue_event.clear()
            seq_id_rx = data[0]

            # Check if the sequence ID matches
            if seq_id_rx == seq_id:
                #logging.info(f"CommandsTx::__wait_for_command_response - Sequence ID = {seq_id_rx} matched")
                return data
            else:
                logging.info(f"CommandsTx::__wait_for_command_response - Sequence ID = {seq_id_rx} did not match received sequence ID = {seq_id}")

    # Command ID = 1
    async def motors(self, enable: bool) -> bool:
        if not self._ble_central.is_connected:
            logging.info("CommandsTx::motors - Not connected to a robot")
            return False

        # Command to enable or disable the motors
        if enable:
            parameter = 1
        else:
            parameter = 0

        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBB", seq_id, 1, parameter)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::motors - Command ID = 1, Sequence ID = {seq_id}, enable = {enable}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::motors - Command ID = 1, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True

    # Command ID = 2
    async def forward(self, distance_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::forward - Not connected to a robot")
            return False
        
        # Command to move the robot forward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 2, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::forward - Command ID = 2, Sequence ID = {seq_id}, distance = {distance_mm}")

        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::forward - Command ID = 2, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 3
    async def backward(self, distance_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::backward - Not connected to a robot")
            return False
        
        # Command to move the robot backward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 3, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::backward - Command ID = 3, Sequence ID = {seq_id}, distance = {distance_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::backward - Command ID = 3, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 4
    async def left(self, angle_degrees: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::left - Not connected to a robot")
            return False
        
        # Command to turn the robot left
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 4, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::left - Command ID = 4, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::left - Command ID = 4, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 5
    async def right(self, angle_degrees: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::right - Not connected to a robot")
            return False
        
        # Command to turn the robot right
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 5, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::right - Command ID = 5, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::right - Command ID = 5, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True

    # Command ID = 6
    async def heading(self, angle_degrees: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::heading - Not connected to a robot")
            return False
        
        # Command to set the robot heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 6, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::heading - Command ID = 6, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::heading - Command ID = 6, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 7
    async def position_x(self, x_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::position_x - Not connected to a robot")
            return False
        
        # Command to set the robot X position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 7, x_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::position_x - Command ID = 7, Sequence ID = {seq_id}, x = {x_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::position_x - Command ID = 7, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 8
    async def position_y(self, y_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::position_y - Not connected to a robot")
            return False
        
        # Command to set the robot Y position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 8, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::position_y - Command ID = 8, Sequence ID = {seq_id}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::position_y - Command ID = 8, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 9
    async def position(self, x_mm: float, y_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::position - Not connected to a robot")
            return False
        
        # Command to set the robot position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, 9, x_mm, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::position - Command ID = 9, Sequence ID = {seq_id}, x = {x_mm}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::position - Command ID = 9, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 10
    async def towards(self, x_mm: float, y_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::towards - Not connected to a robot")
            return False
        
        # Command to move the robot towards a point
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, 10, x_mm, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::towards - Command ID = 10, Sequence ID = {seq_id}, x = {x_mm}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::towards - Command ID = 10, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 11
    async def reset_origin(self) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::reset_origin - Not connected to a robot")
            return False
        
        # Command to reset the x,y origin and heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 11)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::reset_origin - Command ID = 11, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::reset_origin - Command ID = 11, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 12
    async def get_heading(self) -> tuple[bool, float]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_heading - Not connected to a robot")
            return False, 0.0
        
        # Command to get the robot heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 12)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_heading - Command ID = 12, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_heading - Command ID = 12, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0.0

        # Extract the heading from the response
        try:
            seq_id, heading = struct.unpack("<Bf", response[:5])
        except ValueError as e:
            logging.error(f"CommandsTx::get_heading - Error unpacking response: {e}")
            return False, 0.0
        logging.info(f"CommandsTx::get_heading - Heading = {heading}")
        return True, heading
    
    # Command ID = 13
    async def get_position(self) -> tuple[bool, float, float]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_position - Not connected to a robot")
            return False, 0.0, 0.0
        
        # Command to get the robot position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 13)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_position - Command ID = 13, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_position - Command ID = 13, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0.0, 0.0

        # Extract the position from the response
        try:
            seq_id, x, y = struct.unpack("<Bff", response[:9])
        except ValueError as e:
            logging.error(f"CommandsTx::get_position - Error unpacking response: {e}")
            return False, 0.0, 0.0
        logging.info(f"CommandsTx::get_position - X = {x}, Y = {y}")
        return True, x, y
    
    # Command ID = 14
    async def pen(self, pen_up: bool) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::pen - Not connected to a robot")
            return False
        
        # Command to raise or lower the pen
        if pen_up:
            parameter = 1
        else:
            parameter = 0

        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBB", seq_id, 14, parameter)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::pen - Command ID = 14, Sequence ID = {seq_id}, pen_up = {pen_up}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::pen - Command ID = 14, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 15
    async def eyes(self, eye_id, red, green, blue) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::eyes - Not connected to a robot")
            return False
        
        # Command to set the eye colour
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBBBBB", seq_id, 15, eye_id, red, green, blue)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::eyes - Command ID = 15, Sequence ID = {seq_id}, eye_id = {eye_id}, red = {red}, green = {green}, blue = {blue}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::eyes - Command ID = 15, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 16
    async def get_power(self) -> tuple[bool, int, int, int]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_power - Not connected to a robot")
            return False, 0, 0, 0
        
        # Command to get the robot power
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 16)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_power - Command ID = 16, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_power - Command ID = 16, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0, 0, 0

        # Extract the power from the response
        try:
            seq_id, mv, ma, mw = struct.unpack("<Blll", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::get_power - Error unpacking response: {e}")
            return False, 0, 0, 0
        logging.info(f"CommandsTx::get_power - mV = {mv}, mA = {ma}, mW = {mw}")
        return True, mv, ma, mw 
    
    # Command ID = 17
    async def get_pen(self) -> tuple[bool, bool]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_pen - Not connected to a robot")
            return False, False
        
        # Command to get the pen status
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 17)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_pen - Command ID = 17, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_pen - Command ID = 17, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, False

        # Extract the pen status from the response
        try:
            seq_id, pen_up = struct.unpack("<BB", response[:2])
        except ValueError as e:
            logging.error(f"CommandsTx::get_pen - Error unpacking response: {e}")
            return False, False
        logging.info(f"CommandsTx::get_pen - Pen up = {pen_up}")
        return True, pen_up
    
    # Command ID = 18
    async def set_linear_velocity(self, target_speed: int, acceleration: int) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::set_linear_velocity - Not connected to a robot")
            return False
        
        # Command to set the linear velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBll", seq_id, 18, target_speed, acceleration)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::set_linear_velocity - Command ID = 18, Sequence ID = {seq_id}, target_speed = {target_speed}, acceleration = {acceleration}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::set_linear_velocity - Command ID = 18, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 19
    async def set_rotational_velocity(self, target_speed: int, acceleration: int) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::set_rotational_velocity - Not connected to a robot")
            return False
        
        # Command to set the rotational velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBll", seq_id, 19, target_speed, acceleration)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::set_rotational_velocity - Command ID = 19, Sequence ID = {seq_id}, target_speed = {target_speed}, acceleration = {acceleration}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::set_rotational_velocity - Command ID = 19, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 20
    async def get_linear_velocity(self) -> tuple[bool, int, int]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_linear_velocity - Not connected to a robot")
            return False, 0, 0
        
        # Command to get the linear velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 20)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_linear_velocity - Command ID = 20, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_linear_velocity - Command ID = 20, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0, 0

        # Extract the linear velocity from the response
        try:
            seq_id, target_speed, acceleration = struct.unpack("<Bll", response[:9])
        except ValueError as e:
            logging.error(f"CommandsTx::get_linear_velocity - Error unpacking response: {e}")
            return False, 0, 0
        logging.info(f"CommandsTx::get_linear_velocity - Target speed = {target_speed}, Acceleration = {acceleration}")
        return True, target_speed, acceleration
    
    # Command ID = 21
    async def get_rotational_velocity(self) -> tuple[bool, int, int]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_rotational_velocity - Not connected to a robot")
            return False, 0, 0
        
        # Command to get the rotational velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 21)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_rotational_velocity - Command ID = 21, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_rotational_velocity - Command ID = 21, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0, 0

        # Extract the rotational velocity from the response
        try:
            seq_id, target_speed, acceleration = struct.unpack("<Bll", response[:9])
        except ValueError as e:
            logging.error(f"CommandsTx::get_rotational_velocity - Error unpacking response: {e}")
            return False, 0, 0
        logging.info(f"CommandsTx::get_rotational_velocity - Target speed = {target_speed}, Acceleration = {acceleration}")
        return True, target_speed, acceleration

    # Command ID = 22
    async def set_wheel_diameter_calibration(self, wheel_diameter: int) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::set_wheel_diameter_calibration - Not connected to a robot")
            return False
        
        # Command to set the wheel diameter calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BBi", seq_id, 22, wheel_diameter)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::set_wheel_diameter_calibration - Command ID = 22, Sequence ID = {seq_id}, wheel_diameter = {wheel_diameter}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::set_wheel_diameter_calibration - Command ID = 22, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        return True

    # Command ID = 23
    async def set_axel_distance_calibration(self, axel_distance: int) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::set_axel_distance_calibration - Not connected to a robot")
            return False
        
        # Command to set the axel distance calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BBi", seq_id, 23, axel_distance)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::set_axel_distance_calibration - Command ID = 23, Sequence ID = {seq_id}, axel_distance = {axel_distance}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::set_axel_distance_calibration - Command ID = 23, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        return True

    # Command ID = 24
    async def get_wheel_diameter_calibration(self) -> tuple[bool, int]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_wheel_diameter_calibration - Not connected to a robot")
            return False, 0
        
        # Command to get the wheel diameter calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 24)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_wheel_diameter_calibration - Command ID = 24, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_wheel_diameter_calibration - Command ID = 24, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0

        try:
            seq_id, cali_wheel = struct.unpack("<Bi", response[:5])
        except ValueError as e:
            logging.error(f"CommandsTx::get_wheel_diameter_calibration - Error unpacking response: {e}")
            return False, 0
        logging.info(f"CommandsTx::get_wheel_diameter_calibration - Calibration wheel diameter = {cali_wheel}")
        return True, cali_wheel

    # Command ID = 25
    async def get_axel_distance_calibration(self) -> tuple[bool, int]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_axel_distance_calibration - Not connected to a robot")
            return False, 0
        
        # Command to get the axel distance calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 25)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_axel_distance_calibration - Command ID = 25, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_axel_distance_calibration - Command ID = 25, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0

        try:
            seq_id, cali_axel = struct.unpack("<Bi", response[:5])
        except ValueError as e:
            logging.error(f"CommandsTx::get_axel_distance_calibration - Error unpacking response: {e}")
            return False, 0
        logging.info(f"CommandsTx::get_axel_distance_calibration - Calibration axel distance = {cali_axel}")
        return True, cali_axel

    # Command ID = 26
    async def set_turtle_id(self, turtle_id: int) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::set_turtle_id - Not connected to a robot")
            return False
        
        # Command to set the turtle ID
        seq_id = self.__next_seq()
        data = struct.pack("<BBB", seq_id, 26, turtle_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::set_turtle_id - Command ID = 26, Sequence ID = {seq_id}, turtle_id = {turtle_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::set_turtle_id - Command ID = 26, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        return True

    # Command ID = 27
    async def get_turtle_id(self) -> tuple[bool, int]:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::get_turtle_id - Not connected to a robot")
            return False, 0
        
        # Command to get the turtle ID
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 27)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::get_turtle_id - Command ID = 27, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::get_turtle_id - Command ID = 27, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0

        try:
            seq_id, turtle_id = struct.unpack("<BB", response[:2])
        except ValueError as e:
            logging.error(f"CommandsTx::get_turtle_id - Error unpacking response: {e}")
            return False, 0
        logging.info(f"CommandsTx::get_turtle_id - Turtle ID = {turtle_id}")
        return True, turtle_id

    # Command ID = 28
    async def load_config(self) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::load_config - Not connected to a robot")
            return False
        
        # Command to load the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 28)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::load_config - Command ID = 28, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::load_config - Command ID = 28, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        return True

    # Command ID = 29
    async def save_config(self) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::save_config - Not connected to a robot")
            return False
        
        # Command to save the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 29)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::save_config - Command ID = 29, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::save_config - Command ID = 29, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        return True

    # Command ID = 30
    async def reset_config(self) -> bool:
        if not self._ble_central.is_connected:
            logging.error("CommandsTx::reset_config - Not connected to a robot")
            return False
        
        # Command to reset the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 30)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::reset_config - Command ID = 30, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::reset_config - Command ID = 30, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        return True

if __name__ == "__main__":
    from main import main
    main()