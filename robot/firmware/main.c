/************************************************************************ 

    main.c

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
#include "btstack.h"
#include "pico/cyw43_arch.h"
#include "pico/btstack_cyw43.h"

#include "leds.h"
#include "penservo.h"
#include "drivemotors.h"
#include "i2cbus.h"
#include "ina260.h"
#include "display.h"
#include "buttons.h"
#include "btcomms.h"
#include "debug.h"

int main()
{
    // Initialise the hardware
    stdio_init_all();
    if (cyw43_arch_init()) return -1;
    debugInitialise();
    i2cInitialise();
    ina260Initialise();
    ledInitialise();
    penServoInitialise();
    driveMotorsInitialise();
    displayInitialise();
    buttonsInitialise();
    btcommsInitialise();

    // Turn on the PICO W system LED
    ledSystem(true);

    while (true) {
        sleep_ms(100);
    }
}