/************************************************************************ 

    velocity.h

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

#ifndef VELOCITY_H_
#define VELOCITY_H_

#define INITIAL_SEQUENCE_SIZE 8

// Sequence array structure 
struct velocity_sequence { 
    size_t size; 
    size_t capacity; 
    int32_t* steps;
    int32_t* sps; 
};

typedef struct velocity_sequence velocity_sequence_t;

void velocity_calculator_init(velocity_sequence_t** sequence);
int32_t velocity_calculator(velocity_sequence_t* container, int32_t requiredSteps, int32_t accSpsps, int32_t minimumSps, int32_t maximumSps, int32_t updatesPerSecond);
void velocity_calculator_free(velocity_sequence_t* container);
int32_t velocity_get_steps(velocity_sequence_t* container, int32_t index);
int32_t velocity_get_sps(velocity_sequence_t* container, int32_t index);
int32_t velocity_get_size(velocity_sequence_t* container);

void velocity_sequence_insert(velocity_sequence_t* container, int32_t steps, int32_t sps);

#endif /* VELOCITY_H_ */