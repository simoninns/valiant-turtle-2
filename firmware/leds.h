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
#define LED_USB_PIN 2
#define LED_MIDI_OUT_PIN 3
#define LED_MIDI_IN_PIN 4
#define LED_STATUS_PIN 5

// Enumerations
typedef enum {
    LED_SYSTEM,
	LED_USB,
	LED_MIDI_IN,
    LED_MIDI_OUT,
    LED_STATUS,
} led_id_t;

// Function prototypes
void ledInitialise(void);
void ledControl(led_id_t id, bool ledState);

#endif /* LEDS_H_ */