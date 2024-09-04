/************************************************************************ 

    stepconfig.c

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

#include <stdio.h>
#include "pico/stdlib.h"

#include "stepconf.h"
#include "stepper.h"
#include "acccalc.h"
#include "seqarray.h"

// Globals
sequence_array_t* sequence;
stepconf_t stepper;
bool steppers_enabled;

// Initialise the stepper configuration
void stepconf_initialise(void) {
    // Initialise the low-level stepper control
    stepper_init();

    // Disable the steppers
    stepconf_set_enable(false);

    // Default left stepper configuration
    stepconf_set_direction(STEPPER_FORWARDS);
    stepconf_set_parameters(2, 2, 800, 8); // Acceleration SPSPS, minimum SPS, maximumSPS, updates per second
}

// Enable or disable the steppers (this turns on/off the torque holding)
void stepconf_set_enable(bool status) {
    stepper_enable(status);
    steppers_enabled = status;
}

// Set the stepper direction
void stepconf_set_direction(stepconf_direction_t direction) {
    stepper.direction = direction;
}

// Set the acceleration/run/deceleration parameters
void stepconf_set_parameters(int32_t accSpsps, int32_t minimumSps,
    int32_t maximumSps, int32_t updatesPerSecond) {

    stepper.accSpsps = accSpsps;
    stepper.minimumSps = minimumSps;
    stepper.maximumSps = maximumSps;
    stepper.updatesPerSecond = updatesPerSecond;
}

// Return the current parameters for a stepper
stepconf_t stepconf_get_parameters(void) {
    return stepper;
}

// Dry run the steppers (outputs the acc/run/dec calculation to debug)
void stepconf_dryrun(int32_t requiredSteps) {
    // Calculate the sequence and then display it
    seqarray_init(&sequence);
    bool success = acccalc_calculate(sequence, requiredSteps, stepper.accSpsps,
        stepper.minimumSps, stepper.maximumSps, stepper.updatesPerSecond);
    seqarray_display(sequence);
    seqarray_free(sequence);
}

// Run the steppers
void stepconf_run(int32_t requiredSteps) {
    // Set direction
    if (stepper.direction == STEPPER_FORWARDS) stepper_set_direction(SM_FORWARDS);
    if (stepper.direction == STEPPER_BACKWARDS) stepper_set_direction(SM_BACKWARDS);
    if (stepper.direction == STEPPER_LEFT) stepper_set_direction(SM_LEFT);
    if (stepper.direction == STEPPER_RIGHT) stepper_set_direction(SM_RIGHT);

    // Calculate the sequence and then display it
    seqarray_free(sequence);
    seqarray_init(&sequence);
    bool success = acccalc_calculate(sequence, requiredSteps, stepper.accSpsps,
        stepper.minimumSps, stepper.maximumSps, stepper.updatesPerSecond);
    stepper_set(sequence);
}