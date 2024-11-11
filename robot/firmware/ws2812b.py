#************************************************************************ 
#
#   ws2812b.py
#
#   Low-level WS2812B LED control using PIO
#   Valiant Turtle 2 - Robot firmware
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

from log import log_debug, log_info, log_warn
import array, time
from machine import Pin
import rp2
import asyncio

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)

def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

class Ws2812b:
    def __init__(self, num_leds, _pio, _state_machine, pin):
        if _pio > 1 or _pio < 0:
            ValueError("Ws2812b::__init__ - PIO ID must be 0 or 1")
        if _state_machine > 3 or _state_machine < 0:
            ValueError("Ws2812b::__init__ - State-machine ID must be 0-3")

        log_info("Ws2812b::__init__ - Ws2812b initialising on PIO", _pio, "state-machine", _state_machine, "with", num_leds, "pixels")
        if _pio == 1: _state_machine += 4 # PIO 0 is SM 0-3 and PIO 1 is SM 4-7
        log_info("Ws2812b::__init__ - Micropython state-machine ID is", _state_machine)

        self.num_leds = num_leds
        self.leds = array.array("I", [0 for _ in range(self.num_leds)])
        self.sm = rp2.StateMachine(_state_machine, ws2812, freq=8000000, sideset_base=Pin(pin))
        self.sm.active(1)

        # Set up pixel values
        self.red = []
        self.green = []
        self.blue = []

        for idx in range(self.num_leds):
            self.red.append(0)
            self.green.append(0)
            self.blue.append(0)

        # Set all LEDs to a known state
        self.update_pixels()

    def set_pixel(self, pixel_num, red, green, blue):
        if pixel_num > self.num_leds:
            ValueError("Ws2812b::set_pixel - Pixel number exceeds the number of available LEDs")
        self.red[pixel_num] = red
        self.green[pixel_num] = green
        self.blue[pixel_num] = blue

    # Update the pixels using the PIO state-machine
    def update_pixels(self):
        for idx in range(self.num_leds):
            enc_value =  self.blue[idx] | self.red[idx] << 8 | self.green[idx] << 16
            self.sm.put(enc_value,8)