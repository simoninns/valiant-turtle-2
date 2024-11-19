#************************************************************************ 
#
#   led_fx.py
#
#   WS2812B LED effects
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

import logging
import machine, neopixel

import asyncio

class Led_fx:
    def __init__(self, number_of_leds, data_gpio_pin):
        self.number_of_leds = number_of_leds

        # Initialise the neopixel driver
        self.neopixel = neopixel.NeoPixel(machine.Pin(data_gpio_pin), 5)

        # Set up pixel values
        self.current_red = []
        self.current_green = []
        self.current_blue = []
        self.target_red = []
        self.target_green = []
        self.target_blue = []
        self.fade_speed = []

        for idx in range(self.number_of_leds):
            self.current_red.append(0)
            self.current_green.append(0)
            self.current_blue.append(0)
            self.target_red.append(0)
            self.target_green.append(0)
            self.target_blue.append(0)
            self.fade_speed.append(5)

        self.neopixel.fill((0,0,0))
        self.neopixel.write()

    def set_led_colour(self, led_number, red, green, blue):
        if led_number > self.number_of_leds:
            ValueError("Led_fx::set_led_colour - Led number exceeds the number of available LEDs")
        self.target_red[led_number] = red
        self.target_green[led_number] = green
        self.target_blue[led_number] = blue

    def set_led_fade_speed(self, pixel_num, fade_speed):
        if pixel_num > self.number_of_leds:
            ValueError("Led_fx::set_led_fade_speed - Led number exceeds the number of available LEDs")
        self.fade_speed[pixel_num] = fade_speed

    # Process the LED effects
    async def process_leds_task(self):
        logging.debug("Led_fx::process_leds_task - Task started")
        while True:
            for idx in range(self.number_of_leds):
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

                #self.ws2812b.set_pixel(idx, self.current_red[idx], self.current_green[idx], self.current_blue[idx])
                self.neopixel[idx] = (self.current_red[idx], self.current_green[idx], self.current_blue[idx])

            # Perform the actual update
            self.neopixel.write()
            await asyncio.sleep_ms(10)

if __name__ == "__main__":
    from main import main
    main()