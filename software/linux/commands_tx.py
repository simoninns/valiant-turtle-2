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

class CommandsTx:
    def __init__(self, ble_central: BleCentral):
        self._ble_central = ble_central
        self._command_sequence = 0

    def __next_seq(self) -> int:
        self._command_sequence += 1
        if self._command_sequence > 255:
            self._command_sequence = 0
        return self._command_sequence
    
    async def __wait_for_command_response(self, seq_id: int) -> bytes:
        while True:
            await self._ble_central._p2c_queue_event.wait()
            data = self._ble_central._p2c_queue.pop(0)
            _, seq_id_rx = struct.unpack("BB", data[:2])

            # Check if the sequence ID matches
            if seq_id_rx == seq_id:
                return data

    # Command ID = 1
    async def motors(self, enable: bool):
        # Command to enable or disable the motors
        if enable:
            parameter = 1
        else:
            parameter = 0

        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("BBB", 1, seq_id, parameter)
        self._ble_central.add_to_c2p_queue(data)
        logging.debug(f"Commands::motors - Command ID = 1, Sequence ID = {seq_id}, enable = {enable}")
        
        # Wait for the command to be processed with a 60 second timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=60.0)
            logging.error(f"Commands::motors - Command ID = 1, Sequence ID = {seq_id} response received")
        except asyncio.TimeoutError:
            logging.error(f"Commands::motors - Command ID = 1, Sequence ID = {seq_id} timed out")

        # This command does not return any data, so we don't need to return anything
        return

    # Command ID = 2
    async def forward(self, distance_mm: float):
        # Command to move the robot forward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("BBf", 2, seq_id, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.debug(f"Commands::forward - Command ID = 2, Sequence ID = {seq_id}, distance = {distance_mm}")

        # Wait for the command to be processed with a 60 second timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=60.0)
            logging.error(f"Commands::motors - Command ID = 2, Sequence ID = {seq_id} response received")
        except asyncio.TimeoutError:
            logging.error(f"Commands::motors - Command ID = 2, Sequence ID = {seq_id} timed out")

        # This command does not return any data, so we don't need to return anything
        return
    
    # Command ID = 3
    async def backward(self, distance_mm: float):
        # Command to move the robot backward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("BBf", 3, seq_id, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.debug(f"Commands::backward - Command ID = 3, Sequence ID = {seq_id}, distance = {distance_mm}")
        
        # Wait for the command to be processed with a 60 second timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=60.0)
            logging.error(f"Commands::motors - Command ID = 3, Sequence ID = {seq_id} response received")
        except asyncio.TimeoutError:
            logging.error(f"Commands::motors - Command ID = 3, Sequence ID = {seq_id} timed out")

        # This command does not return any data, so we don't need to return anything
        return
    
    # Command ID = 4
    async def left(self, angle_degrees: float):
        # Command to turn the robot left
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("BBf", 4, seq_id, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.debug(f"Commands::left - Command ID = 4, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a 60 second timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=60.0)
            logging.error(f"Commands::motors - Command ID = 4, Sequence ID = {seq_id} response received")
        except asyncio.TimeoutError:
            logging.error(f"Commands::motors - Command ID = 4, Sequence ID = {seq_id} timed out")

        # This command does not return any data, so we don't need to return anything
        return
    
    # Command ID = 5
    async def right(self, angle_degrees: float):
        # Command to turn the robot right
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("BBf", 5, seq_id, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.debug(f"Commands::right - Command ID = 5, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a 60 second timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=60.0)
            logging.error(f"Commands::motors - Command ID = 5, Sequence ID = {seq_id} response received")
        except asyncio.TimeoutError:
            logging.error(f"Commands::motors - Command ID = 5, Sequence ID = {seq_id} timed out")

        # This command does not return any data, so we don't need to return anything
        return

    # async def heading(self, heading_degrees: float):
    #     self._diff_drive.set_heading(heading_degrees)
    #     # Wait for the drive to finish
    #     while self._diff_drive.is_moving:
    #         await asyncio.sleep_ms(250)

    # async def position_x(self, x_mm: float):
    #     self._diff_drive.set_cartesian_x_position(x_mm)
    #     # Wait for the drive to finish
    #     while self._diff_drive.is_moving:
    #         await asyncio.sleep_ms(250)

    # async def position_y(self, y_mm: float):
    #     self._diff_drive.set_cartesian_y_position(y_mm)
    #     # Wait for the drive to finish
    #     while self._diff_drive.is_moving:
    #         await asyncio.sleep_ms(250)

    # async def position(self, x_mm: float, y_mm: float):
    #     self._diff_drive.set_cartesian_position(x_mm, y_mm)
    #     # Wait for the drive to finish
    #     while self._diff_drive.is_moving:
    #         await asyncio.sleep_ms(250)

    # async def towards(self, x_mm: float, y_mm: float):
    #     self._diff_drive.turn_towards_cartesian_point(x_mm, y_mm)
    #     # Wait for the drive to finish
    #     while self._diff_drive.is_moving:
    #         await asyncio.sleep_ms(250)

    # async def reset_origin(self):
    #     self._diff_drive.reset_origin()

    # async def get_heading(self) -> float:
    #     return self._diff_drive.get_heading()

    # async def get_position(self) -> tuple[float, float]:
    #     x_pos, y_pos = self._diff_drive.get_cartesian_position()
    #     return x_pos, y_pos

    # async def pen(self, up: bool):
    #     if up:
    #         self._pen.up()
    #     else:
    #         self._pen.down()

    # async def get_pen(self) -> bool:
    #     return self._pen.is_servo_up

    # async def eyes(self, eye: int, red: int, green: int, blue: int):
    #     if eye == 0:
    #         # Both eyes
    #         self._led_fx.set_led_colour(0, red, green, blue)
    #         self._led_fx.set_led_colour(1, red, green, blue)
    #     elif eye == 1:
    #         # Left eye
    #         self._led_fx.set_led_colour(0, red, green, blue)
    #     else:
    #         # Right eye
    #         self._led_fx.set_led_colour(1, red, green, blue)

    # async def get_mv(self) -> int:
    #     return int(self._ina260.voltage_mV)
    
    # async def get_ma(self) -> int:
    #     return int(self._ina260.current_mA)
    
    # async def get_mw(self) -> int:
    #     return int(self._ina260.power_mW)
    
    # async def set_linear_velocity(self, target_speed: int, acceleration: int):
    #     self._diff_drive.set_linear_velocity(target_speed, acceleration)
    #     self._configuration.linear_target_speed_mmps = target_speed
    #     self._configuration.linear_acceleration_mmpss = acceleration
    #     picolog.debug(f"Commands::set_linear_velocity - Setting linear target speed to = {target_speed} mm/s and acceleration to = {acceleration} mm/s^2")

    # async def set_rotational_velocity(self, target_speed: int, acceleration: int):
    #     self._diff_drive.set_rotational_velocity(target_speed, acceleration)
    #     self._configuration.rotational_target_speed_mmps = target_speed
    #     self._configuration.rotational_acceleration_mmpss = acceleration
    #     picolog.debug(f"Commands::set_rotational_velocity - Setting rotational target speed to = {target_speed} mm/s and acceleration to = {acceleration} mm/s^2")

    # async def get_linear_velocity(self) -> tuple[int, int]:
    #     return self._diff_drive.get_linear_velocity()
    
    # async def get_rotational_velocity(self) -> tuple[int, int]:
    #     return self._diff_drive.get_rotational_velocity()
        
    # async def set_wheel_diameter_calibration(self, calibration_um: int):
    #     self._diff_drive.set_wheel_calibration(calibration_um)
    #     self._configuration.wheel_calibration_um = calibration_um

    # async def set_axel_distance_calibration(self, calibration_um: int):
    #     self._diff_drive.set_axel_calibration(calibration_um)
    #     self._configuration.axel_calibration_um = calibration_um

    # async def get_wheel_diameter_calibration(self) -> int:
    #     return self._diff_drive.get_wheel_calibration()
    
    # async def get_axel_distance_calibration(self) -> int:
    #     return self._diff_drive.get_axel_calibration()
    
    # async def set_turtle_id(self, turtle_id: int):
    #     self._configuration.turtle_id = turtle_id

    # async def get_turtle_id(self) -> int:
    #     return self._configuration.turtle_id

    # async def load_config(self):
    #     self._configuration.unpack(self._eeprom.read(0, self._configuration.pack_size))
    #     self._diff_drive.set_linear_velocity(self._configuration.linear_target_speed_mmps, self._configuration.linear_acceleration_mmpss)
    #     self._diff_drive.set_rotational_velocity(self._configuration.rotational_target_speed_mmps, self._configuration.rotational_acceleration_mmpss)
    #     self._diff_drive.set_wheel_calibration(self._configuration.wheel_calibration_um)
    #     self._diff_drive.set_axel_calibration(self._configuration.axel_calibration_um)

    # async def save_config(self):
    #     self._eeprom.write(0, self._configuration.pack())

    # async def reset_config(self):
    #     self._configuration.default()
    #     self._diff_drive.set_linear_velocity(self._configuration.linear_target_speed_mmps, self._configuration.linear_acceleration_mmpss)
    #     self._diff_drive.set_rotational_velocity(self._configuration.rotational_target_speed_mmps, self._configuration.rotational_acceleration_mmpss)
    #     self._diff_drive.set_wheel_calibration(self._configuration.wheel_calibration_um)
    #     self._diff_drive.set_axel_calibration(self._configuration.axel_calibration_um)

if __name__ == "__main__":
    from main import main
    main()