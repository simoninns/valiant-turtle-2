#************************************************************************ 
#
#   diffdrive.py
#
#   Differential Drive Motor Control
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

import library.picolog as picolog
from drv8825 import Drv8825
from stepper import Stepper

from machine import Pin

class DiffDrive:
    def __init__(self, drv8825_enable_gpio: int, drv8825_m0_gpio :int, drv8825_m1_gpio :int, drv8825_m2_gpio :int, left_step_gpio :int, left_direction_gpio :int, right_step_gpio :int, right_direction_gpio :int):
        # Configure the DRV8825 control GPIOs
        self._drv8825_enable_pin = Pin(drv8825_enable_gpio, Pin.OUT)
        self._drv8825_m0_pin = Pin(drv8825_m0_gpio, Pin.OUT)
        self._drv8825_m1_pin = Pin(drv8825_m1_gpio, Pin.OUT)
        self._drv8825_m2_pin = Pin(drv8825_m2_gpio, Pin.OUT)

        # Create the DRV8825 instance (The DRV8825 driver is shared between the two stepper motors
        # as the enable line and microstepping mode pins are shared)
        self._steps_per_revolution = 800
        self._drv8825 = Drv8825(self._drv8825_enable_pin, self._drv8825_m0_pin, self._drv8825_m1_pin, self._drv8825_m2_pin)
        self._drv8825.set_steps_per_revolution(self._steps_per_revolution)
        self._drv8825.set_enable(False)

        # Configure the stepper control GPIOs
        self._left_step_pin = Pin(left_step_gpio, Pin.OUT)
        self._left_direction_pin = Pin(left_direction_gpio, Pin.OUT)
        self._right_step_pin = Pin(right_step_gpio, Pin.OUT)
        self._right_direction_pin = Pin(right_direction_gpio, Pin.OUT)

        # Create the combined stepper motor instance
        self._stepper = Stepper(self._drv8825, self._left_step_pin, self._left_direction_pin, self._right_step_pin, self._right_direction_pin)
        self._stepper.set_direction_forwards()

        # Default linear velocity
        self._linear_target_speed_mmps = 200 # mm per second
        self._linear_acceleration_mmpss = 4 # mm per second per second

        # Default rotational velocity
        self._rotational_target_speed_mmps = 100 # mm per second
        self._rotational_acceleration_mmpss = 4 # mm per second per second

        # Default wheel diameter and axel distance
        self._wheel_diameter_mm = 55.53
        self._axel_distance_mm = 224.0

        # Default wheel and axel calibration
        self._wheel_calibration_um = 0 # micrometers
        self._axel_calibration_um = 0 # micrometers

        # Value of pi
        self._pi = 3.14159

    def set_enable(self, enable: bool):
        """Enable or disable the motor driver"""
        self._drv8825.set_enable(enable)

    @property
    def is_enabled(self):
        """Returns True if the motor driver is enabled"""
        return self._drv8825.is_enabled
    
    @property
    def is_moving(self):
        """Returns True if the motors are moving"""
        return self._stepper.is_busy
    
    def set_wheel_calibration(self, value: int):
        """Set the wheel calibration in micrometers"""
        self._wheel_calibration_um = value

    def get_wheel_calibration(self) -> int:
        """Get the wheel calibration in micrometers"""
        return self._wheel_calibration_um

    def set_axel_calibration(self, value: int):
        """Set the axel calibration in micrometers"""
        self._axel_calibration_um = value

    def get_axel_calibration(self) -> int:
        """Get the axel calibration in micrometers"""
        return self._axel_calibration_um
    
    def drive_forward(self, distance_mm: float):
        """Linear motion forwards"""
        self.__configure_linear_velocity()
        self._stepper.set_direction_forwards()
        self._stepper.move(self.__mm_to_steps(distance_mm))

    def drive_backward(self, distance_mm: float):
        """Linear motion backwards"""
        self.__configure_linear_velocity()
        self._stepper.set_direction_backwards()
        self._stepper.move(self.__mm_to_steps(distance_mm))

    def turn_left(self, degrees: float):
        """Rotational motion to the left"""
        self.__configure_rotational_velocity()
        self._stepper.set_direction_left()
        self._stepper.move(self.__degrees_to_steps(degrees))

    def turn_right(self, degrees: float):
        """Rotational motion to the right"""
        self.__configure_rotational_velocity()
        self._stepper.set_direction_right()
        self._stepper.move(self.__degrees_to_steps(degrees))

    def __configure_linear_velocity(self):
        """Configure the steppers for the linear velocity"""
        self._stepper.set_target_speed_sps(self.__mm_to_steps(self._linear_target_speed_mmps))
        self._stepper.set_acceleration_spsps(self.__mm_to_steps(self._linear_acceleration_mmpss))

    def __configure_rotational_velocity(self):
        """Configure the steppers for the rotational velocity"""
        self._stepper.set_target_speed_sps(self.__mm_to_steps(self._rotational_target_speed_mmps))
        self._stepper.set_acceleration_spsps(self.__mm_to_steps(self._rotational_acceleration_mmpss))

    def set_linear_velocity(self, velocity_mm_s: float, acceleration_mm_s2: float):
        """Set the linear velocity"""
        self._linear_target_speed_mmps = velocity_mm_s
        self._linear_acceleration_mmpss = acceleration_mm_s2

    def get_linear_velocity(self) -> tuple:
        """Get the linear target velocity and acceleration"""
        return self._linear_target_speed_mmps, self._linear_acceleration_mmpss

    def set_rotational_velocity(self, velocity_mm_s: float, acceleration_mm_s2: float):
        """Set the rotational velocity"""
        self._rotational_target_speed_mmps = velocity_mm_s
        self._rotational_acceleration_mmpss = acceleration_mm_s2

    def get_rotational_velocity(self) -> tuple:
        """Get the rotational target velocity and acceleration"""
        return self._rotational_target_speed_mmps, self._rotational_acceleration_mmpss

    def get_motor_status(self) -> tuple:
        """Returns a tuple containing the status of the stepper motors with
        0 = idle, 1 = moving forwards, 2 = moving backwards"""
        left_stepper_status = 0
        right_stepper_status = 0

        if self._stepper.is_busy:
            if self._stepper.left_direction:
                left_stepper_status = 1
            else:
                left_stepper_status = 2

            if self._stepper.right_direction:
                right_stepper_status = 1
            else:
                right_stepper_status = 2

        return left_stepper_status, right_stepper_status
    
    # Convert millimeters to steps
    def __mm_to_steps(self, millimeters: float) -> int:
        circumference = self._pi * (self._wheel_diameter_mm + (self._wheel_calibration_um / 1000))
        millimeters_per_step = (circumference / self._steps_per_revolution)
        return int(millimeters / millimeters_per_step)
    
    # Convert degrees to steps
    # Note: This is only for when the robot turns on it's axis
    def __degrees_to_steps(self, degrees: float) -> int:
        circumference = self._pi * (self._axel_distance_mm + (self._axel_calibration_um / 1000))
        millimeters = (circumference / 360.0) * degrees
        return self.__mm_to_steps(millimeters)
    
if __name__ == "__main__":
    from main import main
    main()