#************************************************************************ 
#
#   cat.py
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

class Cat():
    def __init__(self, t: TurtleInterface, speed: int):
        self._t = t
        self._speed = speed

    def render(self):
        # Connect
        self._t.connect()
        self._t.motors(True)
        self._t.speed(self._speed)
        self._t.eyes(0, 0, 255, 0)
        
        # Draw the head (circle)
        self._t.penup()
        self._t.goto(0, 50)
        self._t.pendown()
        self._t.circle(50, 360)

        # Draw the left ear (triangle pointing upwards)
        self._t.penup()
        self._t.goto(-40, 150 + 30)
        self._t.pendown()
        self._t.goto(-50, 100 + 30)
        self._t.goto(-10, 100 + 30)
        self._t.goto(-40, 150 + 30)

        # Draw the right ear (triangle pointing upwards)
        self._t.penup()
        self._t.goto(40, 150 + 30)
        self._t.pendown()
        self._t.goto(50, 100 + 30)
        self._t.goto(10, 100 + 30)
        self._t.goto(40, 150 + 30)

        # Draw the eyes (small circles)
        self._t.penup()
        self._t.goto(-20, 100)
        self._t.pendown()
        self._t.circle(10, 360)
        self._t.penup()
        self._t.goto(20, 100)
        self._t.pendown()
        self._t.circle(10, 360)

        # Draw the nose (triangle)
        self._t.penup()
        self._t.goto(0, 90)
        self._t.pendown()
        self._t.goto(-10, 80)
        self._t.goto(10, 80)
        self._t.goto(0, 90)

        # Draw the mouth (lines)
        self._t.penup()
        self._t.goto(0, 80)
        self._t.setheading(315)
        self._t.pendown()
        self._t.forward(15)
        self._t.penup()
        self._t.goto(0, 80)
        self._t.setheading(225)
        self._t.pendown()
        self._t.forward(15)

        # Draw the whiskers (lines)
        for angle in [200, 180, 160]:
            self._t.penup()
            self._t.goto(-10, 85)
            self._t.setheading(angle)
            self._t.pendown()
            self._t.forward(60)

        for angle in [340, 0, 20]:
            self._t.penup()
            self._t.goto(10, 85)
            self._t.setheading(angle)
            self._t.pendown()
            self._t.forward(60)

        # Draw the body (ellipse-like shape)
        self._t.penup()
        self._t.goto(0, 0)
        self._t.pendown()
        self._t.setheading(270)
        for _ in range(2):
            self._t.circle(50, 90)
            self._t.circle(100, 90)

        # Draw the tail (curved line)
        self._t.penup()
        self._t.goto(50, -50)
        self._t.setheading(120)
        self._t.pendown()
        self._t.circle(40, 200)

        self._t.penup()

        # Clean up
        self._t.motors(False)
        self._t.eyes(0, 0, 0, 0)
        self._t.disconnect()