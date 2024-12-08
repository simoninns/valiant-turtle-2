#************************************************************************ 
#
#   metric.py
#
#   Functions to convert metric measurements into stepper steps
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

class Metric:
    """
    A class to represent the metric measurements and conversions for the robot's movement.
    Attributes
    ----------
    wheel_diameter_mm : float
        Diameter of the wheel in millimeters.
    axel_distance_mm : float
        Distance between the two wheels (axel distance) in millimeters.
    steps_per_revolution : int
        Number of steps per one full revolution of the wheel.
    pi : float
        Value of Pi used for calculations.
    Methods
    -------
    mm_to_steps(millimeters) -> int:
        Converts a distance in millimeters to the equivalent number of steps.
    degrees_to_steps(degrees) -> int:
        Converts an angle in degrees to the equivalent number of steps for the robot to turn on its axis.
    """

    def __init__(self, wheel_diameter_mm = 55.53, axel_distance_mm = 224.0, steps_per_revolution = 800):
        """
        Initialize the Metric class with given parameters.
        Args:
            wheel_diameter_mm (float): Diameter of the wheel in millimeters. Default is 55.53 mm.
            axel_distance_mm (float): Distance between the axles in millimeters. Default is 230.0 mm.
            steps_per_revolution (int): Number of steps per revolution of the wheel. Default is 800.
        """

        self._wheel_diameter_mm = wheel_diameter_mm
        self._axel_distance_mm = axel_distance_mm
        self._steps_per_revolution = steps_per_revolution
        self._pi = 3.14159

        # Calibration values (in micrometers / 1000th of a mm)
        self._wheel_calibration = 0
        self._axel_calibration = 0

    def get_wheel_calibration(self):
        return self._wheel_calibration * 1000 # Convert to um
    
    def set_wheel_calibration(self, value: float):
        self._wheel_calibration = value / 1000 # Convert to mm
        logging.debug(f"Metric::set_wheel_calibration: Wheel diameter calibration set to {value} um (total wheel diameter: {self._wheel_diameter_mm + self._wheel_calibration} mm)")

    def get_axel_calibration(self) -> float:
        return self._axel_calibration * 1000 # Convert to um
    
    def set_axel_calibration(self, value: float):
        self._axel_calibration = value / 1000 # Convert to mm
        logging.debug(f"Metric::set_wheel_calibration: Axel distance calibration set to {value} um (total axel distance: {self._axel_distance_mm + self._axel_calibration} mm)")

    # Convert millimeters to steps
    def mm_to_steps(self, millimeters: float) -> int:
        """
        Convert millimeters to motor steps.
        This method calculates the number of motor steps required to cover a given distance in millimeters.
        It uses the wheel diameter and the number of steps per revolution to perform the conversion.
        Args:
            millimeters (float): The distance in millimeters to be converted to steps.
        Returns:
            int: The number of motor steps corresponding to the given distance in millimeters.
        """

        circumference = (2.0 * self._pi) * ((self._wheel_diameter_mm + self._wheel_calibration) / 2.0) # C = 2pi x r 
        millimeters_per_step = (circumference / self._steps_per_revolution)
        return int(millimeters / millimeters_per_step)
    
    def steps_to_mm(self, steps: int) -> float:
        """
        Convert motor steps to millimeters.
        This method calculates the distance in millimeters covered by a given number of motor steps.
        It uses the wheel diameter and the number of steps per revolution to perform the conversion.
        Args:
            steps (int): The number of motor steps to be converted to millimeters.
        Returns:
            float: The distance in millimeters covered by the given number of motor steps.
        """

        circumference = (2.0 * self._pi) * ((self._wheel_diameter_mm + self._wheel_calibration) / 2.0)
        millimeters_per_step = (circumference / self._steps_per_revolution)
        return steps * millimeters_per_step

    # Convert degrees to steps
    # Note: This is only for when the robot turns on it's axis
    def degrees_to_steps(self, degrees: float) -> int:
        """
        Convert degrees of rotation to motor steps.
        Args:
            degrees (float): The number of degrees to convert.
        Returns:
            int: The equivalent number of motor steps.
        """

        circumference = (2.0 * self._pi) * ((self._axel_distance_mm + self._axel_calibration) / 2.0)
        millimeters = (circumference / 360.0) * degrees
        return self.mm_to_steps(millimeters)
    
    # Convert steps to degrees
    # Note: This is only for when the robot turns on it's axis
    def steps_to_degrees(self, steps: int) -> float:
        """
        Convert motor steps to degrees of rotation.
        Args:
            steps (int): The number of motor steps to convert.
        Returns:
            float: The equivalent number of degrees of rotation.
        """

        circumference = (2.0 * self._pi) * ((self._axel_distance_mm + self._axel_calibration) / 2.0)
        millimeters = self.steps_to_mm(steps)
        return (millimeters / circumference) * 360.0
    
if __name__ == "__main__":
    from main import main
    main()