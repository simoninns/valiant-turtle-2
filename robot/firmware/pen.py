#************************************************************************ 
#
#   pen.py
#
#   Control the pen lift mechanism
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

from servo import Servo

class Pen:
    def __init__(self, pin):
        # Initialise the pen servo to off
        self.servo = Servo(pin)
        self.servo.set_power(False)

    def up(self):
        self.servo.set_position(90)
        self.servo.set_power(True)
    
    def down(self):
        self.servo.set_position(0)
        self.servo.set_power(True)

    def off(self):
        self.servo.set_power(False)