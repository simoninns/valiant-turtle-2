/************************************************************************ 

    fifo.c

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
#include <ctype.h>
#include <stdlib.h>

#include "fifo.h"
 
fifoBuffer_t inputBuffer;
fifoBuffer_t outputBuffer;

void fifoInitialise(void)
{
    // Initialise the input buffer
    inputBuffer.head = 0;
    inputBuffer.tail = 0;
    inputBuffer.data = malloc(sizeof(char*) * IN_BUFFER_SIZE);

    // Initialise the output buffer
    outputBuffer.head = 0;
    outputBuffer.tail = 0;
    outputBuffer.data = malloc(sizeof(char*) * OUT_BUFFER_SIZE);
}
 
// Reads a byte from the buffer and return 0 if buffer empty
char fifoInRead(void)
{
   if (inputBuffer.head == inputBuffer.tail) return 0;
   inputBuffer.tail = (inputBuffer.tail + 1) % IN_BUFFER_SIZE;
   return inputBuffer.data[inputBuffer.tail];
}
 
// Writes a byte to the buffer if not full
char fifoInWrite(char val)
{
   if (inputBuffer.head + 1 == inputBuffer.tail) return 0;
   inputBuffer.head = (inputBuffer.head + 1) % IN_BUFFER_SIZE;
   return inputBuffer.data[inputBuffer.head] = val;
}

// Reads a byte from the buffer and return 0 if buffer empty
char fifoOutRead(void)
{
   if (outputBuffer.head == outputBuffer.tail) return 0;
   outputBuffer.tail = (outputBuffer.tail + 1) % OUT_BUFFER_SIZE;
   return outputBuffer.data[outputBuffer.tail];
}
 
// Writes a byte to the buffer if not full
char fifoOutWrite(char val)
{
   if (outputBuffer.head + 1 == outputBuffer.tail) return 0;
   outputBuffer.head = (outputBuffer.head + 1) % OUT_BUFFER_SIZE;
   return outputBuffer.data[outputBuffer.head] = val;
}

bool fifoIsInEmpty(void)
{
    if (inputBuffer.head == inputBuffer.tail) return true;
    return false;
}

bool fifoIsOutEmpty(void)
{
    if (outputBuffer.head == outputBuffer.tail) return true;
    return false;
}