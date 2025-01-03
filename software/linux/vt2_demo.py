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
from cat import Cat
from logotype import Logotype
from calitest import Calitest1, Calitest2

def main():
     # Configure the logging module
    log_format = "[%(asctime)s %(filename)s::%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, filename="vt2_demo.log")

    # Set up argparse
    parser = argparse.ArgumentParser(description="Choose turtle mode and shape.")
    parser.add_argument(
        "-m", "--mode",
        choices=["screen", "floor"],
        default="screen",
        help="Choose between 'screen' for the on-screen turtle or 'floor' for the physical robot. Default is 'screen'."
    )
    parser.add_argument(
        "-d", "--drawing",
        choices=["cat", "logotype", "calitest1", "calitest2"],
        default="logotype",
        help="Choose the shape to draw: 'cat', 'calitest1', 'calitest2' or 'logotype'. Default is 'logotype'."
    )
    parser.add_argument(
        "-s", "--speed",
        type=int,
        choices=range(10),
        default=6,
        help="Choose the speed of the turtle (0-9). Default is 6."
    )
    args = parser.parse_args()
    mode = args.mode
    drawing = args.drawing
    speed = args.speed

    # Range check for speed
    if speed < 0 or speed > 9:
        print("Speed must be between 0 and 9.")
        return

    if mode == "screen":
        turtle_object = ScreenTurtle()
    elif mode == "floor":
        commands_tx = CommandsTx()
        turtle_object = FloorTurtle(commands_tx)
    else:
        print("Unsupported mode. Please choose 'screen' or 'floor'.")
        return

    if drawing == "cat":
        # Draw the cat
        cat = Cat(turtle_object, speed)
        cat.render()
    elif drawing == "logotype":
        # Draw the Valiant Turtle 2 logo
        logotype = Logotype(turtle_object, speed)
        logotype.render()
    elif drawing == "calitest1":
        # Draw the calitest
        calitest1 = Calitest1(turtle_object, speed)
        calitest1.render()
    elif drawing == "calitest2":
        # Draw the calitest
        calitest2 = Calitest2(turtle_object, speed)
        calitest2.render()
    else:
        print("Unsupported drawing. Please choose 'cat' or 'logotype'.")
        return

    # If we are in screen mode, run the main loop to keep the window open
    if mode == "screen":
        turtle_object.screen.mainloop()

if __name__ == "__main__":
    main()