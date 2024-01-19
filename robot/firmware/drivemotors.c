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
#include "btcomms.h"

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
    gpio_init(DM_LM0_GPIO);
    gpio_init(DM_LM1_GPIO);
    gpio_init(DM_RM0_GPIO);
    gpio_init(DM_RM1_GPIO);

    // Set the drive motor control GPIO directions
    gpio_set_dir(DM_ENABLE_GPIO, GPIO_OUT);
    gpio_set_dir(DM_LSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(DM_RSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(DM_LDIR_GPIO, GPIO_OUT);
    gpio_set_dir(DM_RDIR_GPIO, GPIO_OUT);
    gpio_set_dir(DM_LM0_GPIO, GPIO_OUT);
    gpio_set_dir(DM_LM1_GPIO, GPIO_OUT);
    gpio_set_dir(DM_RM0_GPIO, GPIO_OUT);
    gpio_set_dir(DM_RM1_GPIO, GPIO_OUT);

    // Default values
    driveMotorsEnable(false);
    driveMotorsRunning(false);
    driveMotorSetDir(MOTOR_LEFT, MOTOR_FORWARDS);
    driveMotorSetDir(MOTOR_RIGHT, MOTOR_FORWARDS);
    driveMotorSetSpeed(MOTOR_LEFT, MOTOR_1_8);
    driveMotorSetSpeed(MOTOR_RIGHT, MOTOR_1_8);

    // Set remaining steps to zero
    leftMotor.steps = 0;
    rightMotor.steps = 0;
    
    // Set the initial step states to off
    leftMotor.state = 0;
    rightMotor.state = 0;

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
    if (leftMotor.enabled && leftMotor.running) {
        // Step the left motor
        if (leftMotor.steps > 0) {
            if (leftMotor.state == 0) {
                gpio_put(DM_LSTEP_GPIO, 1);
                leftMotor.state++;
            } else {
                gpio_put(DM_LSTEP_GPIO, 0);
                leftMotor.state++;
            }

            // Reset the state as required
            if (leftMotor.state > 1) {
                leftMotor.state = 0;
                leftMotor.steps--; 
            }
        } else {
            // No left steps remaining - hold at zero
            gpio_put(DM_LSTEP_GPIO, 0);
            leftMotor.state = 0;
        }
    } else {
        // Left motor is inactive, hold at 0
        gpio_put(DM_LSTEP_GPIO, 0);
        leftMotor.state = 0;
    }

    if (rightMotor.enabled && rightMotor.running) {
        // Step the right motor
        if (rightMotor.steps > 0) {
            if (rightMotor.state == 0) {
                gpio_put(DM_RSTEP_GPIO, 1);
                rightMotor.state++;
            } else {
                gpio_put(DM_RSTEP_GPIO, 0);
                rightMotor.state++;
            }

            // Reset the state as required
            if (rightMotor.state > 1) {
                rightMotor.state = 0;
                rightMotor.steps--; 
            }
        } else {
            // No right steps remaining - hold at zero
            gpio_put(DM_RSTEP_GPIO, 0);
            rightMotor.state = 0;
        }
    } else {
        // Right motor is inactive, hold at 0
        gpio_put(DM_LSTEP_GPIO, 0);
        leftMotor.state = 0;
    }

    return true;
}

void driveMotorsEnable(bool state)
{
    if (state) {
        leftMotor.enabled = true;
        rightMotor.enabled = true;
        gpio_put(DM_ENABLE_GPIO, 1);
        debugPrintf("Drive motors: Motors powered on\r\n");
    } else {
        leftMotor.enabled = false;
        rightMotor.enabled = false;
        gpio_put(DM_ENABLE_GPIO, 0);
        debugPrintf("Drive motors: Motors powered off\r\n");
    }
}

void driveMotorsRunning(bool state)
{
    if (state) {
        leftMotor.running = true;
        rightMotor.running = true;
        debugPrintf("Drive motors: Motors running\r\n");
    } else {
        leftMotor.running = false;
        rightMotor.running = false;
        debugPrintf("Drive motors: Motors stopped\r\n");
    }
}

void driveMotorSetDir(motor_side_t side, motor_direction_t direction)
{
    if (side == MOTOR_LEFT) {
        if (direction == MOTOR_FORWARDS) {
            leftMotor.direction = MOTOR_FORWARDS;
            gpio_put(DM_LDIR_GPIO, 1);
            debugPrintf("Drive motors: Left motor direction forwards\r\n");
        }
        else {
            leftMotor.direction = MOTOR_BACKWARDS;
            gpio_put(DM_LDIR_GPIO, 0);
            debugPrintf("Drive motors: Left motor direction reverse\r\n");
        }
    }
    
    if (side == MOTOR_RIGHT) {
        if (direction == MOTOR_FORWARDS) {
            rightMotor.direction = MOTOR_FORWARDS;
            gpio_put(DM_RDIR_GPIO, 0);
            debugPrintf("Drive motors: Right motor direction forwards\r\n");
        } else {
            rightMotor.direction = MOTOR_BACKWARDS;
            gpio_put(DM_RDIR_GPIO, 1);
            debugPrintf("Drive motors: Right motor direction reverse\r\n");
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

// DRV8825 Microstep control table
//
// M0 M1 M2 - Resolution
//  0  0  0   Full step
//  1  0  0   Half step
//  0  1  0   1/4 step
//  1  1  0   1/8 step
//  0  0  1   1/16 step
//  1  0  1   1/32 step
//  0  1  1   1/32 step
//  1  1  1   1/32 step

void driveMotorSetSpeed(motor_side_t side, motor_speed_t speed)
{
    if (side == MOTOR_LEFT) {
        // Left motor
        leftMotor.speed = speed;

        switch(speed) {
            case MOTOR_1:
                gpio_put(DM_LM0_GPIO, 0);
                gpio_put(DM_LM1_GPIO, 0);
                debugPrintf("Drive motors: Set left motor speed to 1\r\n", speed);
                break;

            case MOTOR_1_2:
                gpio_put(DM_LM0_GPIO, 1);
                gpio_put(DM_LM1_GPIO, 0);
                debugPrintf("Drive motors: Set left motor speed to 1/2\r\n", speed);
                break;

            case MOTOR_1_4:
                gpio_put(DM_LM0_GPIO, 0);
                gpio_put(DM_LM1_GPIO, 1);
                debugPrintf("Drive motors: Set left motor speed to 1/4\r\n", speed);
                break;

            case MOTOR_1_8:
                gpio_put(DM_LM0_GPIO, 1);
                gpio_put(DM_LM1_GPIO, 1);
                debugPrintf("Drive motors: Set left motor speed to 1/8\r\n", speed);
                break;
        }
    } else {
        // Right motor
        rightMotor.speed = speed;

        switch(speed) {
            case MOTOR_1:
                gpio_put(DM_RM0_GPIO, 0);
                gpio_put(DM_RM1_GPIO, 0);
                debugPrintf("Drive motors: Set right motor speed to 1\r\n", speed);
                break;

            case MOTOR_1_2:
                gpio_put(DM_RM0_GPIO, 1);
                gpio_put(DM_RM1_GPIO, 0);
                debugPrintf("Drive motors: Set right motor speed to 1/2\r\n", speed);
                break;

            case MOTOR_1_4:
                gpio_put(DM_RM0_GPIO, 0);
                gpio_put(DM_RM1_GPIO, 1);
                debugPrintf("Drive motors: Set right motor speed to 1/4\r\n", speed);
                break;

            case MOTOR_1_8:
                gpio_put(DM_RM0_GPIO, 1);
                gpio_put(DM_RM1_GPIO, 1);
                debugPrintf("Drive motors: Set right motor speed to 1/8\r\n", speed);
                break;
        }
    }
}

void driveMotorStatus(void)
{
    // Left motor status
    btPrintf("Drive motors: Left motor status -\r\n");
    if (leftMotor.enabled) btPrintf("  Powered on\r\n");
    else btPrintf("  Powered off\r\n");
    if (leftMotor.running) btPrintf("  Running\r\n");
    else btPrintf("  Stopped\r\n");

    switch(leftMotor.speed) {
        case MOTOR_1:
            btPrintf("  Speed is 1 (200 steps per revolution)\r\n");
            break;

        case MOTOR_1_2:
            btPrintf("  Speed is 1/2 (400 steps per revolution)\r\n");
            break;

        case MOTOR_1_4:
            btPrintf("  Speed is 1/4 (800 steps per revolution)\r\n");
            break;

        case MOTOR_1_8:
            btPrintf("  Speed is 1/8 (1600 steps per revolution)\r\n");
            break;
    }

    if (leftMotor.direction == MOTOR_FORWARDS) btPrintf("  Forwards\r\n");
    else btPrintf("  Backwards\r\n");

    btPrintf("  Steps remaining: %d\r\n", leftMotor.steps);

    // Right motor status
    btPrintf("Drive motors: Right motor status -\r\n");
    if (rightMotor.enabled) btPrintf("  Powered on\r\n");
    else btPrintf("  Powered off\r\n");
    if (rightMotor.running) btPrintf("  Running\r\n");
    else btPrintf("  Stopped\r\n");

    switch(rightMotor.speed) {
        case MOTOR_1:
            btPrintf("  Speed is 1 (200 steps per revolution)\r\n");
            break;

        case MOTOR_1_2:
            btPrintf("  Speed is 1/2 (400 steps per revolution)\r\n");
            break;

        case MOTOR_1_4:
            btPrintf("  Speed is 1/4 (800 steps per revolution)\r\n");
            break;

        case MOTOR_1_8:
            btPrintf("  Speed is 1/8 (1600 steps per revolution)\r\n");
            break;
    }

    if (rightMotor.direction == MOTOR_FORWARDS) btPrintf("  Forwards\r\n");
    else btPrintf("  Backwards\r\n");

    btPrintf("  Steps remaining: %d\r\n", rightMotor.steps);
}