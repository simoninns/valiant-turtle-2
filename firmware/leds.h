/************************************************************************ 

    leds.h

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

#ifndef LEDS_H_
#define LEDS_H_

// Hardware mapping
#define LED_R_GPIO 16
#define LED_G_GPIO 22
#define LED_B_GPIO 26

// Function prototypes
void ledInitialise(void);
void ledSystem(bool ledState);
void ledRedInitialise(void);
void ledGreenInitialise(void);
void ledBlueInitialise(void);
void ledRedSet(int16_t brightness);
void ledGreenSet(int16_t brightness);
void ledBlueSet(int16_t brightness);

#endif /* LEDS_H_ */