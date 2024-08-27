/************************************************************************ 

    seqarray.h

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

#ifndef SEQARRAY_H_
#define SEQARRAY_H_

#define INITIAL_SEQUENCE_SIZE 8

typedef struct sequence_array sequence_array_t; // Forward declaration

void seqarray_init(sequence_array_t** sequence);
void seqarray_insert(sequence_array_t* container, int32_t steps, int32_t sps);
int32_t seqarray_get_steps(sequence_array_t* container, int32_t index);
int32_t seqarray_get_sps(sequence_array_t* container, int32_t index);
void seqarray_display(sequence_array_t* container);
int32_t seqarray_get_size(sequence_array_t* container);
void seqarray_free(sequence_array_t* container);

#endif /* SEQARRAY_H_ */