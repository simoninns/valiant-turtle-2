/************************************************************************ 

    ir_uart.h

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

#ifndef IR_UART_H_
#define IR_UART_H_

// Define the UART output GPIO
#define IR_GPIO 22

void ir_uart_initialise(void);
void ir_uart_pulse(int32_t delay_time_us);
char ir_uart_parity(char x);
void ir_uart_putc(char c);
void ir_uart_puts(const char *s);
uint32_t ir_uart_setbit(uint32_t in_word, uint32_t bit_position);
bool ir_uart_isBitSet(uint8_t value, uint8_t bitIndex);
uint32_t ir_uart_encode(uint8_t tx_byte);

#endif /* IR_UART_H_ */