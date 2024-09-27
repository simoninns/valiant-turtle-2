/************************************************************************ 

    ws2812.h

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

#ifndef WS2812_H_
#define WS2812_H_

// Define GPIO for WS2812 data out
#define WS2812_DATAOUT_GPIO 7

#define IS_RGBW false

// Prototypes
void ws2812_initialise(void);
void ws2812_pio_start(void);
void ws2812_pio_stop(void);

void ws2812_put_pixel(uint8_t r, uint8_t g, uint8_t b);

#endif /* WS2812_H_ */