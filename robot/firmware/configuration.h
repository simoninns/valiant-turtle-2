/************************************************************************ 

    configuration.h

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

#ifndef CONFIGURATION_H_
#define CONFIGURATION_H_

#define CONFIG_VERSION 2

// Typedef for stepper's velocity configuration
typedef struct stepper_configuration_t {
    int32_t accSpsps;
    int32_t minimumSps;
    int32_t maximumSps;
    int32_t updatesPerSecond;
} stepper_configuration_t;

// Type definition for metric configuration
typedef struct metric_configuration_t {
    float wheel_diameter_mm;
    float axel_distance_mm;
    float steps_per_revolution;
} metric_configuration_t;

// Type definition for overall stepper configuration
typedef struct configuration_t {
    uint16_t version_number;
    metric_configuration_t metric_config;
    stepper_configuration_t stepper_left;
    stepper_configuration_t stepper_right;
} configuration_t;

void configuration_initialise(void);
configuration_t configuration_get_default(void);
configuration_t configuration_get(void);
void configuration_set(configuration_t configuration);
void configuration_store(configuration_t configuration);
configuration_t configuration_retrieve(void);

#endif /* CONFIGURATION_H_ */