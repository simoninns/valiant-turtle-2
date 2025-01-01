#************************************************************************ 
#
#   logotype.py
#
#   Draw the Valiant Turtle 2 logo using the turtle graphics library
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

import math
from abstract_turtle import TurtleInterface

class Logotype():
    def __init__(self, scale, t: TurtleInterface):
        self._scale = scale
        self._t = t

    def draw_line(self, start, end):
        self._t.penup()
        self._t.goto(start[0] * self._scale, start[1] * self._scale)
        self._t.pendown()
        self._t.goto(end[0] * self._scale, end[1] * self._scale)

    def logo_flippers(self):
        coordinates = [
            # Back flipper
            ([0, 13], [1, 15]),
            ([1, 15], [13, 15]),
            ([13, 15], [13.5, 11]),
            ([13.5, 11], [10, 7.5]),

            # Front flipper
            ([-6, 11], [-9, 15]),
            ([-9, 15], [-13, 15]),
            ([-13, 15], [-14, 9]),
            ([-14, 9], [-10.75, 6.25])
        ]
        
        for start, end in coordinates:
            self.draw_line([start[0], -start[1]], [end[0], -end[1]])

        for start, end in coordinates:
            self.draw_line(start, end)

    def logo_head(self):
        coordinates = [
            # Head
            ([-12.5 + 0.125, 3], [-16, 3]),
            ([-16, 3], [-19, 0]),
            ([-19, 0], [-16, -3]),
            ([-16, -3], [-12.5 + 0.125, -3])
        ]
        
        for start, end in coordinates:
            self.draw_line(start, end)

    def draw_rotated_pentagon(self, radius, rotation_angle):
        angle = math.radians(rotation_angle)
        points = []
        for i in range(5):
            x = radius * math.cos(2 * math.pi * i / 5 + angle)
            y = radius * math.sin(2 * math.pi * i / 5 + angle)
            points.append((x, y))
        self._t.penup()
        self._t.goto(points[0][0] * self._scale, points[0][1] * self._scale)
        self._t.pendown()
        for point in points[1:]:
            self._t.goto(point[0] * self._scale, point[1] * self._scale)
        self._t.goto(points[0][0] * self._scale, points[0][1] * self._scale)
        return points

    def roman_numerals(self):
        # Roman numeral II
        # Horizontal lines
        self._t.penup()
        self._t.goto(1.5 * self._scale, -2.5 * self._scale)
        self._t.pendown()
        self._t.setheading(90)
        self._t.forward(5 * self._scale)
        self._t.penup()
        self._t.goto(-1.5 * self._scale, -2.5 * self._scale)
        self._t.pendown()
        self._t.forward(5 * self._scale)

        # Vertical lines
        self._t.penup()
        self._t.goto(-3 * self._scale, 2.5 * self._scale)
        self._t.pendown()
        self._t.goto(3 * self._scale, 2.5 * self._scale)
        self._t.penup()
        self._t.goto(-3 * self._scale, -2.5 * self._scale)
        self._t.pendown()
        self._t.goto(3 * self._scale, -2.5 * self._scale)

    def render(self):
        # Connect
        self._t.connect()
        self._t.motors(True)

        # Dodecagon
        self._t.penup()
        self._t.goto(0, -13 * self._scale)
        self._t.pendown()
        self._t.circle(13 * self._scale, steps=10)

        # Inter pentagon
        pentagon_points = self.draw_rotated_pentagon(7.5, 0)

        # Spokes
        for rota in range(0, 360, 72):
            self._t.penup()
            self._t.goto(0, 0)
            self._t.setheading(rota)
            self._t.forward(7.5 * self._scale)
            self._t.pendown()
            self._t.forward((4.75+0.125) * self._scale)

        # Roman numerals
        self.roman_numerals()

        # Head
        self.logo_head()

        # Flippers
        self.logo_flippers()

        # Clean up
        self._t.penup()
        self._t.motors(False)
        self._t.disconnect()