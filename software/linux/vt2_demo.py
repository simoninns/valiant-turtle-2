#************************************************************************ 
#
#   vt2_demo.py
#
#   Demonstration
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
import logging
import time
import sys
from turtle_wrapper import TurtleWrapper
import turtle

def draw_simple_cat(turtle):
    # Draw the head (circle)
    turtle.penup()
    turtle.goto(0, 50)
    turtle.pendown()
    turtle.circle(50, 360)

    # Draw the left ear (triangle pointing upwards)
    turtle.penup()
    turtle.goto(-40, 150 + 30)
    turtle.pendown()
    turtle.goto(-50, 100 + 30)
    turtle.goto(-10, 100 + 30)
    turtle.goto(-40, 150 + 30)

    # Draw the right ear (triangle pointing upwards)
    turtle.penup()
    turtle.goto(40, 150 + 30)
    turtle.pendown()
    turtle.goto(50, 100 + 30)
    turtle.goto(10, 100 + 30)
    turtle.goto(40, 150 + 30)

    # Draw the eyes (small circles)
    turtle.penup()
    turtle.goto(-20, 100)
    turtle.pendown()
    turtle.circle(10, 360)
    turtle.penup()
    turtle.goto(20, 100)
    turtle.pendown()
    turtle.circle(10, 360)

    # Draw the nose (triangle)
    turtle.penup()
    turtle.goto(0, 90)
    turtle.pendown()
    turtle.goto(-10, 80)
    turtle.goto(10, 80)
    turtle.goto(0, 90)

    # Draw the mouth (lines)
    turtle.penup()
    turtle.goto(0, 80)
    turtle.setheading(315)
    turtle.pendown()
    turtle.forward(15)
    turtle.penup()
    turtle.goto(0, 80)
    turtle.setheading(225)
    turtle.pendown()
    turtle.forward(15)

    # Draw the whiskers (lines)
    for angle in [200, 180, 160]:
        turtle.penup()
        turtle.goto(-10, 85)
        turtle.setheading(angle)
        turtle.pendown()
        turtle.forward(60)

    for angle in [340, 0, 20]:
        turtle.penup()
        turtle.goto(10, 85)
        turtle.setheading(angle)
        turtle.pendown()
        turtle.forward(60)

    # Draw the body (ellipse-like shape)
    turtle.penup()
    turtle.goto(0, 0)
    turtle.pendown()
    turtle.setheading(270)
    for _ in range(2):
        turtle.circle(50, 90)
        turtle.circle(100, 90)

    # Draw the tail (curved line)
    turtle.penup()
    turtle.goto(50, -50)
    turtle.setheading(120)
    turtle.pendown()
    turtle.circle(40, 200)

    turtle.penup()

# Call this to use the real robot
def main_physical():
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
    turtle = TurtleWrapper()

    try:
        turtle.connect()
        logging.info("Connected to BLE")
        turtle.motors_on()
        draw_simple_cat(turtle)
        turtle.motors_off()
        logging.info("Drawing completed")
    finally:
        turtle.disconnect()
        logging.info("Disconnected from BLE")

# Call this to use the screen turtle graphics class
def main_screen():
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

    turtle.speed(1)
    draw_simple_cat(turtle)
    logging.info("Drawing completed")
    turtle.goto(0,0)
    turtle.setheading(0)
    turtle.done()

#main_screen()
main_physical()