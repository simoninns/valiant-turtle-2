/************************************************************************ 

    i2c.cpp

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
#include "hardware/i2c.h"

#include "i2c.h"

// Initialise the I2C interface
I2c::I2c(i2c_inst_t* _i2c_id, uint8_t _sda_gpio, uint8_t _sck_gpio)
    : i2c_id(_i2c_id), sda_gpio(_sda_gpio), sck_gpio(_sck_gpio) {

    // Initialise I2C interface
    i2c_init(i2c_id, 400000); // Standard mode 100 Kbps

    // Select i2c function for GPIOs
    gpio_set_function(sda_gpio, GPIO_FUNC_I2C);
    gpio_set_function(sck_gpio, GPIO_FUNC_I2C);

    // Turn on pull-ups
    gpio_pull_up(sda_gpio);
    gpio_pull_up(sck_gpio);
}