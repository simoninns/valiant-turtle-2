#************************************************************************ 
#
#   calitest.py
#
#   Draw a cat using the turtle graphics library
#   Valiant Turtle 2 - Communicator Linux Firmware
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

from abstract_turtle import TurtleInterface

class Calitest1():
    """
    A calibration test designed to test the accuracy of the turtle's movement when
    performing linear and rotational movements (but not circular movements).
    """
    def __init__(self, t: TurtleInterface, speed: int):
        self._t = t
        self._speed = speed

    def render(self):
        # Connect
        self._t.connect()
        self._t.motors(True)
        self._t.speed(self._speed)
        self._t.eyes(0, 0, 255, 0)
        
        repeats = 6

        step = 360 / repeats
        for t in range(0, 360, int(step)):
            self._t.pendown()
            for i in range(3):
                self._t.forward(100)
                self._t.left(90)
            self._t.forward(100)

            # self._t.penup()
            # self._t.forward(50)
            # self._t.pendown()
            # self._t.circle(50, 360)
            # self._t.penup()
            # self._t.backward(50)

            self._t.right((360/repeats) - 90)

        # Clean up
        self._t.penup()
        self._t.motors(False)
        self._t.eyes(0, 0, 0, 0)
        self._t.disconnect()

class Calitest2():
    """
    A calibration test designed to test the accuracy of the turtle's movement when
    performing linear, rotational and circular movements.
    """
    def __init__(self, t: TurtleInterface, speed: int):
        self._t = t
        self._speed = speed

    def render(self):
        # Connect
        self._t.connect()
        self._t.motors(True)
        self._t.speed(self._speed)
        self._t.eyes(0, 0, 255, 0)
        
        repeats = 6

        step = 360 / repeats
        for t in range(0, 360, int(step)):
            self._t.pendown()
            for i in range(4):
                self._t.forward(100)
                self._t.left(90)

            self._t.penup()
            self._t.forward(50)
            self._t.pendown()
            self._t.circle(50, 360)
            self._t.penup()
            self._t.backward(50)

            self._t.right((360/repeats))

        # Clean up
        self._t.penup()
        self._t.motors(False)
        self._t.eyes(0, 0, 0, 0)
        self._t.disconnect()