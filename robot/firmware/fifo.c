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
 
char buffer[BUFFER_SIZE];
int16_t head;
int16_t tail;
int16_t count; 

void fifoInitialise(void)
{
    head = 0;
    tail = 0;
    count = 0; 
}
 
// Reads a byte from the buffer and return 0 if buffer empty
char fifoRead(void)
{
   if (head == tail) return 0;
   tail = (tail + 1) % BUFFER_SIZE;
   return buffer[tail];
}
 
// Writes a byte to the buffer if not full
char fifoWrite(char val)
{
   if (head + 1 == tail) return 0;
   head = (head + 1) % BUFFER_SIZE;
   return buffer[head] = val;
}

// Return the current buffer size
int16_t fifoSize(void)
{
    return head - tail;
}