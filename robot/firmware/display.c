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
#include "ina260.h"
#include "debug.h"

// Global
ssd1306_t disp;
bool displayTimerCallback(repeating_timer_t *rt);
repeating_timer_t timer;
int16_t startCounter;

// State Globals
display_state_t displayState;

void displayInitialise(void)
{
    // Initialise the display state machine
    displayState = DISPLAY_START;
    startCounter = 0;

    // Initialise the SSD1306 OLED library
    disp.external_vcc=false;
    ssd1306_init(&disp, 128, 64, 0x3C, i2c0);
    ssd1306_clear(&disp);

    // Set up the repeating display update timer
    int16_t hz = 2;

    if (!add_repeating_timer_us(1000000 / hz, displayTimerCallback, NULL, &timer)) {
        debugPrintf("Display: Failed to add display update timer!\r\n");
    }
}

bool displayTimerCallback(repeating_timer_t *rt)
{
    displayProcess();
    return true;
}

// Display state machine ------------------------------------------------------------

void displayProcess(void)
{
    switch(displayState) {
        case DISPLAY_START:
            displayState = displayState_Start();
            break;

        case DISPLAY_POWER:
            displayState = displayState_Power();
            break;

        case DISPLAY_BT:
            displayState = displayState_Bt();
            break;

        case DISPLAY_FWINFO:
            displayState = displayState_FwInfo();
            break; 
    }
}

// Start-up display information
display_state_t displayState_Start(void)
{
    // Update the display
    ssd1306_clear(&disp);
    ssd1306_draw_string(&disp, 15, 0, 1, "Valiant Turtle 2");
    ssd1306_draw_string(&disp, 25, 22, 2, "Turtle");
    ssd1306_draw_string(&disp, 25, 40, 2, "Power!");
    ssd1306_show(&disp);

    // Keep the start screen active for 5 timer callbacks
    startCounter++;
    if (startCounter == 5) return DISPLAY_POWER;

    return DISPLAY_START;
}

// Show power information
display_state_t displayState_Power(void)
{
    // Prepare the information
    float mAmps = ina260ReadCurrent();
    float mVolts = ina260ReadBusVoltage();
    float mWatts = ina260ReadPower();

    char mVoltsString[32];
    char mAmpsString[32];
    char mWattsString[32];
    sprintf(mAmpsString, "Current: %.2f mA\r\n", mAmps);
    sprintf(mVoltsString, "Voltage: %.2f mV\r\n", mVolts);
    sprintf(mWattsString, "  Power: %.2f mW\r\n", mWatts);

    // Update the display
    ssd1306_clear(&disp);
    ssd1306_draw_string(&disp, 0, 0, 2, "Power:");
    ssd1306_draw_string(&disp, 0, 24, 1, mAmpsString);
    ssd1306_draw_string(&disp, 0, 34, 1, mVoltsString);
    ssd1306_draw_string(&disp, 0, 44, 1, mWattsString);
    ssd1306_show(&disp);

    return DISPLAY_POWER;
}

// Show Bluetooth information
display_state_t displayState_Bt(void)
{
    // Update the display
    ssd1306_clear(&disp);
    ssd1306_draw_string(&disp, 0, 0, 2, "Bluetooth:");
    ssd1306_show(&disp);

    return DISPLAY_POWER;
}

// Show Software Information
display_state_t displayState_FwInfo(void)
{
    // Update the display
    ssd1306_clear(&disp);
    ssd1306_draw_string(&disp, 0, 0, 2, "Firmware:");
    ssd1306_show(&disp);

    return DISPLAY_POWER;
}