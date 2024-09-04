/************************************************************************ 

    stepper.h

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

#ifndef STEPPER_H_
#define STEPPER_H_

// Hardware mapping
// Drive motors enable - GPIO 06 (pin 9)
#define SM_ENABLE_GPIO 6

// Drive motors left step - GPIO 02 (pin 4)
// Drive motors right step - GPIO 03 (pin 5)
// These must be consecutive GPIOs due to PIO restrictions
#define SM_LSTEP_GPIO 2
#define SM_RSTEP_GPIO 3

// Drive motors left direction - GPIO 04 (pin 6)
// Drive motors right direction - GPIO 05 (pin 7)
#define SM_LDIR_GPIO 4
#define SM_RDIR_GPIO 5

// Drive motor microstep control
#define SM_LM0_GPIO 21
#define SM_LM1_GPIO 20
#define SM_RM0_GPIO 19
#define SM_RM1_GPIO 18

typedef enum {
    SM_FORWARDS,
    SM_BACKWARDS,
    SM_LEFT,
    SM_RIGHT
} sm_direction_t;

typedef enum {
    SM_MODE_200,  //  200 steps/revolution (70% torque)
    SM_MODE_400,  //  400 steps/revolution (38% torque)
    SM_MODE_800,  //  800 steps/revolution (19% torque)
    SM_MODE_1600  // 1600 steps/revolution (10% torque)
} sm_microstep_mode_t;

typedef struct sequence_array sequence_array_t; // Forward declaration

void stepper_init(void);
void stepper_set_direction(sm_direction_t direction);
void stepper_enable(bool state);
void stepper_set_microstep_mode(sm_microstep_mode_t microstep_mode);
bool stepper_is_busy(void);

void stepper_pio_start(void);
void stepper_pio_stop(void);
bool stepper_set(sequence_array_t* container);
int32_t stepper_sps_to_delay(int32_t sps);
static void pio_irq_func(void);

#endif /* STEPPER_H_ */