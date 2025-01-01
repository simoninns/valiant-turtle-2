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

    def logo_flippers(self):
        back_flipper = [
            ([0, 13], [1, 15]),
            ([1, 15], [13, 15]),
            ([13, 15], [13.5, 11]),
            ([13.5, 11], [10, 7.5])
        ]

        front_flipper = [
            ([-6, 11], [-9, 15]),
            ([-9, 15], [-13, 15]),
            ([-13, 15], [-14, 9]),
            ([-14, 9], [-10.75, 6.25])
        ]

        def draw_path(path, flip_y=False):
            if flip_y:
                path = [([x[0], -x[1]], [y[0], -y[1]]) for x, y in path]

            # Move to the starting point without drawing
            start_point = path[0][0]
            self._t.penup()
            self._t.goto(start_point[0] * self._scale, start_point[1] * self._scale)
            self._t.pendown()

            # Draw the path
            for start, end in path:
                dx = end[0] - start[0]
                dy = end[1] - start[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                angle = math.degrees(math.atan2(dy, dx))

                self._t.setheading(angle)
                self._t.forward(distance * self._scale)

        # Draw the lower back flipper
        draw_path(back_flipper, flip_y=True)

        # Draw the lower front flipper
        draw_path(front_flipper, flip_y=True)

        # Draw the upper front flipper
        draw_path(front_flipper, flip_y=False)

         # Draw the upper back flipper
        draw_path(back_flipper, flip_y=False)

    def logo_head(self):
        coordinates = [
            # Head
            ([-12.5 + 0.125, 3], [-16, 3]),
            ([-16, 3], [-19, 0]),
            ([-19, 0], [-16, -3]),
            ([-16, -3], [-12.5 + 0.125, -3])
        ]

        def move_and_draw(start, end):
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            angle = math.degrees(math.atan2(dy, dx))

            self._t.setheading(angle)
            self._t.forward(distance * self._scale)

        # Move to the starting point without drawing
        start_point = coordinates[0][0]
        self._t.penup()
        self._t.setheading(0)
        self._t.setposition(start_point[0] * self._scale, start_point[1] * self._scale)
        self._t.pendown()

        # Draw the head in one continuous path
        for start, end in coordinates:
            move_and_draw(start, end)

    def draw_rotated_pentagon(self, radius, rotation_angle):
        # Save the current heading and position
        self._t.penup()

        # Move the turtle to the center of the pentagon
        # In a regular pentagon, the center is effectively the origin
        self._t.goto(0, 0)

        # Adjust the turtle to start at the bottom edge of the pentagon
        self._t.setheading(-90 + rotation_angle)  # Point to the bottom of the pentagon and apply rotation
        self._t.forward(radius * self._scale)  # Move to the starting edge of the pentagon

        # Draw the pentagon using the circle method
        self._t.setheading(rotation_angle)  # Set the turtle's heading to the rotation angle
        self._t.pendown()
        self._t.circle(radius * self._scale, steps=5)
        self._t.penup()

        # Return the turtle to the center of the pentagon
        self._t.goto(0, 0)

    def roman_numerals(self):
        # Roman numeral II
        self._t.penup()
        self._t.setheading(90)  # Point upwards

        # Draw first vertical line
        self._t.goto(1.5 * self._scale, -2.5 * self._scale)
        self._t.pendown()
        self._t.forward(5 * self._scale)

        # Move to second vertical line position
        self._t.penup()
        self._t.goto(-1.5 * self._scale, -2.5 * self._scale)
        self._t.pendown()
        self._t.forward(5 * self._scale)

        # Draw horizontal lines
        self._t.penup()
        self._t.goto(-3 * self._scale, 2.5 * self._scale)  # Top horizontal line start
        self._t.setheading(0)  # Face right
        self._t.pendown()
        self._t.forward(6 * self._scale)

        self._t.penup()
        self._t.goto(-3 * self._scale, -2.5 * self._scale)  # Bottom horizontal line start
        self._t.pendown()
        self._t.forward(6 * self._scale)

    def render(self):
        # Connect
        self._t.connect()
        self._t.speed(0)
        self._t.motors(True)

        # Dodecagon
        self._t.penup()
        self._t.goto(0, -13 * self._scale)
        self._t.pendown()
        self._t.circle(13 * self._scale, steps=10)

        # Inter pentagon
        self.draw_rotated_pentagon(7.5, 36/2)

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
        self._t.goto(0, 0)
        self._t.setheading(180)
        self._t.forward(300)

        self._t.motors(False)
        self._t.disconnect()