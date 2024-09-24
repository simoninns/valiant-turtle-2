/************************************************************************ 

    pulse_generator.h

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

#ifndef PULSE_GENERATOR_H_
#define PULSE_GENERATOR_H_

// Define 2 step output GPIOs - These must be consecutive GPIOs
// due to PIO restrictions
#define PG_GPIO0 2
#define PG_GPIO1 3

// Type for callback function
typedef void (*callback_t) (void);

// Prototypes
void pulse_generator_init(void);
void pulse_generator_pio_start(void);
void pulse_generator_pio_stop(void);
void pulse_generator_set(int32_t sm, int32_t pio_delay, int32_t pulses);
uint32_t pulse_generator_pps_to_pio_delay(uint32_t pps);
void pulse_generator_register_callback(uint8_t sm, callback_t _registered_callback);
static void pulse_generator_interrupt_handler(void);

#endif /* PULSE_GENERATOR_H_ */