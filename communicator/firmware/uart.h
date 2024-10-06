/************************************************************************ 

    uart.h

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

#ifndef UART_H_
#define UART_H_

#define UART0_ID uart0
#define UART0_TX_PIN 0
#define UART0_RX_PIN 1
#define UART0_BAUD_RATE 115200

#define UART1_ID uart1
#define UART1_TX_PIN 4
#define UART1_RX_PIN 5
#define UART1_BAUD_RATE 4800

void uart_initialise(void);

#endif /* UART_H_ */