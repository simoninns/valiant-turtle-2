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
stepperMotor_t leftMotor;
stepperMotor_t rightMotor;

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
    driveMotorSetSpeed(MOTOR_LEFT, 0);
    driveMotorSetSpeed(MOTOR_RIGHT, 0);

    // Set remaining steps to zero
    leftMotor.steps = 0;
    rightMotor.steps = 0;
    
    // Set the initial step states to off
    leftMotor.state = 0;
    rightMotor.state = 0;

    // Set the initial speeds
    leftMotor.currentSpeed = 0;
    rightMotor.currentSpeed = 0;
    leftMotor.targetSpeed = 0;
    rightMotor.targetSpeed = 0;

    // Set up the repeating motor update timer
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
    if (leftMotor.steps > 0) {
        if (leftMotor.state == 0) {
            gpio_put(DM_LSTEP_GPIO, 1);
            leftMotor.state++;
        } else {
            gpio_put(DM_LSTEP_GPIO, 0);
            leftMotor.state++;
        }

        // Reset the steps according to speed
        if (leftMotor.state > leftMotor.currentSpeed) {
            leftMotor.state = 0;
            leftMotor.steps--; 
        }
    } else {
        // No left steps remaining - hold at zero
        gpio_put(DM_LSTEP_GPIO, 0);
        leftMotor.state = 0;
    }

    // Step the right motor
    if (rightMotor.steps > 0) {
        if (rightMotor.state == 0) {
            gpio_put(DM_RSTEP_GPIO, 1);
            rightMotor.state++;
        } else {
            gpio_put(DM_RSTEP_GPIO, 0);
            rightMotor.state++;
        }

        // Reset the steps according to speed
        if (rightMotor.state > rightMotor.currentSpeed) {
            rightMotor.state = 0;
            rightMotor.steps--; 
        }
    } else {
        // No right steps remaining - hold at zero
        gpio_put(DM_RSTEP_GPIO, 0);
        rightMotor.state = 0;
    }

    return true;
}

void driveMotorsEnable(bool state)
{
    if (state) {
        gpio_put(DM_ENABLE_GPIO, 1);
        debugPrintf("Drive motors: DRV8825 Motors enabled\r\n");
    } else {
        gpio_put(DM_ENABLE_GPIO, 0);
        debugPrintf("Drive motors: DRV8825 Motors disabled\r\n");
    }
}

void driveMotorSetDir(motor_side_t side, motor_direction_t direction)
{
    if (side == MOTOR_LEFT) {
        if (direction == MOTOR_FORWARDS) {
            gpio_put(DM_LDIR_GPIO, 1);
            debugPrintf("Drive motors: DRV8825 Left motor direction forwards\r\n");
        }
        else {
            gpio_put(DM_LDIR_GPIO, 0);
            debugPrintf("Drive motors: DRV8825 Left motor direction reverse\r\n");
        }
    }
    
    if (side == MOTOR_RIGHT) {
        if (direction == MOTOR_FORWARDS) {
            gpio_put(DM_RDIR_GPIO, 0);
            debugPrintf("Drive motors: DRV8825 Right motor direction forwards\r\n");
        } else {
            gpio_put(DM_RDIR_GPIO, 1);
            debugPrintf("Drive motors: DRV8825 Right motor direction reverse\r\n");
        }
    }
}

void driveMotorSetSteps(int16_t lSteps, int16_t rSteps)
{
    // Add the required number of steps to the remaining steps for the motor...
    leftMotor.steps += lSteps;
    rightMotor.steps += rSteps;
    debugPrintf("Drive motors: Added motor steps Left %d - Right %d\r\n", lSteps, rSteps);
}

void driveMotorSetSpeed(motor_side_t side, int16_t speed)
{
    if (speed < 0) speed = 0;
    if (speed > 9) speed = 9;

    int16_t stepNums;
    if (speed == 0) stepNums =  1; // Fastest
    if (speed == 1) stepNums =  2;
    if (speed == 2) stepNums =  3;  
    if (speed == 3) stepNums =  4;
    if (speed == 4) stepNums =  5;
    if (speed == 5) stepNums =  6;
    if (speed == 6) stepNums =  7;
    if (speed == 7) stepNums =  8;
    if (speed == 8) stepNums =  9;
    if (speed == 9) stepNums = 10; // Slowest

    if (side == MOTOR_LEFT) {
        leftMotor.currentSpeed = stepNums;
        debugPrintf("Drive motors: Set left motor speed to %d\r\n", speed);
    }

    if (side == MOTOR_RIGHT) {
        rightMotor.currentSpeed = stepNums;
        debugPrintf("Drive motors: Set right motor speed to %d\r\n", speed);
    }
}