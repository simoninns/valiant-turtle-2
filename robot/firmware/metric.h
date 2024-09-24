/************************************************************************ 

    metric.h

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

#ifndef METRIC_H_
#define METRIC_H_

// Type definition for metric configuration
typedef struct metric_config_t {
    float wheel_diameter_mm;
    float axel_distance_mm;
    float steps_per_revolution;
} metric_config_t;

// Type definition for metric calculation result
typedef struct metric_result_t {
    int32_t left_steps;
    int32_t right_steps;
    stepper_direction_t left_direction;
    stepper_direction_t right_direction;
} metric_result_t;

void metric_initialise(void);
metric_config_t metric_get_config(void);
void metric_set_config(metric_config_t config);

metric_result_t metric_forwards(float distance_mm);
metric_result_t metric_backwards(float distance_mm);
metric_result_t metric_left(float degrees);
metric_result_t metric_right(float degrees);

int32_t metric_mm_to_steps(float millimeters);
int32_t metric_deg_to_steps(float degrees);

#endif /* METRIC_H_ */