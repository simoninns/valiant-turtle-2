/************************************************************************ 

    penservo.c

    Valiant Turtle 2 - Raspberry Pi Pico W Firmware
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
#include "hardware/pwm.h"
#include "hardware/clocks.h"

#include "penservo.h"
#include "debug.h"

float clockDiv = 64;
float wrap = 39062;

void pen_servo_initialise() {
    gpio_set_function(PENSERVO_GPIO, GPIO_FUNC_PWM);
    uint slice_num = pwm_gpio_to_slice_num(PENSERVO_GPIO);
    pwm_config config = pwm_get_default_config();
    
    // Calculate required clock speed
    uint64_t clockspeed = clock_get_hz(5);
    clockDiv = 64;
    wrap = 39062;

    while (clockspeed/clockDiv/50 > 65535 && clockDiv < 256) clockDiv += 64; 
    wrap = clockspeed/clockDiv/50;

    pwm_config_set_clkdiv(&config, clockDiv);
    pwm_config_set_wrap(&config, wrap);

    pwm_init(slice_num, &config, true);

    // Set pen up
    pen_up();
}

void pen_down() {
    float ms = 1000;
    pwm_set_gpio_level(PENSERVO_GPIO, (ms/20000.f)*wrap);
    debug_printf("pen_down(): Pen down\r\n");
}

void pen_up() {
    float ms = 2000;
    pwm_set_gpio_level(PENSERVO_GPIO, (ms/20000.f)*wrap);
    debug_printf("pen_up(): Pen up\r\n");
}

void pen_off(void) {
    pwm_set_gpio_level(PENSERVO_GPIO, 0);
    debug_printf("pen_off: Pen servo off\r\n");
}