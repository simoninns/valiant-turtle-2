#************************************************************************ 
#
#   leds.py
#
#   LED effects
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

import logging
from machine import PWM, Pin, Timer

class Leds:
    def __init__(self, data_gpio_pins):
        self.period_ms = 25
        self.number_of_leds = len(data_gpio_pins)
        logging.debug("Leds::__init__ - Initialising with", self.number_of_leds, "leds")

        # Set up led values
        self.current_brightness = []
        self.target_brightness = []
        self.fade_speed = []
        self.led = []

        for gpio_pin in data_gpio_pins:
            self.current_brightness.append(0)
            self.target_brightness.append(0)
            self.fade_speed.append(20)

            self.led.append(PWM(gpio_pin))
            self.led[-1].freq(5000)
            self.led[-1].duty_u16(0)

        # Start the processing one-shot timer
        self.timer = Timer(period=self.period_ms, mode=Timer.ONE_SHOT, callback=self.__update_leds)

    def set_brightness(self, led_number, brightness):
        if led_number > self.number_of_leds:
            ValueError("Leds::set_led_brightness - Led number exceeds the number of available LEDs")
        self.target_brightness[led_number] = brightness

    def set_fade_speed(self, led_number, fade_speed):
        if led_number > self.number_of_leds:
            ValueError("Leds::set_led_fade_speed - Led number exceeds the number of available LEDs")
        self.fade_speed[led_number] = fade_speed

    # Update the LEDs
    def __update_leds(self, t):
        for led_number in range(self.number_of_leds):
            if (self.target_brightness[led_number] > self.current_brightness[led_number]): self.current_brightness[led_number] += self.fade_speed[led_number]
            elif (self.target_brightness[led_number] < self.current_brightness[led_number]): self.current_brightness[led_number] -= self.fade_speed[led_number]

            if (self.current_brightness[led_number] < 0): self.current_brightness[led_number] = 0
            if (self.current_brightness[led_number] > 255): self.current_brightness[led_number] = 255

            invert = int((255 - self.current_brightness[led_number]) * 257)
            self.led[led_number].duty_u16(invert)

        # Set the one-shot timer up again
        self.timer.init(period=self.period_ms, mode=Timer.ONE_SHOT, callback=self.__update_leds)