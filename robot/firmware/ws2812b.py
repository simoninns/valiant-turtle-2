#************************************************************************ 
#
#   ws2812b.py
#
#   Control WS2812B RGB LEDs using PIO
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
    def __init__(self, num_pixels, _pio, _state_machine, pin, fade_speed = 10):
        if _pio > 1 or _pio < 0:
            ValueError("Ws2812b::__init__ - PIO ID must be 0 or 1")
        if _state_machine > 3 or _state_machine < 0:
            ValueError("Ws2812b::__init__ - State-machine ID must be 0-3")

        log_info("Ws2812b::__init__ - Ws2812b initialising on PIO", _pio, "state-machine", _state_machine, "with", num_pixels, "pixels")
        if _pio == 1: _state_machine += 4 # PIO 0 is SM 0-3 and PIO 1 is SM 4-7
        log_info("Ws2812b::__init__ - Micropython state-machine ID is", _state_machine)

        self.pixels = array.array("I", [0 for _ in range(num_pixels)])
        self.sm = rp2.StateMachine(_state_machine, ws2812, freq=8000000, sideset_base=Pin(pin))
        self.sm.active(1)
        self.num_pixels = num_pixels

        # Set up pixel values
        self.current_red = []
        self.current_green = []
        self.current_blue = []
        self.target_red = []
        self.target_green = []
        self.target_blue = []
        self.fade_speed = []

        for idx in range(self.num_pixels):
            self.current_red.append(0)
            self.current_green.append(0)
            self.current_blue.append(0)
            self.target_red.append(0)
            self.target_green.append(0)
            self.target_blue.append(0)
            self.fade_speed.append(fade_speed)

    def set_pixel(self, pixel_num, red, green, blue):
        if pixel_num > self.num_pixels:
            ValueError("Ws2812b::set_pixel - Pixel number exceeds the number of available LEDs")
        self.target_red[pixel_num] = red
        self.target_green[pixel_num] = green
        self.target_blue[pixel_num] = blue

    def set_fade_speed(self, pixel_num, fade_speed):
        if pixel_num > self.num_pixels:
            ValueError("Ws2812b::set_pixel - Pixel number exceeds the number of available LEDs")
        self.fade_speed[pixel_num] = fade_speed

    # Process the LED fading
    async def process_pixels_task(self):
        while True:
            for idx in range(self.num_pixels):
                if (self.target_red[idx] > self.current_red[idx]): self.current_red[idx] += self.fade_speed[idx]
                elif (self.target_red[idx] < self.current_red[idx]): self.current_red[idx] -= self.fade_speed[idx]
                if (self.target_green[idx] > self.current_green[idx]): self.current_green[idx] += self.fade_speed[idx]
                elif (self.target_green[idx] < self.current_green[idx]): self.current_green[idx] -= self.fade_speed[idx]
                if (self.target_blue[idx] > self.current_blue[idx]): self.current_blue[idx] += self.fade_speed[idx]
                elif (self.target_blue[idx] < self.current_blue[idx]): self.current_blue[idx] -= self.fade_speed[idx]

                if (self.current_red[idx] < 0): self.current_red[idx] = 0
                if (self.current_red[idx] > 255): self.current_red[idx] = 255
                if (self.current_green[idx] < 0): self.current_green[idx] = 0
                if (self.current_green[idx] > 255): self.current_green[idx] = 255
                if (self.current_blue[idx] < 0): self.current_blue[idx] = 0
                if (self.current_blue[idx] > 255): self.current_blue[idx] = 255

            self.__update_pixels()
            await asyncio.sleep_ms(10)

    # Update the pixels using the PIO state-machine
    def __update_pixels(self):
        for idx in range(self.num_pixels):
            enc_value =  self.current_blue[idx] | self.current_red[idx] << 8 | self.current_green[idx] << 16
            self.sm.put(enc_value,8)