#************************************************************************ 
#
#   status_led.py
#
#   Valiant Turtle 2 - Communicator firmware
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

from machine import Pin

class Status_led:
    def __init__(self, led_pin):
        self.led = Pin(led_pin, Pin.OUT)
        self.led.value(1) # LEDs are inverted logic 1=OFF

    def set(self, state: bool):
        if state: self.led.value(0) # True = ON
        else: self.led.value(1) # False = OFF
