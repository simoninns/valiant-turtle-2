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
                logging.error("Commands::__wait_for_command_response - Got P2C queue event but the queue was empty?")
                seq_id_rx = 0
                return None

            self._ble_central._p2c_queue_event.clear()
            seq_id_rx = data[0]

            # Check if the sequence ID matches
            if seq_id_rx == seq_id:
                #logging.info(f"Commands::__wait_for_command_response - Sequence ID = {seq_id_rx} matched")
                return data
            else:
                logging.info(f"Commands::__wait_for_command_response - Sequence ID = {seq_id_rx} did not match received sequence ID = {seq_id}")

    # Command ID = 1
    async def motors(self, enable: bool) -> bool:
        if not self._ble_central.is_connected:
            logging.info("Commands::motors - Not connected to a robot")
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
        logging.info(f"Commands::motors - Command ID = 1, Sequence ID = {seq_id}, enable = {enable}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::motors - Command ID = 1, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True

    # Command ID = 2
    async def forward(self, distance_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::forward - Not connected to a robot")
            return False
        
        # Command to move the robot forward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 2, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::forward - Command ID = 2, Sequence ID = {seq_id}, distance = {distance_mm}")

        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::forward - Command ID = 2, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 3
    async def backward(self, distance_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::backward - Not connected to a robot")
            return False
        
        # Command to move the robot backward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 3, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::backward - Command ID = 3, Sequence ID = {seq_id}, distance = {distance_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::backward - Command ID = 3, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 4
    async def left(self, angle_degrees: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::left - Not connected to a robot")
            return False
        
        # Command to turn the robot left
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 4, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::left - Command ID = 4, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::left - Command ID = 4, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 5
    async def right(self, angle_degrees: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::right - Not connected to a robot")
            return False
        
        # Command to turn the robot right
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 5, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::right - Command ID = 5, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::right - Command ID = 5, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True

    # Command ID = 6
    async def heading(self, angle_degrees: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::heading - Not connected to a robot")
            return False
        
        # Command to set the robot heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 6, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::heading - Command ID = 6, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::heading - Command ID = 6, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 7
    async def position_x(self, x_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::position_x - Not connected to a robot")
            return False
        
        # Command to set the robot X position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 7, x_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::position_x - Command ID = 7, Sequence ID = {seq_id}, x = {x_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::position_x - Command ID = 7, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 8
    async def position_y(self, y_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::position_y - Not connected to a robot")
            return False
        
        # Command to set the robot Y position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, 8, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::position_y - Command ID = 8, Sequence ID = {seq_id}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::position_y - Command ID = 8, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 9
    async def position(self, x_mm: float, y_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::position - Not connected to a robot")
            return False
        
        # Command to set the robot position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, 9, x_mm, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::position - Command ID = 9, Sequence ID = {seq_id}, x = {x_mm}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::position - Command ID = 9, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 10
    async def towards(self, x_mm: float, y_mm: float) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::towards - Not connected to a robot")
            return False
        
        # Command to move the robot towards a point
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, 10, x_mm, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::towards - Command ID = 10, Sequence ID = {seq_id}, x = {x_mm}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::towards - Command ID = 10, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 11
    async def reset_origin(self) -> bool:
        if not self._ble_central.is_connected:
            logging.error("Commands::reset_origin - Not connected to a robot")
            return False
        
        # Command to reset the x,y origin and heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 11)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::reset_origin - Command ID = 11, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::reset_origin - Command ID = 11, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    # Command ID = 12
    async def get_heading(self) -> tuple[bool, float]:
        if not self._ble_central.is_connected:
            logging.error("Commands::get_heading - Not connected to a robot")
            return False, 0.0
        
        # Command to get the robot heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 12)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::get_heading - Command ID = 12, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::get_heading - Command ID = 12, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0.0

        # Extract the heading from the response
        seq_id, heading = struct.unpack("<Bf", response[:5])
        logging.info(f"Commands::get_heading - Heading = {heading}")
        return True, heading
    
    # Command ID = 13
    async def get_position(self) -> tuple[bool, float, float]:
        if not self._ble_central.is_connected:
            logging.error("Commands::get_position - Not connected to a robot")
            return False, 0.0, 0.0
        
        # Command to get the robot position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, 13)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"Commands::get_position - Command ID = 13, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"Commands::get_position - Command ID = 13, Sequence ID = {seq_id} timed out")
            self._ble_central.flag_disconnection()
            return False, 0.0, 0.0

        # Extract the position from the response
        seq_id, x, y = struct.unpack("<Bff", response[:9])
        logging.info(f"Commands::get_position - X = {x}, Y = {y}")
        return True, x, y

if __name__ == "__main__":
    from main import main
    main()