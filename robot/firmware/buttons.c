/************************************************************************ 

    buttons.c

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

#include "buttons.h"

void buttonsInitialise(void)
{
    // Initialise the drive motor control GPIOs
    gpio_init(BUTTON0_GPIO);
    gpio_init(BUTTON1_GPIO);

    gpio_set_dir(BUTTON0_GPIO, GPIO_IN);
    gpio_set_dir(BUTTON1_GPIO, GPIO_IN);

    gpio_pull_up(BUTTON0_GPIO);
    gpio_pull_up(BUTTON1_GPIO);
}

bool buttonsGetState(uint16_t buttonId)
{
    bool buttonState;

    if (buttonId == 0) {
        if(gpio_get(BUTTON0_GPIO)) buttonState = false;
        else buttonState = true;
    }

    if (buttonId == 1) {
        if(gpio_get(BUTTON1_GPIO)) buttonState = false;
        else buttonState = true;
    }

    return buttonState;
}