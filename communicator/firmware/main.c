/************************************************************************ 

    main.c

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
#include "pico/cyw43_arch.h"
#include "hardware/uart.h"

#include "uart.h"
#include "leds.h"
#include "btcomms.h"

int main() {
    // Initialise the hardware
    stdio_init_all();
    if (cyw43_arch_init()) return -1;

    // Initialise modules
    uart_initialise();
    leds_initialise();
    btcomms_initialise();

    // Show some intro text on debug to show we are alive
    printf_debug("Valiant Turtle 2 - Communicator\r\n");
    printf_debug("Debug Console\r\n");

    // Turn on the PICO W system LED
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    leds_state(0, true);
    leds_state(1, false);

    // Loop and process any non-interrupt driven activities
    while (true) {
        for (int i=0; i<50; i++) {
            //printf_debug("C %d Heartbeat\r\n", i);

            for (int a=0; a<5; a++) {
                leds_state(1, true);
                sleep_ms(750);
                leds_state(1, false);
                sleep_ms(250);
            }
        }
    }
}