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

import picolog
from drv8825 import Drv8825
from stepper import Stepper

from machine import Pin
import math

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

        # Create the stepper motor instances
        self._left_stepper = Stepper(self._drv8825, self._left_step_pin, self._left_direction_pin, True)
        self._left_stepper.set_direction_forwards()
        self._right_stepper = Stepper(self._drv8825, self._right_step_pin, self._right_direction_pin, False)
        self._right_stepper.set_direction_forwards()

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

        # Current position in Cartesian coordinates
        self._x_pos = 0
        self._y_pos = 0

        # Current heading in radians (common to both polar and Cartesian coordinates)
        self._heading_radians = 0

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
        return self._left_stepper.is_busy
    
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
        self.__forward(distance_mm)

        # Update the cartesian position, heading is self._heading_radians
        self._x_pos += distance_mm * math.cos(self._heading_radians)
        self._y_pos += distance_mm * math.sin(self._heading_radians)

        # Round the Cartesian position to 2 decimal places
        self._x_pos = round(self._x_pos, 2)
        self._y_pos = round(self._y_pos, 2)

    def drive_backward(self, distance_mm: float):
        """Linear motion backwards"""
        self.__backward(distance_mm)

        # Update the cartesian position, heading is self._heading_radians
        self._x_pos -= distance_mm * math.cos(self._heading_radians)
        self._y_pos -= distance_mm * math.sin(self._heading_radians)

        # Round the Cartesian position to 2 decimal places
        self._x_pos = round(self._x_pos, 2)
        self._y_pos = round(self._y_pos, 2)

    def turn_left(self, degrees: float):
        """Rotational motion to the left"""
        self.__left(math.radians(degrees))
        
        # Update the heading
        self._heading_radians += math.radians(degrees)

    def turn_right(self, degrees: float):
        """Rotational motion to the right"""
        self.__right(math.radians(degrees))

        # Update the heading
        self._heading_radians -= math.radians(degrees)

    def circle(self, radius_mm: float, extent_degrees: float):
        """Move in a circle"""
        self.__circle(radius_mm, math.radians(extent_degrees))

        # Update the Cartesian position and heading
        arc_center_x = self._x_pos - radius_mm * math.sin(self._heading_radians)
        arc_center_y = self._y_pos + radius_mm * math.cos(self._heading_radians)

        new_heading_radians = self._heading_radians + math.radians(extent_degrees)

        self._x_pos = arc_center_x + radius_mm * math.sin(new_heading_radians)
        self._y_pos = arc_center_y - radius_mm * math.cos(new_heading_radians)

        self._heading_radians = new_heading_radians

    def __forward(self, distance_mm: float):
        """Linear motion forwards"""
        if distance_mm <= 0:
            picolog.debug(f"DiffDrive::__forward - Distance in mm must be greater than zero")
            return
        self.__configure_linear_velocity()
        self._left_stepper.set_direction_forwards()
        self._right_stepper.set_direction_forwards()
        picolog.debug(f"DiffDrive::__forward - Moving {distance_mm} mm using {self.__mm_to_steps(distance_mm)} steps")
        self._left_stepper.move(self.__mm_to_steps(distance_mm))
        self._right_stepper.move(self.__mm_to_steps(distance_mm))

    def __backward(self, distance_mm: float):
        """Linear motion backwards"""
        if distance_mm <= 0:
            picolog.debug(f"DiffDrive::__backward - Distance in mm must be greater than zero")
            return
        self.__configure_linear_velocity()
        self._left_stepper.set_direction_backwards()
        self._right_stepper.set_direction_backwards()
        picolog.debug(f"DiffDrive::__backward - Moving {distance_mm} mm using {self.__mm_to_steps(distance_mm)} steps")
        self._left_stepper.move(self.__mm_to_steps(distance_mm))
        self._right_stepper.move(self.__mm_to_steps(distance_mm))

    def __left(self, radians: float):
        """Rotational motion to the left"""
        if radians <= 0:
            picolog.debug(f"DiffDrive::__left - Radians must be greater than zero")
            return
        self.__configure_rotational_velocity()
        self._left_stepper.set_direction_left()
        self._right_stepper.set_direction_left()
        picolog.debug(f"DiffDrive::__left - Turning left {radians} radians using {self.__radians_to_steps(radians)} steps")
        self._left_stepper.move(self.__radians_to_steps(radians))
        self._right_stepper.move(self.__radians_to_steps(radians))

    def __right(self, radians: float):
        """Rotational motion to the right"""
        if radians <= 0:
            picolog.debug(f"DiffDrive::__right - Radians must be greater than zero")
            return
        self.__configure_rotational_velocity()
        self._left_stepper.set_direction_right()
        self._right_stepper.set_direction_right()
        picolog.debug(f"DiffDrive::__right - Turning right {radians} radians using {self.__radians_to_steps(radians)} steps")
        self._left_stepper.move(self.__radians_to_steps(radians))
        self._right_stepper.move(self.__radians_to_steps(radians))

    def __circle(self, radius_mm: float, extent_radians: float):
        """Move in a circle of the specified radius and extent."""

        # Ensure the radius is not zero
        if radius_mm == 0:
            picolog.debug(f"DiffDrive::__circle - Radius must be non-zero")
            return
        
        # Ensure the extent is not zero
        if extent_radians == 0:
            picolog.debug(f"DiffDrive::__circle - Extent must be non-zero")
            return

        # Ensure that the absolute radius is greater than the half the axel distance
        if abs(radius_mm) >= (self._axel_distance_mm / 2):
            self.__circle_big(radius_mm, extent_radians)
        else:
            self.__circle_small(radius_mm, extent_radians)
            return
        
    def __circle_big(self, radius_mm: float, extent_radians: float):
        """Move the fulcrum of the wheel axle in a circle of the specified radius and extent (when the radius is equal or greater to the half the wheel axle distance)."""
        if abs(radius_mm) < (self._axel_distance_mm / 2):
            picolog.debug(f"DiffDrive::__circle_big - Radius must be greater than or equal to the axel distance")
            return
        
        picolog.debug(f"DiffDrive::__circle_big - Moving in a circle with radius {radius_mm} mm and extent {math.degrees(extent_radians)} degrees")
        # If the radius is positive the outer wheel is the left wheel
        if radius_mm > 0:
            outer_stepper = self._left_stepper
            inner_stepper = self._right_stepper
            picolog.debug(f"DiffDrive::__circle_big - Moving in a circle to the left, left motor is outer and right motor is inner")
        else:
            outer_stepper = self._right_stepper
            inner_stepper = self._left_stepper
            picolog.debug(f"DiffDrive::__circle_big - Moving in a circle to the right, right motor is outer and left motor is inner")

        # Calculate the outer and inner wheel distances
        outer_distance = abs(radius_mm) * (extent_radians * 2)
        inner_distance = (abs(radius_mm) - (self._axel_distance_mm / 2)) * (extent_radians * 2)

        # Set the target speed and acceleration of the outer wheel to the maximum allowed
        self.__configure_rotational_velocity()
        outer_stepper.set_target_speed_sps(self.__mm_to_steps(self._rotational_target_speed_mmps))
        outer_stepper.set_acceleration_spsps(self.__mm_to_steps(self._rotational_acceleration_mmpss))

        # Calculate the inner wheel speed and acceleration to match the movement time of the outer wheel
        inner_speed = (inner_distance / outer_distance) * self._rotational_target_speed_mmps
        inner_acceleration = (inner_distance / outer_distance) * self._rotational_acceleration_mmpss

        # Set the target speed and acceleration of the inner wheel
        inner_stepper.set_target_speed_sps(self.__mm_to_steps(inner_speed))
        inner_stepper.set_acceleration_spsps(self.__mm_to_steps(inner_acceleration))

        # If extent is positive, both wheels move forwards
        if extent_radians > 0:
            outer_stepper.set_direction_forwards()
            inner_stepper.set_direction_forwards()
        else:
            outer_stepper.set_direction_backwards()
            inner_stepper.set_direction_backwards()

        # Ensure steps are positive
        outer_distance = abs(outer_distance)
        inner_distance = abs(inner_distance)

        # Move the outer and inner wheels
        outer_stepper.move(self.__mm_to_steps(outer_distance))
        inner_stepper.move(self.__mm_to_steps(inner_distance))

    def __circle_small(self, radius_mm: float, extent_radians: float):
        """Move the fulcrum of the wheel axle in a circle of the specified radius and extent
        (when the radius describes the path of the midpoint between the wheels and is smaller 
        than half the axle distance, requiring opposite rotation for the inner wheel)."""

        if abs(radius_mm) >= (self._axel_distance_mm / 2):
            picolog.debug(f"DiffDrive::__circle_small - Radius must be smaller than half the axle distance")
            return

        picolog.debug(f"DiffDrive::__circle_small - Moving in a circle with radius {radius_mm} mm and extent {math.degrees(extent_radians)} degrees")

        # Determine which wheel is inner and which is outer
        if radius_mm > 0:
            outer_stepper = self._left_stepper
            inner_stepper = self._right_stepper
            picolog.debug(f"DiffDrive::__circle_small - Moving in a tight circle to the left, left motor is outer and right motor is inner")
        else:
            outer_stepper = self._right_stepper
            inner_stepper = self._left_stepper
            picolog.debug(f"DiffDrive::__circle_small - Moving in a tight circle to the right, right motor is outer and left motor is inner")

        # Calculate the actual radii for the inner and outer wheels
        outer_radius = abs(radius_mm) + (self._axel_distance_mm / 2)
        inner_radius = abs(radius_mm) - (self._axel_distance_mm / 2)

        # Calculate the distances traveled by each wheel
        outer_distance = outer_radius * abs(extent_radians)
        inner_distance = inner_radius * abs(extent_radians)

        # Set the target speed and acceleration for the outer wheel
        self.__configure_rotational_velocity()
        picolog.debug(f"DiffDrive::__circle_small - Setting outer stepper target speed to {self._rotational_target_speed_mmps} mm/s and acceleration to {self._rotational_acceleration_mmpss} mm/s^2")
        outer_stepper.set_target_speed_sps(self.__mm_to_steps(self._rotational_target_speed_mmps))
        outer_stepper.set_acceleration_spsps(self.__mm_to_steps(self._rotational_acceleration_mmpss))

        # Calculate the inner wheel speed and acceleration to match the movement time of the outer wheel
        inner_speed = abs((inner_distance / outer_distance) * self._rotational_target_speed_mmps)
        inner_acceleration = abs((inner_distance / outer_distance) * self._rotational_acceleration_mmpss)

        # Set the target speed and acceleration for the inner wheel
        picolog.debug(f"DiffDrive::__circle_small - Setting inner stepper target speed to {inner_speed} mm/s and acceleration to {inner_acceleration} mm/s^2")
        inner_stepper.set_target_speed_sps(self.__mm_to_steps(inner_speed))
        inner_stepper.set_acceleration_spsps(self.__mm_to_steps(inner_acceleration))

        # Handle wheel direction: inner wheel rotates in the opposite direction
        if extent_radians > 0:
            outer_stepper.set_direction_forwards()
            inner_stepper.set_direction_backwards()
            picolog.debug(f"DiffDrive::__circle_small - Outer wheel moves forward, inner wheel moves backward")
        else:
            outer_stepper.set_direction_backwards()
            inner_stepper.set_direction_forwards()
            picolog.debug(f"DiffDrive::__circle_small - Outer wheel moves backward, inner wheel moves forward")

        # Move the outer and inner wheels
        outer_stepper.move(self.__mm_to_steps(abs(outer_distance)))
        inner_stepper.move(self.__mm_to_steps(abs(inner_distance)))

    def set_heading(self, degrees: float):
        """Set the heading in degrees"""
        degrees = degrees % 360

        current_heading_degrees = math.degrees(self._heading_radians)
        if math.isclose(current_heading_degrees, degrees, abs_tol=1e-2):
            picolog.debug(f"DiffDrive::set_heading - Already at required heading ({degrees}°)")
            return

        # Convert degrees to radians
        target_radians = math.radians(degrees)

        # Set the heading
        self.__set_heading(target_radians)

    def __set_heading(self, target_radians: float):
        # Normalize the angle difference to the range [-π, π]
        def normalize_angle(angle):
            return (angle + math.pi) % (2 * math.pi) - math.pi

        angle_difference = normalize_angle(target_radians - self._heading_radians)

        # Determine turning direction
        if angle_difference > 0:
            picolog.debug(f"DiffDrive::__set_heading - Turning left by {math.degrees(angle_difference):.2f}°")
            self.turn_left(math.degrees(angle_difference))
        elif angle_difference < 0:
            picolog.debug(f"DiffDrive::__set_heading - Turning right by {math.degrees(-angle_difference):.2f}°")
            self.turn_right(math.degrees(-angle_difference))

        # Update the heading to the target value
        self._heading_radians = target_radians

    def get_heading(self) -> float:
        """Get the heading in degrees"""
        heading_degrees = round(math.degrees(self._heading_radians), 2) % 360
        return heading_degrees

    def set_cartesian_x_position(self, x: float):
        """Move to the specified x-coordinate"""
        self.set_cartesian_position(x, self._y_pos, False)

    def set_cartesian_y_position(self, y: float):
        """Move to the specified y-coordinate"""
        self.set_cartesian_position(self._x_pos, y, False)

    def turn_towards_cartesian_point(self, x: float, y: float):
        """Turn towards the specified Cartesian point"""
        self.set_cartesian_position(x, y, True)

    def set_cartesian_position(self, x: float, y: float, turn_only: bool = False):
        """Move to the specified x and y coordinates in one motion."""
        if x == self._x_pos and y == self._y_pos:
            picolog.debug("Already at the required position.")
            return

        # Store the current heading
        current_heading = self._heading_radians

        # Calculate the target angle and distance
        delta_x = x - self._x_pos
        delta_y = y - self._y_pos
        target_angle = math.atan2(delta_y, delta_x)
        distance = math.sqrt(delta_x**2 + delta_y**2)

        # Normalize angles to [-pi, pi]
        angle_diff = (target_angle - self._heading_radians + math.pi) % (2 * math.pi) - math.pi

        # Determine the turning direction based on the angle difference
        # Note: Always turn towards the position (facing forwards) if turn_only is True
        if abs(angle_diff) > math.pi / 2 and not turn_only: 
            # Backward movement
            turn_angle = math.pi - abs(angle_diff)
            turn_angle *= -1 if angle_diff > 0 else 1

            if angle_diff > 0:
                self.__right(abs(turn_angle))
            else:
                self.__left(abs(turn_angle))

            self._heading_radians = (self._heading_radians + turn_angle) % (2 * math.pi)

            picolog.debug("Waiting for turn to complete (backward).")
            while self._left_stepper.is_busy or self._right_stepper.is_busy:
                pass

            if not turn_only:
                self.drive_backward(distance)

                picolog.debug("Waiting for movement to complete (backward).")
                while self._left_stepper.is_busy or self._right_stepper.is_busy:
                    pass

                # Restore the original heading
                self.__set_heading(current_heading)                
        else:
            # Forward movement
            if angle_diff > 0:
                self.__left(angle_diff)
            else:
                self.__right(-angle_diff)

            self._heading_radians = (self._heading_radians + angle_diff) % (2 * math.pi)

            picolog.debug("Waiting for turn to complete (forward).")
            while self._left_stepper.is_busy or self._right_stepper.is_busy:
                pass

            if not turn_only:
                self.drive_forward(distance)

                picolog.debug("Waiting for movement to complete (forward).")
                while self._left_stepper.is_busy or self._right_stepper.is_busy:
                    pass

                # Restore the original heading
                self.__set_heading(current_heading) 

    def get_cartesian_position(self) -> tuple:
        """Get the Cartesian x and y position"""
        return round(self._x_pos, 2), round(self._y_pos, 2)

    def reset_origin(self):
        """Reset the Cartesian origin and heading to the current position"""
        picolog.debug(f"DiffDrive::reset_origin - Resetting origin and heading")
        self._x_pos = 0
        self._y_pos = 0
        self._heading_radians = 0

    def __configure_linear_velocity(self):
        """Configure the steppers for the linear velocity"""
        self._left_stepper.set_target_speed_sps(self.__mm_to_steps(self._linear_target_speed_mmps))
        self._left_stepper.set_acceleration_spsps(self.__mm_to_steps(self._linear_acceleration_mmpss))
        self._right_stepper.set_target_speed_sps(self.__mm_to_steps(self._linear_target_speed_mmps))
        self._right_stepper.set_acceleration_spsps(self.__mm_to_steps(self._linear_acceleration_mmpss))

    def __configure_rotational_velocity(self):
        """Configure the steppers for the rotational velocity"""
        self._left_stepper.set_target_speed_sps(self.__mm_to_steps(self._rotational_target_speed_mmps))
        self._left_stepper.set_acceleration_spsps(self.__mm_to_steps(self._rotational_acceleration_mmpss))
        self._right_stepper.set_target_speed_sps(self.__mm_to_steps(self._rotational_target_speed_mmps))
        self._right_stepper.set_acceleration_spsps(self.__mm_to_steps(self._rotational_acceleration_mmpss))

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

        if self._left_stepper.is_busy:
            if self._left_stepper.direction:
                left_stepper_status = 1
            else:
                left_stepper_status = 2

            if self._right_stepper.direction:
                right_stepper_status = 1
            else:
                right_stepper_status = 2

        return left_stepper_status, right_stepper_status
    
    # Convert millimeters to steps
    def __mm_to_steps(self, millimeters: float) -> int:
        circumference = self._pi * (self._wheel_diameter_mm + (self._wheel_calibration_um / 1000))
        millimeters_per_step = (circumference / self._steps_per_revolution)
        return int(millimeters / millimeters_per_step)
    
    # Convert radians to steps
    def __radians_to_steps(self, radians: float) -> int:
        """Convert radians to steps"""
        circumference = self._pi * (self._axel_distance_mm + (self._axel_calibration_um / 1000))
        millimeters = (circumference / (2 * self._pi)) * radians
        return self.__mm_to_steps(millimeters)
    
if __name__ == "__main__":
    from main import main
    main()