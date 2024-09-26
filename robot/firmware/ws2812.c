/************************************************************************ 

    ws2812.c

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

#include <stdint.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pio.h"

#include "ws2812.h"
#include "ws2812.pio.h"
#include "debug.h"

// Globals
static PIO ws2812_pio;
static uint ws2812_sm;
static uint ws2812_offset;

// Initialise the step generation
void ws2812_initialise()
{
    // Initialise the pulse output GPIOs
    gpio_init(WS2812_DATAOUT_GPIO);

    // Start the PIO running
    ws2812_pio_start();
}

// Claim PIO, SM and then start the PIOs
// also enables the required interrupts for CPU interaction
void ws2812_pio_start()
{
    ws2812_pio = pio1;

    // Load PIO 1 and claim SM 0
    ws2812_offset = pio_add_program(ws2812_pio, &ws2812_program);
    ws2812_sm = (int8_t)pio_claim_unused_sm(ws2812_pio, false);

    ws2812_program_init(ws2812_pio, ws2812_sm, ws2812_offset, WS2812_DATAOUT_GPIO, 800000, IS_RGBW);
}

// Stop the PIO and free the PIO and SM
void ws2812_pio_stop()
{
    // Cleanup PIO
    pio_remove_program_and_unclaim_sm(&ws2812_program, ws2812_pio, ws2812_sm, ws2812_offset);
}

// Output a pixel of data in RGB format
void ws2812_put_pixel(uint8_t r, uint8_t g, uint8_t b)
{
    uint32_t pixel_grb = ((uint32_t) (r) << 8) | ((uint32_t) (g) << 16) | (uint32_t) (b);
    pio_sm_put_blocking(ws2812_pio, ws2812_sm, pixel_grb << 8u);
}