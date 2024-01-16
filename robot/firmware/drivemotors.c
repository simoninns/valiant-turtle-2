/************************************************************************ 

    drivemotors.c

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

#include <stdio.h>
#include <pico/stdlib.h>
#include <string.h>

#include "drivemotors.h"
#include "debug.h"

// Globals
int16_t leftSteps;
int16_t rightSteps;
bool leftState;
bool rightState;
bool motorTimerCallback(repeating_timer_t *rt);
repeating_timer_t motorTimer;

void driveMotorsInitialise(void)
{
    // Initialise the drive motor control GPIOs
    gpio_init(DM_ENABLE_GPIO);
    gpio_init(DM_LSTEP_GPIO);
    gpio_init(DM_RSTEP_GPIO);
    gpio_init(DM_LDIR_GPIO);
    gpio_init(DM_RDIR_GPIO);

    // Set the drive motor control GPIO directions
    gpio_set_dir(DM_ENABLE_GPIO, GPIO_OUT);
    gpio_set_dir(DM_LSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(DM_RSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(DM_LDIR_GPIO, GPIO_OUT);
    gpio_set_dir(DM_RDIR_GPIO, GPIO_OUT);

    // Default values
    driveMotorsEnable(false);
    driveMotorSetDir(MOTOR_LEFT, MOTOR_FORWARDS);
    driveMotorSetDir(MOTOR_RIGHT, MOTOR_FORWARDS);

    // Set remaining steps to zero
    leftSteps = 0;
    rightSteps = 0;
    
    // Set the initial step states to off
    leftState = false;
    rightState = false;

    // Set up the repeating display update timer
    // Maximum DRV8825 frequency is 1.9us, so we need to callback every
    // 850us with a pulse at 50% duty
    if (!add_repeating_timer_us(-1900/2, motorTimerCallback, NULL, &motorTimer)) {
        debugPrintf("Drive motors: Failed to add motor update timer!\r\n");
    }
}

// Callback function for the motor pulse timer
bool motorTimerCallback(repeating_timer_t *rt)
{
    // Step the left motor
    if (leftSteps > 0) {
        if (!leftState) {
            gpio_put(DM_LSTEP_GPIO, 1);
            leftState = true;
        } else {
            gpio_put(DM_LSTEP_GPIO, 0);
            leftState = false;
            leftSteps--;
        }
    } else {
        // Not in motion, remain at zero
        gpio_put(DM_LSTEP_GPIO, 0);
        leftState = false;
    }

    // Step the right motor
    if (rightSteps > 0) {
        if (!rightState) {
            gpio_put(DM_RSTEP_GPIO, 1);
            rightState = true;
        } else {
            gpio_put(DM_RSTEP_GPIO, 0);
            rightState = false;
            rightSteps--;
        }
    } else {
        // Not in motion, remain at zero
        gpio_put(DM_RSTEP_GPIO, 0);
        rightState = false;
    }

    return true;
}

void driveMotorsEnable(bool state)
{
    if (state) gpio_put(DM_ENABLE_GPIO, 1);
    else gpio_put(DM_ENABLE_GPIO, 0);
}

void driveMotorSetDir(motor_side_t side, motor_direction_t direction)
{
    if (side == MOTOR_LEFT) {
        if (direction == MOTOR_FORWARDS) gpio_put(DM_LDIR_GPIO, 1);
        else gpio_put(DM_LDIR_GPIO, 0);
    }
    
    if (side == MOTOR_RIGHT) {
        if (direction == MOTOR_FORWARDS) gpio_put(DM_RDIR_GPIO, 0);
        else gpio_put(DM_RDIR_GPIO, 1);
    }
}

void driveMotorSetSteps(motor_side_t side, uint16_t steps)
{
    // Add the required number of steps to the remaining steps for the motor...
    if (steps > 0) {
        if (side == MOTOR_LEFT) leftSteps += steps;
        if (side == MOTOR_RIGHT) rightSteps += steps;
    }
}