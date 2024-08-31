/************************************************************************ 

    fifo.c

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
#include <pico/stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#include "fifo.h"
#include "debug.h"
 
fifoBuffer_t input_buffer;
fifoBuffer_t output_buffer;

void fifo_initialise(void) {
    // Initialise the input buffer
    input_buffer.head = 0;
    input_buffer.tail = 0;
    input_buffer.data = malloc(sizeof(char*) * IN_BUFFER_SIZE);

    if (!input_buffer.data) {
        debug_printf("fifo_initialise(): Input buffer memory allocation failed\n"); 
        exit(0); 
    }

    // Initialise the output buffer
    output_buffer.head = 0;
    output_buffer.tail = 0;
    output_buffer.data = malloc(sizeof(char*) * OUT_BUFFER_SIZE);

    if (!input_buffer.data) {
        debug_printf("fifo_initialise(): Output buffer memory allocation failed\n"); 
        exit(0); 
    }
}
 
// Reads a byte from the buffer and return 0 if buffer empty
char fifo_in_read(void) {
   if (input_buffer.head == input_buffer.tail) return 0;
   input_buffer.tail = (input_buffer.tail + 1) % IN_BUFFER_SIZE;
   return input_buffer.data[input_buffer.tail];
}
 
// Writes a byte to the buffer if not full
char fifo_in_write(char val) {
   if (input_buffer.head + 1 == input_buffer.tail) return 0;
   input_buffer.head = (input_buffer.head + 1) % IN_BUFFER_SIZE;
   return input_buffer.data[input_buffer.head] = val;
}

// Reads a byte from the buffer and return 0 if buffer empty
char fifo_out_read(void) {
   if (output_buffer.head == output_buffer.tail) return 0;
   output_buffer.tail = (output_buffer.tail + 1) % OUT_BUFFER_SIZE;
   return output_buffer.data[output_buffer.tail];
}
 
// Writes a byte to the buffer if not full
char fifo_out_write(char val) {
   if (output_buffer.head + 1 == output_buffer.tail) return 0;
   output_buffer.head = (output_buffer.head + 1) % OUT_BUFFER_SIZE;
   return output_buffer.data[output_buffer.head] = val;
}

bool fifo_is_in_empty(void) {
    if (input_buffer.head == input_buffer.tail) return true;
    return false;
}

bool fifo_is_out_empty(void) {
    if (output_buffer.head == output_buffer.tail) return true;
    return false;
}