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
from commands_tx import CommandsTx
import sys
import time
import cmd

def draw_simple_cat(commands_tx: CommandsTx):
    commands_tx.motors(True)

    # Draw the head (circle)
    commands_tx.pen(True)
    commands_tx.position(0, 50)
    commands_tx.pen(False)
    commands_tx.circle(50, 360)

    # Draw the left ear (triangle pointing upwards)
    commands_tx.pen(True)
    commands_tx.position(-40, 150+30)
    commands_tx.pen(False)
    commands_tx.position(-50, 100+30)
    commands_tx.position(-10, 100+30)
    commands_tx.position(-40, 150+30)

    # Draw the right ear (triangle pointing upwards)
    commands_tx.pen(True)
    commands_tx.position(40, 150+30)
    commands_tx.pen(False)
    commands_tx.position(50, 100+30)
    commands_tx.position(10, 100+30)
    commands_tx.position(40, 150+30)

    # Draw the eyes (small circles)
    commands_tx.pen(True)
    commands_tx.position(-20, 100)
    commands_tx.pen(False)
    commands_tx.circle(10, 360)
    commands_tx.pen(True)
    commands_tx.position(20, 100)
    commands_tx.pen(False)
    commands_tx.circle(10, 360)

    # Draw the nose (triangle)
    commands_tx.pen(True)
    commands_tx.position(0, 90)
    commands_tx.pen(False)
    commands_tx.position(-10, 80)
    commands_tx.position(10, 80)
    commands_tx.position(0, 90)

    # Draw the mouth (lines)
    commands_tx.pen(True)
    commands_tx.position(0, 80)
    commands_tx.heading(315)
    commands_tx.pen(False)
    commands_tx.forward(15)
    commands_tx.pen(True)
    commands_tx.position(0, 80)
    commands_tx.heading(225)
    commands_tx.pen(False)
    commands_tx.forward(15)

    # Draw the whiskers (lines)
    # Left side
    for angle in [200, 180, 160]:
        commands_tx.pen(True)
        commands_tx.position(-10, 85)
        commands_tx.heading(angle)
        commands_tx.pen(False)
        commands_tx.forward(60)

    # Right side
    for angle in [340, 0, 20]:
        commands_tx.pen(True)
        commands_tx.position(10, 85)
        commands_tx.heading(angle)
        commands_tx.pen(False)
        commands_tx.forward(60)

    # Draw the body (ellipse-like shape)
    commands_tx.pen(True)
    commands_tx.position(0, 0)
    commands_tx.pen(False)
    commands_tx.heading(270)
    for _ in range(2):
        commands_tx.circle(50, 90)
        commands_tx.circle(100, 90)

    # Draw the tail (curved line)
    commands_tx.pen(True)
    commands_tx.position(50, -50)
    commands_tx.heading(120)
    commands_tx.pen(False)
    commands_tx.circle(40, 200)

    commands_tx.pen(True)
    commands_tx.motors(False)

def main():
    # Configure the logging module
    log_format = "[%(asctime)s %(filename)s::%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, filename="vt2_cmdtest.log")

    commands_tx = CommandsTx()

    # Wait for BLE connection
    commands_tx.connect()
    logging.info("Waiting for BLE connection...")
    while not commands_tx.connected:
        time.sleep(1)
    logging.info("Connected to BLE")

    draw_simple_cat(commands_tx)
    logging.info("Command tests completed. Exiting program.")
    commands_tx.disconnect()
    logging.info("Disconnected from BLE")

    sys.exit(0)

if __name__ == "__main__":
    main()