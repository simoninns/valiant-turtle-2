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
 
fifoBuffer_t input_buffer[NUMBER_OF_BUFFERS];
fifoBuffer_t output_buffer[NUMBER_OF_BUFFERS];

// Note: Do not use debug.h in this module - since debug requires the FIFO for output
// to Bluetooth, it can cause a race condition and crash.  Better to simply panic()

void fifo_initialise(void) {
    for (int i = 0; i < NUMBER_OF_BUFFERS; i++){
        // Initialise the input buffer
        input_buffer[i].head = 0;
        input_buffer[i].tail = 0;
        input_buffer[i].data = malloc(sizeof(char*) * (IN_BUFFER_KSIZE * 1024));

        if (!input_buffer[i].data) {
            panic("fifo_initialise(): Input buffer memory allocation failed!"); 
            exit(0); 
        }

        // Initialise the output buffer
        output_buffer[i].head = 0;
        output_buffer[i].tail = 0;
        output_buffer[i].data = malloc(sizeof(char*) * (OUT_BUFFER_KSIZE * 1024));

        if (!output_buffer[i].data) {
            panic("fifo_initialise(): Output buffer memory allocation failed!"); 
            exit(0); 
        }
    }
}
 
// Reads a byte from the buffer and return 0 if buffer empty
char fifo_in_read(uint16_t buffer_number) {
    if (input_buffer[buffer_number].head == input_buffer[buffer_number].tail) return 0;
    input_buffer[buffer_number].tail = (input_buffer[buffer_number].tail + 1) % (IN_BUFFER_KSIZE * 1024);
    return input_buffer[buffer_number].data[input_buffer[buffer_number].tail];
}
 
// Writes a byte to the buffer if not full
bool fifo_in_write(uint16_t buffer_number, char val) {
    if (input_buffer[buffer_number].head + 1 == input_buffer[buffer_number].tail) {
        return false;
    }
    input_buffer[buffer_number].head = (input_buffer[buffer_number].head + 1) % (IN_BUFFER_KSIZE * 1024);
    input_buffer[buffer_number].data[input_buffer[buffer_number].head] = val;
    return true;
}

// Reads a byte from the buffer and return 0 if buffer empty
char fifo_out_read(uint16_t buffer_number) {
    if (output_buffer[buffer_number].head == output_buffer[buffer_number].tail) return 0;
    output_buffer[buffer_number].tail = (output_buffer[buffer_number].tail + 1) % (OUT_BUFFER_KSIZE * 1024);
    return output_buffer[buffer_number].data[output_buffer[buffer_number].tail];
}
 
// Writes a byte to the buffer if not full
bool fifo_out_write(uint16_t buffer_number, char val) {
   if (output_buffer[buffer_number].head + 1 == output_buffer[buffer_number].tail)  {
        return false;
    }
    output_buffer[buffer_number].head = (output_buffer[buffer_number].head + 1) % (OUT_BUFFER_KSIZE * 1024);
    output_buffer[buffer_number].data[output_buffer[buffer_number].head] = val;
    return true;
}

bool fifo_is_in_empty(uint16_t buffer_number) {
    if (input_buffer[buffer_number].head == input_buffer[buffer_number].tail) return true;
    return false;
}

bool fifo_is_out_empty(uint16_t buffer_number) {
    if (output_buffer[buffer_number].head == output_buffer[buffer_number].tail) return true;
    return false;
}