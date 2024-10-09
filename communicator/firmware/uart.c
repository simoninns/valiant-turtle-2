/************************************************************************ 

    uart.c

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

#include <stdio.h>
#include <pico/stdlib.h>
#include <string.h>
#include "hardware/uart.h"
#include "hardware/irq.h"

#include "uart.h"
#include "debug.h"
#include "fsm.h"

static uint16_t pos = 0;

void uart_initialise()
{
    // Configure UART0 (Debug)
    uart_init(UART0_ID, UART0_BAUD_RATE);
    gpio_set_function(UART0_TX_PIN, UART_FUNCSEL_NUM(UART0_ID, UART0_TX_PIN));
    gpio_set_function(UART0_RX_PIN, UART_FUNCSEL_NUM(UART0_ID, UART0_RX_PIN));
    uart_set_hw_flow(UART0_ID, false, false);
    uart_set_format(UART0_ID, UART0_DATA_BITS, UART0_STOP_BITS, UART0_PARITY);

    // Configure UART1 (Connection to robot controlling computer)
    uart_init(UART1_ID, UART1_BAUD_RATE);
    gpio_set_function(UART1_TX_PIN, UART_FUNCSEL_NUM(UART1_ID, UART1_TX_PIN));
    gpio_set_function(UART1_RX_PIN, UART_FUNCSEL_NUM(UART1_ID, UART1_RX_PIN));

    gpio_set_function(UART1_RTS_PIN, UART_FUNCSEL_NUM(UART1_ID, UART1_RTS_PIN));
    gpio_set_function(UART1_CTS_PIN, UART_FUNCSEL_NUM(UART1_ID, UART1_CTS_PIN));

    uart_set_hw_flow(UART1_ID, true, true); // CTS on, RTS on
    uart_set_format(UART1_ID, UART1_DATA_BITS, UART1_STOP_BITS, UART1_PARITY);

    // Turn off UART1 FIFO
    uart_set_fifo_enabled(UART1_ID, false);

    // Enable receive interrupt on UART1
    irq_set_exclusive_handler(UART1_IRQ, uart_rx_callback);
    irq_set_enabled(UART1_IRQ, true);

    // static void uart_set_irqs_enabled (uart_inst_t *uart, bool rx_has_data, bool tx_needs_data)
    uart_set_irq_enables(UART1_ID, true, false);
}

void uart_rx_callback()
{
    while (uart_is_readable(UART1_ID)) {
        // Get the received byte
        uint8_t ch = uart_getc(UART1_ID);

        // Process the byte
        fsm_process(ch);
    }
}