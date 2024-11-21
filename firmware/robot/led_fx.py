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

class LedFx:
    """
    A class to control and manage LED effects using a NeoPixel strip.
    Attributes:
    -----------
    number_of_leds : int
        The number of LEDs in the NeoPixel strip.
    neopixel : neopixel.NeoPixel
        The NeoPixel driver instance.
    current_red : list
        The current red color values for each LED.
    current_green : list
        The current green color values for each LED.
    current_blue : list
        The current blue color values for each LED.
    target_red : list
        The target red color values for each LED.
    target_green : list
        The target green color values for each LED.
    target_blue : list
        The target blue color values for each LED.
    fade_speed : list
        The fade speed for each LED.
    Methods:
    --------
    __init__(number_of_leds, data_gpio_pin):
        Initializes the LED effects controller with the specified number of LEDs and GPIO pin.
    set_led_colour(led_number, red, green, blue):
        Sets the target color for a specific LED.
    set_led_fade_speed(pixel_num, fade_speed):
        Sets the fade speed for a specific LED.
    process_leds_task():
        Asynchronous task to process and update the LED colors based on the target values and fade speeds.
    """

    def __init__(self, number_of_leds, data_gpio_pin):
        """
        Initialize the LED effects controller.
        Args:
            number_of_leds (int): The number of LEDs in the strip.
            data_gpio_pin (int): The GPIO pin connected to the data line of the LED strip.
        Attributes:
            number_of_leds (int): The number of LEDs in the strip.
            neopixel (neopixel.NeoPixel): The NeoPixel driver instance.
            current_red (list): The current red color values for each LED.
            current_green (list): The current green color values for each LED.
            current_blue (list): The current blue color values for each LED.
            target_red (list): The target red color values for each LED.
            target_green (list): The target green color values for each LED.
            target_blue (list): The target blue color values for each LED.
            fade_speed (list): The fade speed for each LED.
        """

        self.number_of_leds = number_of_leds

        # Initialise the neopixel driver
        self.neopixel = neopixel.NeoPixel(machine.Pin(data_gpio_pin), self.number_of_leds)

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
        """
        Sets the color of a specific LED by its number.
        Args:
            led_number (int): The index of the LED to set the color for.
            red (int): The intensity of the red color component (0-255).
            green (int): The intensity of the green color component (0-255).
            blue (int): The intensity of the blue color component (0-255).
        Raises:
            ValueError: If the led_number exceeds the number of available LEDs.
        """

        if led_number < 0 or led_number >= self.number_of_leds:
            raise ValueError("LedFx::set_led_colour - Led number exceeds the number of available LEDs")
        self.target_red[led_number] = red
        self.target_green[led_number] = green
        self.target_blue[led_number] = blue

    def set_led_fade_speed(self, pixel_num, fade_speed):
        """
        Sets the fade speed for a specific LED.
        Parameters:
        pixel_num (int): The index of the LED to set the fade speed for.
        fade_speed (int): The speed at which the LED should fade.
        Raises:
        ValueError: If the pixel_num exceeds the number of available LEDs.
        """

        if pixel_num < 0 or pixel_num >= self.number_of_leds:
            raise ValueError("LedFx::set_led_fade_speed - Led number exceeds the number of available LEDs")
        self.fade_speed[pixel_num] = fade_speed

    # Process the LED effects
    async def process_leds_task(self):
        """
        Asynchronous task to process and update the LED colors.
        This task continuously adjusts the current color values of the LEDs towards their target values
        using a specified fade speed. It ensures that the color values remain within the valid range (0-255)
        and updates the LED strip accordingly.
        The task runs indefinitely, updating the LED colors and writing the changes to the LED strip
        at regular intervals.
        """

        logging.debug("LedFx::process_leds_task - Task started")
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

                self.neopixel[idx] = (self.current_red[idx], self.current_green[idx], self.current_blue[idx])

            # Perform the actual update
            self.neopixel.write()
            await asyncio.sleep_ms(10)

if __name__ == "__main__":
    from main import main
    main()