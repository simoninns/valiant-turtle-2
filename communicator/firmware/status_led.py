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

from log import log_debug, log_info, log_warn
from machine import PWM

class Status_led:
    def __init__(self, led_pin, brightness = 0, fade_speed = 10):
        self.led_pin = led_pin
        self.led = PWM(self.led_pin)
        self.led.freq(5000)
        self.led.duty_u16(0)

        self.current_brightness = 0
        self.target_brightness = brightness
        self.fade_speed = fade_speed # 1-255
        log_debug("Status_led::__init__ - Initialised LED on pin", self.led_pin)

    # Set brightness from 0 to 255
    def set_brightness(self, brightness: int):
        if (brightness < 0): brightness = 0
        if (brightness > 255): brightness = 255
        self.target_brightness = brightness

    def set_fade_speed(self, fade_speed):
        if (fade_speed < 1): fade_speed = 1
        if (fade_speed > 255): fade_speed = 255
        self.fade_speed = fade_speed

    # This should be called by a timer to process the LED fading
    def led_process(self):
        if (self.target_brightness > self.current_brightness):
            self.current_brightness += self.fade_speed
        elif (self.target_brightness < self.current_brightness):
            self.current_brightness -= self.fade_speed

        if (self.current_brightness < 0): self.current_brightness = 0
        if (self.current_brightness > 255): self.current_brightness = 255

        invert = int((255 - self.current_brightness) * 257)
        self.led.duty_u16(invert)