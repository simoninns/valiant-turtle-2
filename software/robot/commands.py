#************************************************************************ 
#
#   commands.py
#
#   Command handling for the Valiant Turtle 2 robot
#   Valiant Turtle 2 - Robot firmware
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

import picolog
import asyncio

from pen import Pen
from ina260 import Ina260
from eeprom import Eeprom
from configuration import Configuration
from led_fx import LedFx
from diffdrive import DiffDrive

class Commands:
    def __init__(self, pen :Pen, ina260 :Ina260, eeprom :Eeprom, led_fx :LedFx, diff_drive :DiffDrive, configuration :Configuration):
        self._pen = pen
        self._ina260 = ina260
        self._eeprom = eeprom
        self._led_fx = led_fx
        self._diff_drive = diff_drive
        self._configuration = configuration

    async def motors(self, enable: bool):
        # Command to enable or disable the motors
        if enable:
            self._diff_drive.set_enable(True)
        else:
            self._diff_drive.set_enable(False)

    async def forward(self, distance_mm: float):
        self._diff_drive.drive_forward(distance_mm)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def backward(self, distance_mm: float):
        self._diff_drive.drive_backward(distance_mm)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def left(self, angle_degrees: float):
        self._diff_drive.turn_left(angle_degrees)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def right(self, angle_degrees: float):
        self._diff_drive.turn_right(angle_degrees)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def heading(self, heading_degrees: float):
        self._diff_drive.set_heading(heading_degrees)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def position_x(self, x_mm: float):
        self._diff_drive.set_cartesian_x_position(x_mm)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def position_y(self, y_mm: float):
        self._diff_drive.set_cartesian_y_position(y_mm)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def position(self, x_mm: float, y_mm: float):
        self._diff_drive.set_cartesian_position(x_mm, y_mm)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def towards(self, x_mm: float, y_mm: float):
        self._diff_drive.turn_towards_cartesian_point(x_mm, y_mm)
        # Wait for the drive to finish
        while self._diff_drive.is_moving:
            await asyncio.sleep(0.25)

    async def reset_origin(self):
        self._diff_drive.reset_origin()

    async def get_heading(self) -> float:
        return self._diff_drive.get_heading()

    async def get_position(self) -> tuple[float, float]:
        x_pos, y_pos = self._diff_drive.get_cartesian_position()
        return x_pos, y_pos

    async def pen(self, up: bool):
        if up:
            self._pen.up()
        else:
            self._pen.down()

    async def get_pen(self) -> bool:
        return self._pen.is_servo_up

    async def eyes(self, eye: int, red: int, green: int, blue: int):
        if eye == 0:
            # Both eyes
            self._led_fx.set_led_colour(0, red, green, blue)
            self._led_fx.set_led_colour(1, red, green, blue)
        elif eye == 1:
            # Left eye
            self._led_fx.set_led_colour(0, red, green, blue)
        else:
            # Right eye
            self._led_fx.set_led_colour(1, red, green, blue)

    async def get_mv(self) -> int:
        return int(self._ina260.voltage_mV)
    
    async def get_ma(self) -> int:
        return int(self._ina260.current_mA)
    
    async def get_mw(self) -> int:
        return int(self._ina260.power_mW)
    
    async def set_linear_velocity(self, target_speed: int, acceleration: int):
        self._diff_drive.set_linear_velocity(target_speed, acceleration)
        self._configuration.linear_target_speed_mmps = target_speed
        self._configuration.linear_acceleration_mmpss = acceleration
        picolog.debug(f"Commands::set_linear_velocity - Setting linear target speed to = {target_speed} mm/s and acceleration to = {acceleration} mm/s^2")

    async def set_rotational_velocity(self, target_speed: int, acceleration: int):
        self._diff_drive.set_rotational_velocity(target_speed, acceleration)
        self._configuration.rotational_target_speed_mmps = target_speed
        self._configuration.rotational_acceleration_mmpss = acceleration
        picolog.debug(f"Commands::set_rotational_velocity - Setting rotational target speed to = {target_speed} mm/s and acceleration to = {acceleration} mm/s^2")

    async def get_linear_velocity(self) -> tuple[int, int]:
        return self._diff_drive.get_linear_velocity()
    
    async def get_rotational_velocity(self) -> tuple[int, int]:
        return self._diff_drive.get_rotational_velocity()
        
    async def set_wheel_diameter_calibration(self, calibration_um: int):
        self._diff_drive.set_wheel_calibration(calibration_um)
        self._configuration.wheel_calibration_um = calibration_um

    async def set_axel_distance_calibration(self, calibration_um: int):
        self._diff_drive.set_axel_calibration(calibration_um)
        self._configuration.axel_calibration_um = calibration_um

    async def get_wheel_diameter_calibration(self) -> int:
        return self._diff_drive.get_wheel_calibration()
    
    async def get_axel_distance_calibration(self) -> int:
        return self._diff_drive.get_axel_calibration()
    
    async def set_turtle_id(self, turtle_id: int):
        self._configuration.turtle_id = turtle_id

    async def get_turtle_id(self) -> int:
        return self._configuration.turtle_id

    async def load_config(self):
        self._configuration.unpack(self._eeprom.read(0, self._configuration.pack_size))
        self._diff_drive.set_linear_velocity(self._configuration.linear_target_speed_mmps, self._configuration.linear_acceleration_mmpss)
        self._diff_drive.set_rotational_velocity(self._configuration.rotational_target_speed_mmps, self._configuration.rotational_acceleration_mmpss)
        self._diff_drive.set_wheel_calibration(self._configuration.wheel_calibration_um)
        self._diff_drive.set_axel_calibration(self._configuration.axel_calibration_um)

    async def save_config(self):
        self._eeprom.write(0, self._configuration.pack())

    async def reset_config(self):
        self._configuration.default()
        self._diff_drive.set_linear_velocity(self._configuration.linear_target_speed_mmps, self._configuration.linear_acceleration_mmpss)
        self._diff_drive.set_rotational_velocity(self._configuration.rotational_target_speed_mmps, self._configuration.rotational_acceleration_mmpss)
        self._diff_drive.set_wheel_calibration(self._configuration.wheel_calibration_um)
        self._diff_drive.set_axel_calibration(self._configuration.axel_calibration_um)

if __name__ == "__main__":
    from main import main
    main()