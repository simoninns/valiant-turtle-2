/************************************************************************ 

    leds.c

    Valiant Turtle 2 - Raspberry Pi Pico W Firmware
    Copyright (C) 2023 Simon Inns

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
#include "pico/cyw43_arch.h"

#include "leds.h"

// Initialise all LED GPIO functions
void ledInitialise(void)
{
    // Nothing to do here
}

// Control the LEDs
void ledControl(led_id_t id, bool ledState)
{
    switch(id) {
        // Note: On the Pico W the system LED is connected to the the CYW43
        case LED_SYSTEM:
            if (ledState) cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
            else cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
            break;
        // case LED_STATUS:
        //     if (ledState) gpio_put(LED_SYSTEM_PIN, 1);
        //     else gpio_put(LED_SYSTEM_PIN, 0);
        //     break;
    }
}
