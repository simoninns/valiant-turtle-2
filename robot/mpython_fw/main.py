#************************************************************************ 
#
#   main.py
#
#   Valiant Turtle 2 - Raspberry Pi Pico W Firmware
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

from ws2812b import Ws2812b
from pen import Pen
from time import sleep

# Initialise the LEDs and show some colour
leds = Ws2812b(3, 0, 7, delay=0)

# Initialise the pen control
pen = Pen(16)

while True:
    leds.set_pixel(0, 255, 0, 0)
    leds.set_pixel(1, 0, 255, 0)
    leds.set_pixel(2, 0, 0, 255)
    leds.show()
    pen.off()
    sleep(1.0)

    leds.set_pixel(0, 0, 255, 0)
    leds.set_pixel(1, 0, 0, 255)
    leds.set_pixel(2, 255, 0, 0)
    leds.show()
    pen.up()
    sleep(1.0)

    leds.set_pixel(0, 0, 0, 255)
    leds.set_pixel(1, 255, 0, 0)
    leds.set_pixel(2, 0, 255, 0)
    leds.show()
    pen.down()
    sleep(1.0)
