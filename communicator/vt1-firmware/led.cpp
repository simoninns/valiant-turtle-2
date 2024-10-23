/************************************************************************ 

    led.cpp

    Valiant Turtle Communicator 2
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

#include <cstdio>
#include <iostream>
#include "pico/stdlib.h"

#include "led.h"

// Initialise the LED
Led::Led(uint8_t _led_gpio) {
    led_gpio = _led_gpio;
    gpio_init(led_gpio);
    gpio_set_dir(led_gpio, GPIO_OUT);
    set_state(false);
}

// Set the state of the LED (true = on, false = off)
void Led::set_state(bool _led_state) {
    led_state = _led_state;
    gpio_put(led_gpio, !led_state);
}