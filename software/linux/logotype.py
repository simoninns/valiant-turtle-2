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
    def __init__(self, t: TurtleInterface, speed: int):
        self._t = t
        self._speed = speed

    def pentagon_points(self, radius, index):
        angle = math.radians(72 * index)
        x = radius * math.sin(angle)
        y = -radius * math.cos(angle)
        return (x, y)
    
    def dodecagon_points(self, radius, index):
        angle = math.radians(36 * index)
        x = radius * math.sin(angle)
        y = -radius * math.cos(angle)
        return (x, y)

    def draw_spokes(self, pentagon_radius, dodecagon_radius):
        # Draw lines from each point of the pentagon to the dodecagon

        # Draw lines from pentagon points to dodecagon points
        for i in range(5):
            self._t.penup()
            self._t.towards(self.pentagon_points(pentagon_radius, i)[0], self.pentagon_points(pentagon_radius, i)[1])
            self._t.goto(self.pentagon_points(pentagon_radius, i))

            self._t.towards(self.dodecagon_points(dodecagon_radius, 2 * i)[0], self.dodecagon_points(dodecagon_radius, 2 * i)[1])
            self._t.pendown()
            self._t.goto(self.dodecagon_points(dodecagon_radius, 2 * i))

        self._t.penup()
    
    def move_to_dodecagon_line_fraction(self, dodecagon_radius, side: int, fraction: float):
        # Calculate the fractional point along a line of the dodecagon
        x1, y1 = self.dodecagon_points(dodecagon_radius, side)
        x2, y2 = self.dodecagon_points(dodecagon_radius, (side + 1) % 10)
        x_frac = x1 + fraction * (x2 - x1)
        y_frac = y1 + fraction * (y2 - y1)
        self._t.goto(x_frac, y_frac)
        return x_frac, y_frac

    def draw_head(self):
        # Calculate the coordinates of the first midpoint
        x1, y1 = self.dodecagon_points(130, 4)
        x2, y2 = self.dodecagon_points(130, 5)
        x_mid1 = (x1 + x2) / 2
        y_mid1 = (y1 + y2) / 2

        # Calculate the coordinates of the second midpoint
        x3, y3 = self.dodecagon_points(130, 5)
        x4, y4 = self.dodecagon_points(130, 6)
        x_mid2 = (x3 + x4) / 2
        y_mid2 = (y3 + y4) / 2

        # Start the continuous path at the first midpoint
        self._t.penup()
        self._t.goto(x_mid1, y_mid1)

        # Draw the head shape in a continuous path
        self._t.setheading(90)
        self._t.pendown()
        self._t.forward(40)  # Line upward from first midpoint
        self._t.goto(0, 200)  # Line to the center of the head
        self._t.goto(x_mid2, y_mid2 + 40)  # Line to the second midpoint
        self._t.setheading(90)  # Face upward
        self._t.backward(40)  # Line downward to complete the path
        
        self._t.penup()

    def back_flipper_right(self):
        self.move_to_dodecagon_line_fraction(130, 1, 0)
        self._t.setheading(90 + 36)
        self._t.pendown()
        self._t.backward(50)
        self._t.setheading(10)
        self._t.forward(45)
        self._t.setheading(90)
        self._t.forward(130)
        self.move_to_dodecagon_line_fraction(130, 2, 0.5)
        self._t.penup()

    def back_flipper_left(self):
        self.move_to_dodecagon_line_fraction(130, 9, 0)
        self._t.setheading(90 - 36)
        self._t.pendown()
        self._t.backward(50)
        self._t.setheading(170)
        self._t.forward(45)
        self._t.setheading(90)
        self._t.forward(130)
        self.move_to_dodecagon_line_fraction(130, 7, 0.5)
        self._t.penup()

    def front_flipper_right(self):
        self.move_to_dodecagon_line_fraction(130, 3, 0.25)
        self._t.setheading(36)
        self._t.pendown()
        
        self._t.forward(48)
        self._t.setheading(90)
        self._t.forward(46)
        self._t.left(80)
        self._t.forward(60)

        self.move_to_dodecagon_line_fraction(130, 4, 0.25)
        self._t.penup()

    def front_flipper_left(self):
        self.move_to_dodecagon_line_fraction(130, 6, 0.75)
        self._t.setheading(36 * 4)
        self._t.pendown()
        
        self._t.forward(48)
        self._t.setheading(90)
        self._t.forward(46)
        self._t.right(80)
        self._t.forward(60)

        self.move_to_dodecagon_line_fraction(130, 5, 0.75)
        self._t.penup()

    def render(self):
        # Connect
        self._t.connect()
        self._t.speed(self._speed)
        self._t.motors(True)
        self._t.eyes(0, 0, 255, 0)

        # Central pentagon
        self._t.penup()
        self._t.goto(0, -75)
        self._t.pendown()
        self._t.circle(75, steps=5)

        # Dodecagon
        self._t.penup()
        self._t.goto(0, -130)
        self._t.pendown()
        self._t.circle(130, steps=10)
        self._t.penup()

        # Draw spokes
        self.draw_spokes(75, 130)

        # Draw back flippers
        self.back_flipper_left()
        self.back_flipper_right()

        # Draw front flippers
        self.front_flipper_right()
        self.front_flipper_left()

        # Draw head
        self.draw_head()

        self._t.penup()
        self._t.goto(300, 0)
        self._t.setheading(0)
                    
        # Disconnect
        self._t.motors(False)
        self._t.eyes(0, 0, 0, 0)
        self._t.disconnect()