/************************************************************************ 

    metric.c

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
#include <math.h>

#include "pico/stdlib.h"

#include "stepper.h"
#include "metric.h"
#include "debug.h"

// Globals
metric_config_t metric_config;

// Initialise the metric to step module
void metric_initialise()
{
    // Set the initial configuration
    metric_config.wheel_diameter_mm = 55.0;
    metric_config.axel_distance_mm = 230.0;
    metric_config.steps_per_revolution = 800;
}

// Return the current configuration
metric_config_t metric_get_config(void)
{
    return metric_config;
}

// Set the current configuration
void metric_set_config(metric_config_t config)
{
    metric_config.wheel_diameter_mm = config.wheel_diameter_mm;
    metric_config.axel_distance_mm = config.axel_distance_mm;
    metric_config.steps_per_revolution = config.steps_per_revolution;
}

// Calculate the stepper settings to move forwards a specified number of millimeters
metric_result_t metric_forwards(float distance_mm)
{
    metric_result_t result;

    // Set both steppers to forwards
    result.left_direction = STEPPER_FORWARDS;
    result.right_direction = STEPPER_FORWARDS;

    // Calculate the required number of steps
    result.left_steps = metric_mm_to_steps(distance_mm);
    result.right_steps = metric_mm_to_steps(distance_mm);

    return result;
}

// Calculate the stepper settings to move backwards a specified number of millimeters
metric_result_t metric_backwards(float distance_mm)
{
    metric_result_t result;

    // Set both steppers to backwards
    result.left_direction = STEPPER_BACKWARDS;
    result.right_direction = STEPPER_BACKWARDS;

    // Calculate the required number of steps
    result.left_steps = metric_mm_to_steps(distance_mm);
    result.right_steps = metric_mm_to_steps(distance_mm);

    return result;
}

// Calculate the stepper settings to rotate left a specified number of degrees
metric_result_t metric_left(float degrees)
{
    metric_result_t result;

    // Set steppers to counter-rotate left
    result.left_direction = STEPPER_FORWARDS;
    result.right_direction = STEPPER_BACKWARDS;

    // Calculate the required number of steps
    result.left_steps = metric_deg_to_steps(degrees);
    result.right_steps = metric_deg_to_steps(degrees);

    return result;
}

// Calculate the stepper settings to rotate right a specified number of degrees
metric_result_t metric_right(float degrees)
{
    metric_result_t result;

    // Set steppers to counter-rotate right
    result.left_direction = STEPPER_BACKWARDS;
    result.right_direction = STEPPER_FORWARDS;

    // Calculate the required number of steps
    result.left_steps = metric_deg_to_steps(degrees);
    result.right_steps = metric_deg_to_steps(degrees);

    return result;
}

// Conversion functions ------------------------------------------------------

// Convert millimeters to steps
int32_t metric_mm_to_steps(float millimeters) {
    float circumference = (2.0 * M_PI) * (metric_config.wheel_diameter_mm / 2.0); // C = 2pi x r 
    float mm_per_step = (circumference / metric_config.steps_per_revolution);
    return (int32_t)roundf(millimeters / mm_per_step);
}

// Convert degrees to steps
int32_t metric_deg_to_steps(float degrees) {
    float circumference = (2.0 * M_PI) * (metric_config.axel_distance_mm / 2.0);
    float millimeters = (circumference / 360.0) * degrees;
    return metric_mm_to_steps(millimeters);
}
