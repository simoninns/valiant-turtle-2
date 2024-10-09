/************************************************************************ 

    ir.h

    Valiant Turtle 2 Communicator - Raspberry Pi Pico W Firmware
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

#ifndef IR_H_
#define IR_H_

void ir_initialise(void);
void ir_pulse(int32_t delay_time_us);
bool ir_isBitSet(uint8_t value, uint8_t bitIndex);
uint8_t ir_parity(uint8_t x);
void ir_send_byte(uint8_t tx_byte);

#endif /* IR_H_ */