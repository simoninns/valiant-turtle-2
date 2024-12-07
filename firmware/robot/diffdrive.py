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

import library.logging as logging
from drv8825 import Drv8825
from stepper import Stepper
from metric import Metric

from machine import Pin

class DiffDrive:
    def __init__(self, drv8825_enable_gpio: int, drv8825_m0_gpio :int, drv8825_m1_gpio :int, drv8825_m2_gpio :int, left_step_gpio :int, left_direction_gpio :int, right_step_gpio :int, right_direction_gpio :int):
        # Create a metric object for unit conversion with default calibration values
        self._metric = Metric()

        # Configure the DRV8825 control GPIOs
        self._drv8825_enable_pin = Pin(drv8825_enable_gpio, Pin.OUT)
        self._drv8825_m0_pin = Pin(drv8825_m0_gpio, Pin.OUT)
        self._drv8825_m1_pin = Pin(drv8825_m1_gpio, Pin.OUT)
        self._drv8825_m2_pin = Pin(drv8825_m2_gpio, Pin.OUT)

        # Create the DRV8825 instance (The DRV8825 driver is shared between the two stepper motors
        # as the enable line and microstepping mode pins are shared)
        self._drv8825 = Drv8825(self._drv8825_enable_pin, self._drv8825_m0_pin, self._drv8825_m1_pin, self._drv8825_m2_pin)
        self._drv8825.set_steps_per_revolution(800)
        self._drv8825.set_enable(False)

        # Configure the stepper control GPIOs
        self._left_step_pin = Pin(left_step_gpio, Pin.OUT)
        self._left_direction_pin = Pin(left_direction_gpio, Pin.OUT)
        self._right_step_pin = Pin(right_step_gpio, Pin.OUT)
        self._right_direction_pin = Pin(right_direction_gpio, Pin.OUT)

        # Create the left and right stepper motor instances
        self._left_stepper = Stepper(self._drv8825, self._left_step_pin, self._left_direction_pin, True)
        self._right_stepper = Stepper(self._drv8825, self._right_step_pin, self._right_direction_pin, False)
        self._left_stepper.set_direction_forwards()
        self._right_stepper.set_direction_forwards()

        # Default linear velocity
        self._linear_target_speed_sps = self._metric.mm_to_steps(200)
        self._linear_acceleration_spsps = self._metric.mm_to_steps(4)

        # Default rotational velocity
        self._rotational_target_speed_sps = self._metric.mm_to_steps(100)
        self._rotational_acceleration_spsps = self._metric.mm_to_steps(4)

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
        return self._left_stepper.is_busy or self._right_stepper.is_busy
    
    def set_wheel_calibration(self, value: float):
        """Set the wheel calibration"""
        self._metric.set_wheel_calibration(value)

    def set_axel_calibration(self, value: float):
        """Set the axel calibration"""
        self._metric.set_axel_calibration(value)
    
    def drive_forward(self, distance_mm: float):
        """Linear motion forwards"""
        self.__configure_linear_velocity()
        self._left_stepper.set_direction_forwards()
        self._right_stepper.set_direction_forwards()
        self._left_stepper.move(self._metric.mm_to_steps(distance_mm))
        self._right_stepper.move(self._metric.mm_to_steps(distance_mm))

    def drive_backward(self, distance_mm: float):
        """Linear motion backwards"""
        self.__configure_linear_velocity()
        self._left_stepper.set_direction_backwards()
        self._right_stepper.set_direction_backwards()
        self._left_stepper.move(self._metric.mm_to_steps(distance_mm))
        self._right_stepper.move(self._metric.mm_to_steps(distance_mm))

    def turn_left(self, degrees: float):
        """Rotational motion to the left"""
        self.__configure_rotational_velocity()
        self._left_stepper.set_direction_forwards()
        self._right_stepper.set_direction_backwards()
        self._left_stepper.move(self._metric.degrees_to_steps(degrees))
        self._right_stepper.move(self._metric.degrees_to_steps(degrees))

    def turn_right(self, degrees: float):
        """Rotational motion to the right"""
        self.__configure_rotational_velocity()
        self._left_stepper.set_direction_backwards()
        self._right_stepper.set_direction_forwards()
        self._left_stepper.move(self._metric.degrees_to_steps(degrees))
        self._right_stepper.move(self._metric.degrees_to_steps(degrees))

    def __configure_linear_velocity(self):
        """Configure the steppers for the linear velocity"""
        self._left_stepper.set_target_speed_sps(self._linear_target_speed_sps)
        self._left_stepper.set_acceleration_spsps(self._linear_acceleration_spsps)
        self._right_stepper.set_target_speed_sps(self._linear_target_speed_sps)
        self._right_stepper.set_acceleration_spsps(self._linear_acceleration_spsps)

    def __configure_rotational_velocity(self):
        """Configure the steppers for the rotational velocity"""
        self._left_stepper.set_target_speed_sps(self._rotational_target_speed_sps)
        self._left_stepper.set_acceleration_spsps(self._rotational_acceleration_spsps)
        self._right_stepper.set_target_speed_sps(self._rotational_target_speed_sps)
        self._right_stepper.set_acceleration_spsps(self._rotational_acceleration_spsps)

    def set_linear_velocity(self, velocity_mm_s: float, acceleration_mm_s2: float):
        """Set the linear velocity"""
        self._linear_target_speed_sps = self._metric.mm_to_steps(velocity_mm_s)
        self._linear_acceleration_spsps = self._metric.mm_to_steps(acceleration_mm_s2)

    def set_rotational_velocity(self, velocity_mm_s: float, acceleration_mm_s2: float):
        """Set the rotational velocity"""
        self._rotational_target_speed_sps = self._metric.mm_to_steps(velocity_mm_s)
        self._rotational_acceleration_spsps = self._metric.mm_to_steps(acceleration_mm_s2)

    def get_motor_status(self) -> tuple:
        """Returns a tuple containing the status of the left and right motors with
        0 = idle, 1 = moving forwards, 2 = moving backwards"""
        left_motor_status = 0
        right_motor_status = 0

        if self._left_stepper.is_busy:
            if self._left_stepper.is_forwards:
                left_motor_status = 1
            else:
                left_motor_status = 2

        if self._right_stepper.is_busy:
            if self._right_stepper.is_forwards:
                right_motor_status = 1
            else:
                right_motor_status = 2

        return (left_motor_status, right_motor_status)
    
if __name__ == "__main__":
    from main import main
    main()