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

import logging
import argparse
from abstract_turtle import TurtleInterface
from floor_turtle import FloorTurtle
from screen_turtle import ScreenTurtle
from commands_tx import CommandsTx

def draw_simple_cat(t: TurtleInterface):
    # Connect
    t.connect()
    t.motors(True)
    
    # Draw the head (circle)
    t.penup()
    t.goto(0, 50)
    t.pendown()
    t.circle(50, 360)

    # Draw the left ear (triangle pointing upwards)
    t.penup()
    t.goto(-40, 150 + 30)
    t.pendown()
    t.goto(-50, 100 + 30)
    t.goto(-10, 100 + 30)
    t.goto(-40, 150 + 30)

    # Draw the right ear (triangle pointing upwards)
    t.penup()
    t.goto(40, 150 + 30)
    t.pendown()
    t.goto(50, 100 + 30)
    t.goto(10, 100 + 30)
    t.goto(40, 150 + 30)

    # Draw the eyes (small circles)
    t.penup()
    t.goto(-20, 100)
    t.pendown()
    t.circle(10, 360)
    t.penup()
    t.goto(20, 100)
    t.pendown()
    t.circle(10, 360)

    # Draw the nose (triangle)
    t.penup()
    t.goto(0, 90)
    t.pendown()
    t.goto(-10, 80)
    t.goto(10, 80)
    t.goto(0, 90)

    # Draw the mouth (lines)
    t.penup()
    t.goto(0, 80)
    t.setheading(315)
    t.pendown()
    t.forward(15)
    t.penup()
    t.goto(0, 80)
    t.setheading(225)
    t.pendown()
    t.forward(15)

    # Draw the whiskers (lines)
    for angle in [200, 180, 160]:
        t.penup()
        t.goto(-10, 85)
        t.setheading(angle)
        t.pendown()
        t.forward(60)

    for angle in [340, 0, 20]:
        t.penup()
        t.goto(10, 85)
        t.setheading(angle)
        t.pendown()
        t.forward(60)

    # Draw the body (ellipse-like shape)
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.setheading(270)
    for _ in range(2):
        t.circle(50, 90)
        t.circle(100, 90)

    # Draw the tail (curved line)
    t.penup()
    t.goto(50, -50)
    t.setheading(120)
    t.pendown()
    t.circle(40, 200)

    t.penup()

    # Clean up
    t.motors(False)
    t.disconnect()

def main():
     # Configure the logging module
    log_format = "[%(asctime)s %(filename)s::%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, filename="vt2_demo.log")

    # Set up argparse
    parser = argparse.ArgumentParser(description="Choose turtle mode: screen or floor.")
    parser.add_argument(
        "-m", "--mode",
        choices=["screen", "floor"],
        default="screen",
        help="Choose between 'screen' for the on-screen turtle or 'floor' for the physical robot. Default is 'screen'."
    )
    args = parser.parse_args()
    mode = args.mode

    if mode == "screen":
        turtle_object = ScreenTurtle()
    elif mode == "floor":
        commands_tx = CommandsTx()
        turtle_object = FloorTurtle(commands_tx)
    else:
        print("Unsupported mode. Please choose 'screen' or 'floor'.")
        return

    # Draw the cat
    draw_simple_cat(turtle_object)

    # If we are in screen mode, run the main loop to keep the window open
    if mode == "screen":
        turtle_object.screen.mainloop()

if __name__ == "__main__":
    main()