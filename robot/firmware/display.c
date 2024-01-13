/************************************************************************ 

    display.c

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

#include "display.h"
#include "ssd1306.h"

// Global
ssd1306_t disp;

void displayInitialise(void)
{
    // Initialise the SSD1306 OLED library
    disp.external_vcc=false;
    ssd1306_init(&disp, 128, 64, 0x3C, i2c0);
    ssd1306_clear(&disp);

    ssd1306_draw_string(&disp, 15, 0, 1, "Valiant Turtle 2");
    ssd1306_draw_string(&disp, 25, 22, 2, "Turtle");
    ssd1306_draw_string(&disp, 25, 40, 2, "Power!");
    ssd1306_show(&disp);
}

void displayPowerInformation(float mAmps, float mVolts, float mWatts)
{
    // Prepare the information
    char mVoltsString[32];
    char mAmpsString[32];
    char mWattsString[32];
    sprintf(mAmpsString, "Current: %.2f mA\r\n", mAmps);
    sprintf(mVoltsString, "Voltage: %.2f mV\r\n", mVolts);
    sprintf(mWattsString, "  Power: %.2f mW\r\n", mWatts);

    // Update the display
    ssd1306_clear(&disp);
    ssd1306_draw_string(&disp, 0, 0, 1, mAmpsString);
    ssd1306_draw_string(&disp, 0, 10, 1, mVoltsString);
    ssd1306_draw_string(&disp, 0, 20, 1, mWattsString);
    ssd1306_show(&disp);
}