/************************************************************************ 

    metricmotion.c

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
#include <math.h>

#include "metricmotion.h"
#include "stepconf.h"
#include "debug.h"

void metricmotion_forwards(int32_t millimeters) {
    int32_t steps = metricmotion_mm_to_steps(millimeters);
    debug_printf("metricmotion_forwards(): Moving forwards %d mm using %d steps\r\n", millimeters, steps);

    // Set steppers to move forwards
    stepconf_set_direction(STEPPER_FORWARDS);
    stepconf_run(steps);
}

void metricmotion_backwards(int32_t millimeters) {
    int32_t steps = metricmotion_mm_to_steps(millimeters);
    debug_printf("metricmotion_backwards(): Moving backwards %d mm using %d steps\r\n", millimeters, steps);

    // Set steppers to move backwards
    stepconf_set_direction(STEPPER_BACKWARDS);
    stepconf_run(steps);
}

void metricmotion_left(int32_t degrees) {
    int32_t steps = metricmotion_deg_to_steps(degrees);

    debug_printf("metricmotion_left(): Moving left %d degrees using %d steps\r\n", degrees, steps);

    // Set steppers to move left
    stepconf_set_direction(STEPPER_LEFT);
    stepconf_run(steps);
}

void metricmotion_right(int32_t degrees) {
    int32_t steps = metricmotion_deg_to_steps(degrees);
    debug_printf("metricmotion_right(): Moving right %d degrees using %d steps\r\n", degrees, steps);

    // Set steppers to move right
    stepconf_set_direction(STEPPER_RIGHT);
    stepconf_run(steps);
}

// Convert millimeters to steps
int32_t metricmotion_mm_to_steps(int32_t millimeters) {
    float circumference = (2.0 * M_PI) * (WHEEL_DIAMETER_MM / 2.0); // C = 2pi x r 
    float mm_per_step = (circumference / STEPS_PER_REV);
    return (int32_t)roundf((float)millimeters / mm_per_step);
}

// Convert degrees to steps
int32_t metricmotion_deg_to_steps(int32_t degrees) {
    float circumference = (2.0 * M_PI) * (AXEL_WIDTH / 2);
    float millimeters = (circumference / 360.0) * (float)degrees;

    return metricmotion_mm_to_steps((int32_t)roundf(millimeters));
}