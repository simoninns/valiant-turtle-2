/************************************************************************ 

    main.c

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
#include "pico/cyw43_arch.h"
#include "btstack.h"
#include "pico/btstack_cyw43.h"

#include "debug.h"
#include "cli.h"
#include "i2cbus.h"
#include "ina260.h"
#include "penservo.h"
#include "oleddisplay.h"
#include "stepconf.h"
#include "btcomms.h"

int main() {
    // Initialise the hardware
    stdio_init_all();
    if (cyw43_arch_init()) return -1;

    // Initialise modules
    debug_initialise();
    i2c_initialise();
    ina260_initialise();
    pen_servo_initialise();
    oled_initialise();
    stepconf_initialise();
    cli_initialise();
    btcomms_initialise();

    // Turn on the PICO W system LED
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);

    // Loop and process any non-interrupt driven activities
    while (true) {
        // Process the CLI
        cli_process();

        // Sleep a bit
        sleep_ms(10);
    }
}