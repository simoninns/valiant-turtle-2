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
    def __init__(self, wheel_diameter_mm = 54.0, axel_distance_mm = 230.0, steps_per_revolution = 800):
        self.wheel_diameter_mm = wheel_diameter_mm
        self.axel_distance_mm = axel_distance_mm
        self.steps_per_revolution = steps_per_revolution
        self.pi = 3.14159

    # Convert millimeters to steps
    def mm_to_steps(self, millimeters) -> int:
        circumference = (2.0 * self.pi) * (self.wheel_diameter_mm / 2.0) # C = 2pi x r 
        mm_per_step = (circumference / self.steps_per_revolution)
        return int(millimeters / mm_per_step)

    # Convert degrees to steps
    # Note: This is only for when the robot turns on it's axis
    def degrees_to_steps(self, degrees) -> int:
        circumference = (2.0 * self.pi) * (self.axel_distance_mm / 2.0)
        millimeters = (circumference / 360.0) * degrees
        return self.mm_to_steps(millimeters)
    
if __name__ == "__main__":
    from main import main
    main()