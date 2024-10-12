/************************************************************************ 

    leds.c

    Valiant Turtle 2 Communicator - Raspberry Pi Pico W Firmware
    Copyright (C) 2024 Simon Inns

    This file is part of Valiant Turtle 2

    This is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Email: simon.inns@gmail.com

************************************************************************/

#include <stdio.h>
#include <pico/stdlib.h>

#include "leds.h"

void leds_initialise(void)
{
    gpio_init(LED0_GPIO);
    gpio_init(LED1_GPIO);
    gpio_set_dir(LED0_GPIO, GPIO_OUT);
    gpio_set_dir(LED1_GPIO, GPIO_OUT);

    leds_state(0, false);
    leds_state(1, false);
}

void leds_state(int32_t led_number, bool state)
{
    // LED output is inverted
    if (state) state = false; else state = true;

    // Control the LEDs
    if (led_number == 0) gpio_put(LED0_GPIO, state);
    if (led_number == 1) gpio_put(LED1_GPIO, state);
}