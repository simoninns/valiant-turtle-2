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

// Stepper drive microstep configuration pins
#define SM_M0_GPIO 12
#define SM_M1_GPIO 13
#define SM_M2_GPIO 14

// Enumerations
typedef struct velocity_sequence velocity_sequence_t; // Forward declaration from velocity.h

// ENUM indication which stepper is required
typedef enum {
    STEPPER_LEFT = 0,
    STEPPER_RIGHT = 1,
    STEPPER_BOTH = 2
} stepper_side_t;

// ENUM for stepper direction
typedef enum {
    STEPPER_FORWARDS,
    STEPPER_BACKWARDS
} stepper_direction_t;

// Typedef for stepper's velocity configuration
typedef struct stepper_velocity_config_t {
    stepper_direction_t direction;
    int32_t accSpsps;
    int32_t minimumSps;
    int32_t maximumSps;
    int32_t updatesPerSecond;
} stepper_velocity_config_t;

// Type definition for overall stepper configuration
typedef struct stepper_settings_t {
    stepper_direction_t direction;
    stepper_velocity_config_t velocity;
    velocity_sequence_t *velocity_sequence;
    int32_t sequence_position;
    bool isEnabled;
    bool isBusy;
    int32_t steps_remaining;
} stepper_settings_t;

void stepper_initialise(void);
void stepper_enable(bool isEnabled);
void stepper_set_direction(stepper_side_t side, stepper_direction_t direction);
void stepper_set_velocity(stepper_side_t side, int32_t accSpsps, int32_t minimumSps, int32_t maximumSps, int32_t updatesPerSecond);
void stepper_set_steps(stepper_side_t side, int32_t steps);
int32_t stepper_get_steps(stepper_side_t side);
void stepper_dryrun(stepper_side_t side);
void stepper_dryrun_free(stepper_side_t side);
void stepper_run(stepper_side_t side);
stepper_settings_t stepper_get_configuration(stepper_side_t side);
bool stepper_isBusy(stepper_side_t side);

void stepper_left_callback();
void stepper_right_callback();

void stepper_set_configuration(void);

#endif /* STEPPER_H_ */