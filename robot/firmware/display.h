/************************************************************************ 

    display.h

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

#ifndef DISPLAY_H_
#define DISPLAY_H_

#include "button.h"

// Define the two display button GPIOs
#define BACK_BUTTON 12  // Button on GPIO 16
#define FORWARD_BUTTON 13  // Button on GPIO 17

// Enumerations
typedef enum {
    DISPLAY_START,
    DISPLAY_POWER,
	DISPLAY_BT,
    DISPLAY_FWINFO
} display_state_t;

// Prototypes
void displayInitialise(void);
bool displayTimerCallback(repeating_timer_t *rt);
void buttonChangedCallback(button_t *button_p);

// Display state machine
void displayProcess(void);
display_state_t displayState_Start(void);
display_state_t displayState_Power(void);
display_state_t displayState_Bt(void);
display_state_t displayState_FwInfo(void);

#endif /* DISPLAY_H_ */