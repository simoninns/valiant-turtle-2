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
sequence_array_t* sequence_left;
sequence_array_t* sequence_right;

stepconf_t left_stepper;
stepconf_t right_stepper;

bool steppers_enabled;

// Initialise the stepper configuration
void stepconf_initialise(void) {
    // Initialise the low-level stepper control
    stepper_init();

    // Disable the steppers
    stepconf_set_enable(false);

    // Default left stepper configuration
    stepconf_set_direction(STEPPER_LEFT, STEPPER_FORWARDS);
    stepconf_set_parameters(STEPPER_LEFT, 32, 16, 4000, 8);

    // Default right stepper configuration
    stepconf_set_direction(STEPPER_RIGHT, STEPPER_FORWARDS);
    stepconf_set_parameters(STEPPER_RIGHT, 32, 16, 4000, 8);
}

// Enable or disable the steppers (this turns on/off the torque holding)
void stepconf_set_enable(bool status) {
    stepper_enable(status);
    steppers_enabled = status;
}

// Set the stepper to spin forwards or backwards
void stepconf_set_direction(stepconf_side_t side, stepconf_direction_t direction) {
    if (side == STEPPER_LEFT) left_stepper.direction = direction;
    else right_stepper.direction = direction;
}

// Set the acceleration/run/deceleration parameters
void stepconf_set_parameters(stepconf_side_t side, int32_t accSpsps, int32_t minimumSps,
    int32_t maximumSps, int32_t updatesPerSecond) {
    if (side == STEPPER_LEFT) {
        left_stepper.accSpsps = accSpsps;
        left_stepper.minimumSps = minimumSps;
        left_stepper.maximumSps = maximumSps;
        left_stepper.updatesPerSecond = updatesPerSecond;
    } else {
        right_stepper.accSpsps = accSpsps;
        right_stepper.minimumSps = minimumSps;
        right_stepper.maximumSps = maximumSps;
        right_stepper.updatesPerSecond = updatesPerSecond;
    }
}

// Return the current parameters for a stepper
stepconf_t stepconf_get_parameters(stepconf_side_t side) {
    if (side == STEPPER_LEFT) return left_stepper;
    return right_stepper;
}

// Dry run one of the steppers (outputs the acc/run/dec calculation to debug)
void stepconf_dryrun(stepconf_side_t side, int32_t requiredSteps) {
    // Calculate the sequence and then display it
    if (side == STEPPER_LEFT) {
        seqarray_init(&sequence_left);
        bool success = acccalc_calculate(sequence_left, requiredSteps, left_stepper.accSpsps,
            left_stepper.minimumSps, left_stepper.maximumSps, left_stepper.updatesPerSecond);
        seqarray_display(sequence_left);
        seqarray_free(sequence_left);
    } else {
        seqarray_init(&sequence_right);
        bool success = acccalc_calculate(sequence_right, requiredSteps, right_stepper.accSpsps,
            right_stepper.minimumSps, right_stepper.maximumSps, right_stepper.updatesPerSecond);
        seqarray_display(sequence_right);
        seqarray_free(sequence_right);
    }
}

// Run one of the steppers
void stepconf_run(stepconf_side_t side, int32_t requiredSteps) {
    // Set direction
    if (side == STEPPER_LEFT) {
        if (left_stepper.direction == STEPPER_FORWARDS) stepper_set_direction(SM_LEFT, SM_FORWARDS);
        else stepper_set_direction(SM_LEFT, SM_BACKWARDS);
    } else {
        if (right_stepper.direction == STEPPER_FORWARDS) stepper_set_direction(SM_RIGHT, SM_FORWARDS);
        else stepper_set_direction(SM_RIGHT, SM_BACKWARDS);
    }

    // Calculate the sequence and then display it
    if (side == STEPPER_LEFT) {
        seqarray_free(sequence_left);
        seqarray_init(&sequence_left);
        bool success = acccalc_calculate(sequence_left, requiredSteps, left_stepper.accSpsps,
            left_stepper.minimumSps, left_stepper.maximumSps, left_stepper.updatesPerSecond);
        stepper_set(SM_LEFT, sequence_left);
    } else {
        seqarray_free(sequence_right);
        seqarray_init(&sequence_right);
        bool success = acccalc_calculate(sequence_right, requiredSteps, right_stepper.accSpsps,
            right_stepper.minimumSps, right_stepper.maximumSps, right_stepper.updatesPerSecond);
        stepper_set(SM_RIGHT, sequence_right);
    }
}