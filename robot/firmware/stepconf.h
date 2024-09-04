/************************************************************************ 

    stepconfig.h

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

#ifndef STEPCONF_H_
#define STEPCONF_H_

// Enumerations
typedef enum {
    STEPPER_FORWARDS,
    STEPPER_BACKWARDS,
    STEPPER_LEFT,
    STEPPER_RIGHT
} stepconf_direction_t;

typedef struct stepconf_t {
    stepconf_direction_t direction;
    int32_t accSpsps;
    int32_t minimumSps;
    int32_t maximumSps;
    int32_t updatesPerSecond;
} stepconf_t;

void stepconf_initialise(void);
void stepconf_set_enable(bool status);
void stepconf_set_direction(stepconf_direction_t direction);
void stepconf_set_parameters(int32_t accSpsps, int32_t minimumSps,
    int32_t maximumSps, int32_t updatesPerSecond);
stepconf_t stepconf_get_parameters(void);
void stepconf_dryrun(int32_t requiredSteps);
void stepconf_run(int32_t requiredSteps);

#endif /* STEPCONF_H_ */