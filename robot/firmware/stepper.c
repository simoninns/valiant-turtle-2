/************************************************************************ 

    stepper.c

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
#include <stdlib.h>

#include "pico/stdlib.h"

#include "stepper.h"
#include "velocity.h"
#include "pulse_generator.h"
#include "debug.h"

// Globals
stepper_config_t stepper_config[2];

void stepper_initialise()
{
    // GPIO initialisation
    gpio_init(SM_ENABLE_GPIO);
    gpio_init(SM_LSTEP_GPIO);
    gpio_init(SM_RSTEP_GPIO);
    gpio_init(SM_LDIR_GPIO);
    gpio_init(SM_RDIR_GPIO);

    // GPIO directions
    gpio_set_dir(SM_ENABLE_GPIO, GPIO_OUT);
    gpio_set_dir(SM_LSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(SM_RSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(SM_LDIR_GPIO, GPIO_OUT);
    gpio_set_dir(SM_RDIR_GPIO, GPIO_OUT);

    // Disable steppers
    stepper_enable(false);

    // Set direction to forwards
    stepper_set_direction(STEPPER_BOTH, STEPPER_FORWARDS);

    // Set the initial velocity default
    stepper_set_velocity(STEPPER_BOTH, 2, 2, 800, 8);

    // Set the steppers as not busy
    stepper_config[STEPPER_LEFT].isBusy = false;
    stepper_config[STEPPER_RIGHT].isBusy = false;

    // Initialise the pulse generator (to generate the step pulses)
    pulse_generator_init();

    // Register the pulse generator callback functions
    pulse_generator_register_callback(0, &stepper_left_callback);
    pulse_generator_register_callback(1, &stepper_right_callback);
}

// Enable or disable the steppers (this turns on/off the torque holding)
// Note: There is only one enable signal for both steppers
void stepper_enable(bool isEnabled)
{
    stepper_config[STEPPER_LEFT].isEnabled = isEnabled;
    stepper_config[STEPPER_RIGHT].isEnabled = isEnabled;

    if (isEnabled) {
        gpio_put(SM_ENABLE_GPIO, 1);
        debug_printf("stepper_enable(): Steppers enabled\n");
    } else {
        gpio_put(SM_ENABLE_GPIO, 0);
        debug_printf("stepper_enable(): Steppers disabled\n");
    }
}

// Set the stepper direction
void stepper_set_direction(stepper_side_t side, stepper_direction_t direction)
{
    if (side == STEPPER_LEFT || side == STEPPER_BOTH) {
        if (!stepper_config[STEPPER_LEFT].isBusy) {
            stepper_config[STEPPER_LEFT].direction = direction;

            if (direction == STEPPER_FORWARDS) {
                gpio_put(SM_LDIR_GPIO, 1);
                debug_printf("stepper_set_direction(): Stepper left direction = forwards\n");
            } else {
                gpio_put(SM_LDIR_GPIO, 0);
                debug_printf("stepper_set_direction(): Stepper left direction = backwards\n");
            }
        } else {
            debug_printf("stepper_set_direction(): WARNING - Stepper left is busy... ignoring set\n");
        }
    }

    if (side == STEPPER_RIGHT || side == STEPPER_BOTH) {
        if (!stepper_config[STEPPER_RIGHT].isBusy) {
            stepper_config[STEPPER_RIGHT].direction = direction;

            if (direction == STEPPER_FORWARDS) {
                gpio_put(SM_RDIR_GPIO, 0);
                debug_printf("stepper_set_direction(): Stepper right direction = forwards\n");
            } else {
                gpio_put(SM_RDIR_GPIO, 1);
                debug_printf("stepper_set_direction(): Stepper right direction = backwards\n");
            }
        } else {
            debug_printf("stepper_set_direction(): WARNING - Stepper right is busy... ignoring set\n");
        }
    }
}

// Set the velocity parameters
void stepper_set_velocity(stepper_side_t side, int32_t accSpsps, int32_t minimumSps,
    int32_t maximumSps, int32_t updatesPerSecond)
{
    if (side == STEPPER_LEFT || side == STEPPER_BOTH) {
        if (!stepper_config[STEPPER_LEFT].isBusy) {
            stepper_config[STEPPER_LEFT].velocity.accSpsps = accSpsps;
            stepper_config[STEPPER_LEFT].velocity.minimumSps = minimumSps;
            stepper_config[STEPPER_LEFT].velocity.maximumSps = maximumSps;
            stepper_config[STEPPER_LEFT].velocity.updatesPerSecond = updatesPerSecond;
        } else {
            debug_printf("stepper_set_velocity(): WARNING - Stepper left is busy... ignoring set\n");
        }
    }

    if (side == STEPPER_RIGHT || side == STEPPER_BOTH) {
        if (!stepper_config[STEPPER_RIGHT].isBusy) {
            stepper_config[STEPPER_RIGHT].velocity.accSpsps = accSpsps;
            stepper_config[STEPPER_RIGHT].velocity.minimumSps = minimumSps;
            stepper_config[STEPPER_RIGHT].velocity.maximumSps = maximumSps;
            stepper_config[STEPPER_RIGHT].velocity.updatesPerSecond = updatesPerSecond;
        } else {
            debug_printf("stepper_set_velocity(): WARNING - Stepper right is busy... ignoring set\n");
        }
    }
}

// Set the required number of steps
void stepper_set_steps(stepper_side_t side, int32_t steps)
{
    if (side == STEPPER_LEFT || side == STEPPER_BOTH) {
        stepper_config[STEPPER_LEFT].steps_remaining = steps;
    }

    if (side == STEPPER_RIGHT || side == STEPPER_BOTH) {
        stepper_config[STEPPER_RIGHT].steps_remaining = steps;
    }
}

// Get the required number of steps
int32_t stepper_get_steps(stepper_side_t side)
{
    int32_t steps = 0;

    if (side == STEPPER_LEFT || side == STEPPER_BOTH) {
        steps = stepper_config[STEPPER_LEFT].steps_remaining;
    }

    if (side == STEPPER_RIGHT || side == STEPPER_BOTH) {
        steps = stepper_config[STEPPER_RIGHT].steps_remaining;
    }

    return steps;
}

// Dry-run the stepper(s) - This just calculates the velocity, but 
// doesn't actually move the steppers
void stepper_dryrun(stepper_side_t side)
{
    // Calculate the required velocity sequence(s)
    if (side == STEPPER_LEFT || side == STEPPER_BOTH) {
        velocity_calculator_init(&stepper_config[STEPPER_LEFT].velocity_sequence);
        velocity_calculator(stepper_config[STEPPER_LEFT].velocity_sequence,
            stepper_config[STEPPER_LEFT].steps_remaining,
            stepper_config[STEPPER_LEFT].velocity.accSpsps,
            stepper_config[STEPPER_LEFT].velocity.minimumSps,
            stepper_config[STEPPER_LEFT].velocity.maximumSps,
            stepper_config[STEPPER_LEFT].velocity.updatesPerSecond);

        stepper_config[STEPPER_LEFT].sequence_position = 0;
    }

    if (side == STEPPER_RIGHT || side == STEPPER_BOTH) {
        velocity_calculator_init(&stepper_config[STEPPER_RIGHT].velocity_sequence);
        velocity_calculator(stepper_config[STEPPER_RIGHT].velocity_sequence,
            stepper_config[STEPPER_RIGHT].steps_remaining,
            stepper_config[STEPPER_RIGHT].velocity.accSpsps,
            stepper_config[STEPPER_RIGHT].velocity.minimumSps,
            stepper_config[STEPPER_RIGHT].velocity.maximumSps,
            stepper_config[STEPPER_RIGHT].velocity.updatesPerSecond);

        stepper_config[STEPPER_RIGHT].sequence_position = 0;
    }
}

// Needs to be called after using dryrun in order to free the allocated sequence
void stepper_dryrun_free(stepper_side_t side)
{
    if (side == STEPPER_LEFT || side == STEPPER_BOTH) {
        velocity_calculator_free(stepper_config[STEPPER_LEFT].velocity_sequence);
    }

    if (side == STEPPER_RIGHT || side == STEPPER_BOTH) {
        velocity_calculator_free(stepper_config[STEPPER_RIGHT].velocity_sequence);
    }
}

// Run the stepper(s)
void stepper_run(stepper_side_t side)
{
    // Calculate the required velocity sequence(s)
    if (side == STEPPER_LEFT || side == STEPPER_BOTH) {
        velocity_calculator_init(&stepper_config[STEPPER_LEFT].velocity_sequence);
        velocity_calculator(stepper_config[STEPPER_LEFT].velocity_sequence,
            stepper_config[STEPPER_LEFT].steps_remaining,
            stepper_config[STEPPER_LEFT].velocity.accSpsps,
            stepper_config[STEPPER_LEFT].velocity.minimumSps,
            stepper_config[STEPPER_LEFT].velocity.maximumSps,
            stepper_config[STEPPER_LEFT].velocity.updatesPerSecond);

        stepper_config[STEPPER_LEFT].sequence_position = 0;
    }

    if (side == STEPPER_RIGHT || side == STEPPER_BOTH) {
        velocity_calculator_init(&stepper_config[STEPPER_RIGHT].velocity_sequence);
        velocity_calculator(stepper_config[STEPPER_RIGHT].velocity_sequence,
            stepper_config[STEPPER_RIGHT].steps_remaining,
            stepper_config[STEPPER_RIGHT].velocity.accSpsps,
            stepper_config[STEPPER_RIGHT].velocity.minimumSps,
            stepper_config[STEPPER_RIGHT].velocity.maximumSps,
            stepper_config[STEPPER_RIGHT].velocity.updatesPerSecond);

        stepper_config[STEPPER_RIGHT].sequence_position = 0;
    }

    // Start the velocity sequence(s)
    if (side == STEPPER_LEFT || side == STEPPER_BOTH) {
        int32_t pio_delay = pulse_generator_pps_to_pio_delay(velocity_get_sps(stepper_config[STEPPER_LEFT].velocity_sequence,
            stepper_config[STEPPER_LEFT].sequence_position));
        int32_t pulse = velocity_get_steps(stepper_config[STEPPER_LEFT].velocity_sequence,
            stepper_config[STEPPER_LEFT].sequence_position);

        stepper_config[STEPPER_LEFT].sequence_position++;
        stepper_config[STEPPER_LEFT].isBusy = true;
        pulse_generator_set(0, pio_delay, pulse);
    }

    if (side == STEPPER_RIGHT || side == STEPPER_BOTH) {
        int32_t pio_delay = pulse_generator_pps_to_pio_delay(velocity_get_sps(stepper_config[STEPPER_RIGHT].velocity_sequence,
            stepper_config[STEPPER_RIGHT].sequence_position));
        int32_t pulse = velocity_get_steps(stepper_config[STEPPER_RIGHT].velocity_sequence,
            stepper_config[STEPPER_RIGHT].sequence_position);

        stepper_config[STEPPER_RIGHT].sequence_position++;
        stepper_config[STEPPER_RIGHT].isBusy = true;
        pulse_generator_set(1, pio_delay, pulse);
    }
}

// Return the current configuration for a stepper
stepper_config_t stepper_get_configuration(stepper_side_t side)
{
    if (side == STEPPER_BOTH) {
        debug_printf("stepper_get_configuration(): WARNING - Called with STEPPER_BOTH! Returning STEPPER_RIGHT\n");
    }

    if (side == STEPPER_LEFT) return stepper_config[STEPPER_LEFT];
    return stepper_config[STEPPER_RIGHT];
}

// Returns true if the stepper is busy 
bool stepper_isBusy(stepper_side_t side)
{
    if (side == STEPPER_LEFT) return stepper_get_configuration(STEPPER_LEFT).isBusy;
    if (side == STEPPER_RIGHT) return stepper_get_configuration(STEPPER_RIGHT).isBusy;

    if (side == STEPPER_BOTH) {
        if (stepper_get_configuration(STEPPER_LEFT).isBusy || stepper_get_configuration(STEPPER_RIGHT).isBusy) return true;
    }

    return false;
}


// Pulse generator SM0 callback (left stepper)
void stepper_left_callback()
{
    // Update the remaining steps
    stepper_config[STEPPER_LEFT].steps_remaining -= velocity_get_steps(stepper_config[STEPPER_LEFT].velocity_sequence,
        stepper_config[STEPPER_LEFT].sequence_position - 1);

    // Check if we have completed the sequence
    if (stepper_config[STEPPER_LEFT].sequence_position == velocity_get_size(stepper_config[STEPPER_LEFT].velocity_sequence)) {
        // Complete
        stepper_config[STEPPER_LEFT].isBusy = false;
        velocity_calculator_free(stepper_config[STEPPER_LEFT].velocity_sequence);
        return;
    }

    // Not complete - load the next velocity in the sequence
    int32_t pio_delay = pulse_generator_pps_to_pio_delay(velocity_get_sps(stepper_config[STEPPER_LEFT].velocity_sequence,
        stepper_config[STEPPER_LEFT].sequence_position));
    int32_t pulse = velocity_get_steps(stepper_config[STEPPER_LEFT].velocity_sequence,
        stepper_config[STEPPER_LEFT].sequence_position);

    stepper_config[STEPPER_LEFT].sequence_position++;
    pulse_generator_set(0, pio_delay, pulse);
}

// Pulse generator SM1 callback (right stepper)
void stepper_right_callback()
{
    // Update the remaining steps
    stepper_config[STEPPER_RIGHT].steps_remaining -= velocity_get_steps(stepper_config[STEPPER_RIGHT].velocity_sequence,
        stepper_config[STEPPER_RIGHT].sequence_position - 1);

    // Check if we have completed the sequence
    if (stepper_config[STEPPER_RIGHT].sequence_position == velocity_get_size(stepper_config[STEPPER_RIGHT].velocity_sequence)) {
        // Complete
        stepper_config[STEPPER_RIGHT].isBusy = false;
        velocity_calculator_free(stepper_config[STEPPER_RIGHT].velocity_sequence);
        return;
    }

    // Not complete - load the next velocity in the sequence
    int32_t pio_delay = pulse_generator_pps_to_pio_delay(velocity_get_sps(stepper_config[STEPPER_RIGHT].velocity_sequence,
        stepper_config[STEPPER_RIGHT].sequence_position));
    int32_t pulse = velocity_get_steps(stepper_config[STEPPER_RIGHT].velocity_sequence,
        stepper_config[STEPPER_RIGHT].sequence_position);

    stepper_config[STEPPER_RIGHT].sequence_position++;
    pulse_generator_set(1, pio_delay, pulse);
}