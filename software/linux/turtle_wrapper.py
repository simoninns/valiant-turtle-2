#************************************************************************ 
#
#   turtle_wrapper.py
#
#   A turtle wrapper class to simplify the turtle commands
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

from commands_tx import CommandsTx
import time

class TurtleWrapper:
    def __init__(self):
        self._commands_tx = CommandsTx()
        self._pen_down = False
        self._angle = 0
        self._x = 0
        self._y = 0

    def connect(self):
        self._commands_tx.connect()
        while not self._commands_tx.connected:
            time.sleep(1)
        self._commands_tx.eyes(0, 0, 0, 255)

    def disconnect(self):
        self._commands_tx.eyes(0, 0, 0, 0)
        self._commands_tx.disconnect()

    def penup(self):
        self._pen_down = False
        self._commands_tx.eyes(0, 0, 255, 0)
        self._commands_tx.penup()

    def pendown(self):
        self._pen_down = True
        self._commands_tx.eyes(0, 255, 0, 0)
        self._commands_tx.pendown()

    def goto(self, x, y):
        self._commands_tx.setposition(x, y)

    def forward(self, distance):
        self._commands_tx.forward(distance)

    def backward(self, distance):
        self._commands_tx.backward(distance)

    def setheading(self, angle):
        self._angle = angle % 360
        self._commands_tx.setheading(self._angle)

    def right(self, angle):
        self._commands_tx.right(angle)

    def left(self, angle):
        self._commands_tx.left(angle)

    def circle(self, radius, extent=360):
        self._commands_tx.circle(radius, extent)

    def position(self):
        _, self._x, self._y = self._commands_tx.position()
        return self._x, self._y

    def heading(self):
        _, self._angle = self._commands_tx.heading()
        return self._angle

    def motors_on(self):
        self._commands_tx.motors(True)

    def motors_off(self):
        self._commands_tx.motors(False)