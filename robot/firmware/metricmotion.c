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
    float circumference = (2.0 * M_PI) * (WHEEL_DIAMETER_MM / 2.0); // C = 2pi x r 
    float mm_per_step = (circumference / STEPS_PER_REV);
    int32_t steps = (int32_t)roundf((float)millimeters / mm_per_step);

    debug_printf("metricmotion_forwards(): Circumference = %f mm, mm per step = %f mm\\r\n", circumference, mm_per_step);
    debug_printf("metricmotion_forwards(): Moving forwards %d mm using %d steps\r\n", millimeters, steps);

    // Set both steppers to move forwards
    stepconf_set_direction(STEPPER_LEFT, STEPPER_FORWARDS);
    stepconf_set_direction(STEPPER_RIGHT, STEPPER_FORWARDS);

    // Move
    stepconf_run_both(steps, steps);
}

void metricmotion_backwards(int32_t millimeters) {
    float circumference = (2.0 * M_PI) * (WHEEL_DIAMETER_MM / 2.0); // C = 2pi x r 
    float mm_per_step = (circumference / STEPS_PER_REV);
    int32_t steps = (int32_t)roundf((float)millimeters / mm_per_step);

    debug_printf("metricmotion_backwards(): Circumference = %f mm, mm per step = %f mm\\r\n", circumference, mm_per_step);
    debug_printf("metricmotion_backwards(): Moving backwards %d mm using %d steps\r\n", millimeters, steps);

    // Set both steppers to move forwards
    stepconf_set_direction(STEPPER_LEFT, STEPPER_BACKWARDS);
    stepconf_set_direction(STEPPER_RIGHT, STEPPER_BACKWARDS);

    // Move
    stepconf_run_both(steps, steps);
}

void metricmotion_left(int32_t degrees) {
    float degrees_per_step = 90.0 / STEPS_PER_REV;
    int32_t steps = (int32_t)roundf((float)degrees / degrees_per_step);

    debug_printf("metricmotion_left(): Degrees per step = %f mm\\r\n", degrees_per_step);
    debug_printf("metricmotion_left(): Moving left %d degrees using %d steps\r\n", degrees, steps);

    // Set both steppers to move left
    stepconf_set_direction(STEPPER_LEFT, STEPPER_FORWARDS);
    stepconf_set_direction(STEPPER_RIGHT, STEPPER_BACKWARDS);

    // Move
    stepconf_run_both(steps, steps);
}

void metricmotion_right(int32_t degrees) {
    float degrees_per_step = 90.0 / STEPS_PER_REV;
    int32_t steps = (int32_t)roundf((float)degrees / degrees_per_step);

    debug_printf("metricmotion_right(): Degrees per step = %f mm\\r\n", degrees_per_step);
    debug_printf("metricmotion_right(): Moving right %d degrees using %d steps\r\n", degrees, steps);

    // Set both steppers to move right
    stepconf_set_direction(STEPPER_LEFT, STEPPER_BACKWARDS);
    stepconf_set_direction(STEPPER_RIGHT, STEPPER_FORWARDS);

    // Move
    stepconf_run(STEPPER_LEFT, steps);
    stepconf_run(STEPPER_RIGHT, steps);
}