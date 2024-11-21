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

    def __init__(self, wheel_diameter_mm = 54.0, axel_distance_mm = 230.0, steps_per_revolution = 800):
        """
        Initialize the Metric class with given parameters.
        Args:
            wheel_diameter_mm (float): Diameter of the wheel in millimeters. Default is 54.0 mm.
            axel_distance_mm (float): Distance between the axles in millimeters. Default is 230.0 mm.
            steps_per_revolution (int): Number of steps per revolution of the wheel. Default is 800.
        """

        self.wheel_diameter_mm = wheel_diameter_mm
        self.axel_distance_mm = axel_distance_mm
        self.steps_per_revolution = steps_per_revolution
        self.pi = 3.14159

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

        circumference = (2.0 * self.pi) * (self.wheel_diameter_mm / 2.0) # C = 2pi x r 
        millimeters_per_step = (circumference / self.steps_per_revolution)
        return int(millimeters / millimeters_per_step)

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

        circumference = (2.0 * self.pi) * (self.axel_distance_mm / 2.0)
        millimeters = (circumference / 360.0) * degrees
        return self.mm_to_steps(millimeters)
    
if __name__ == "__main__":
    from main import main
    main()