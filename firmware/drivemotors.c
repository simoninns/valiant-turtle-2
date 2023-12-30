/************************************************************************ 

    drivemotors.c

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
#include <string.h>

#include "drivemotors.h"

void driveMotorsInitialise(void)
{
    // Initialise the drive motor control GPIOs
    gpio_init(DM_ENABLE_GPIO);
    gpio_init(DM_LSTEP_GPIO);
    gpio_init(DM_RSTEP_GPIO);
    gpio_init(DM_LDIR_GPIO);
    gpio_init(DM_RDIR_GPIO);

    // Set the drive motor control GPIO directions
    gpio_set_dir(DM_ENABLE_GPIO, GPIO_OUT);
    gpio_set_dir(DM_LSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(DM_RSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(DM_LDIR_GPIO, GPIO_OUT);
    gpio_set_dir(DM_RDIR_GPIO, GPIO_OUT);

    // Default values
    driveMotorsEnable(false);
    driveMotorLeftDir(false);
    driveMotorRightDir(false);
}

void driveMotorsEnable(bool state)
{
    if (state) gpio_put(DM_ENABLE_GPIO, 1);
    else gpio_put(DM_ENABLE_GPIO, 0);
}

void driveMotorLeftDir(bool state)
{
    if (state) gpio_put(DM_LDIR_GPIO, 1);
    else gpio_put(DM_LDIR_GPIO, 0);
}

void driveMotorRightDir(bool state)
{
    if (state) gpio_put(DM_RDIR_GPIO, 1);
    else gpio_put(DM_RDIR_GPIO, 0);
}

void driveMotorLeftStep(uint16_t steps)
{
    if (steps > 0) {
        printf("I00 - Left stepping %d\r\n", steps);
        for (uint16_t cnt = 0; cnt < steps; cnt++) {
            gpio_put(DM_LSTEP_GPIO, 1);
            sleep_ms(1.9);
            gpio_put(DM_LSTEP_GPIO, 0);
            sleep_ms(1.9);
        }
    }
}

void driveMotorRightStep(uint16_t steps)
{
    if (steps > 0) {
        printf("I00 - Right stepping %d\r\n", steps);
        for (uint16_t cnt = 0; cnt < steps; cnt++) {
            gpio_put(DM_RSTEP_GPIO, 1);
            sleep_us(2);
            gpio_put(DM_RSTEP_GPIO, 0);
            sleep_us(2);
        }
    }
}