/************************************************************************ 

    fifo.h

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

#ifndef FIFO_H_
#define FIFO_H_

#define IN_BUFFER_SIZE 64
#define OUT_BUFFER_SIZE 1024

typedef struct {
    int16_t head;
    int16_t tail;
    char* data;
} fifoBuffer_t;

void fifoInitialise(void);

char fifoInRead(void);
char fifoInWrite(char val);

char fifoOutRead(void);
char fifoOutWrite(char val);

bool fifoIsInEmpty(void);
bool fifoIsOutEmpty(void);

#endif /* FIFO_H_ */