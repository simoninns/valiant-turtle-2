#************************************************************************ 
#
#   cat.py
#
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

import asyncio
import math
from ble_central import BleCentral
from commands_tx import CommandsTx

async def draw_approximated_circle(commands_tx: CommandsTx, cx, cy, radius, segments=36):
    """Draw a circle approximation using straight lines.
    The circle is centered at (cx, cy), and the radius is correctly handled.
    """
    angle = 360 / segments
    await commands_tx.pen(True)
    await commands_tx.position(cx, cy - radius)  # Move to the bottom point of the circle
    await commands_tx.heading(90)
    await commands_tx.pen(False)
    for _ in range(segments):
        await commands_tx.forward(2 * math.pi * radius / segments)
        await commands_tx.left(angle)

async def draw_cat(ble_central: BleCentral, commands_tx: CommandsTx):
    # Wait for connection
    while not ble_central.is_connected:
        await asyncio.sleep(1)

    # Motors on
    await commands_tx.motors(True)

    # Reset the origin
    await commands_tx.reset_origin()

    # Right ear
    print("Drawing the right ear")
    await commands_tx.pen(True)
    await commands_tx.position(40, 100+40)  # Base of the ear
    await commands_tx.pen(False)
    await commands_tx.position(45, 50+40-15)  # Tip of the ear
    await commands_tx.position(10, 50+40+10)  # Other side of the base
    await commands_tx.position(40, 100+40)  # Back to the base

    # Left ear
    print("Drawing the left ear")
    await commands_tx.pen(True)
    await commands_tx.position(-40, 100+40)  # Base of the ear
    await commands_tx.pen(False)
    await commands_tx.position(-50, 50+40-15)  # Tip of the ear
    await commands_tx.position(-10, 50+40+10)  # Other side of the base
    await commands_tx.position(-40, 100+40)  # Back to the base

    # Nose (triangle)
    print("Drawing the nose")
    await commands_tx.pen(True)
    await commands_tx.position(-5, 50)
    await commands_tx.pen(False)
    await commands_tx.position(5, 50)
    await commands_tx.position(0, 40)
    await commands_tx.position(-5, 50)

    # Whiskers - left
    print("Drawing the left whiskers")
    await commands_tx.pen(True)
    await commands_tx.position(-5, 40)
    await commands_tx.pen(False)
    await commands_tx.position(-40, 30)
    await commands_tx.pen(True)
    await commands_tx.position(-5, 40)
    await commands_tx.pen(False)
    await commands_tx.position(-40, 40)
    await commands_tx.pen(True)
    await commands_tx.position(-5, 40)
    await commands_tx.pen(False)
    await commands_tx.position(-40, 50)

    # Whiskers - right
    print("Drawing the right whiskers")
    await commands_tx.pen(True)
    await commands_tx.position(5, 40)
    await commands_tx.pen(False)
    await commands_tx.position(40, 30)
    await commands_tx.pen(True)
    await commands_tx.position(5, 40)
    await commands_tx.pen(False)
    await commands_tx.position(40, 40)
    await commands_tx.pen(True)
    await commands_tx.position(5, 40)
    await commands_tx.pen(False)
    await commands_tx.position(40, 50)

    # Tail
    print("Drawing the tail")
    await commands_tx.pen(True)
    await commands_tx.position(60, -120)
    await commands_tx.pen(False)
    await commands_tx.position(100, -100)
    await commands_tx.position(80, -90)

    # Head (approximated circle)    
    print("Drawing the head")
    await draw_approximated_circle(commands_tx, -6, 50, 50, segments=16)

    # Body (approximated circle)
    print("Drawing the body")
    await draw_approximated_circle(commands_tx, 0, -60, 70, segments=16)

    # # Left eye (approximated small circle)
    # print("Drawing the left eye")
    # await draw_approximated_circle(commands_tx, -20, 70, 10, segments=8)

    # # Right eye (approximated small circle)
    # print("Drawing the right eye")
    # await draw_approximated_circle(commands_tx, 20, 70, 10, segments=8)

    # Finish up
    print("Finishing up")
    await commands_tx.pen(True)
    await commands_tx.motors(False)
    print("Drawing complete")

    while True:
        await asyncio.sleep(1)