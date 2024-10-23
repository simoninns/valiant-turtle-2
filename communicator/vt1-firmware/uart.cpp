/************************************************************************ 

    uart.cpp

    Valiant Turtle Communicator 2
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

#include <cstdio>
#include <iostream>
#include "pico/stdlib.h"

#include "uart.h"

// Initialise the UART
Uart::Uart(uart_inst_t* _uart_id, int8_t _tx_gpio, int8_t _rx_gpio, int32_t _baud_rate) {
    uart_id = _uart_id;
    tx_gpio = _tx_gpio;
    rx_gpio = _rx_gpio;

    // Other defaults
    baud_rate = _baud_rate;
    data_bits = 8;
    stop_bits = 1;
    parity = PARITY_NONE;
    rx_callback_set = false;

    // Configure the UART hardware
    uart_init(uart_id, baud_rate);

    gpio_set_function(tx_gpio, UART_FUNCSEL_NUM(uart_id, tx_gpio));
    gpio_set_function(rx_gpio, UART_FUNCSEL_NUM(uart_id, rx_gpio));

    // Turn hardware flow control off
    set_hardware_flow_off();

    // Set UART format
    uart_parity_t uart_parity = UART_PARITY_NONE;
    if (parity == PARITY_EVEN) uart_parity = UART_PARITY_EVEN;
    if (parity == PARITY_ODD) uart_parity = UART_PARITY_ODD;
    uart_set_format(uart_id, data_bits, stop_bits, uart_parity);
}

// Define CTS/RTS and enable hardware flow control
void Uart::set_hardware_flow_on(int8_t _rts_gpio, int8_t _cts_gpio) {
    rts_gpio = _rts_gpio;
    cts_gpio = _cts_gpio;
    flow_control = FLOW_HARD;

    gpio_set_function(rts_gpio, UART_FUNCSEL_NUM(uart_id, rts_gpio));
    gpio_set_function(cts_gpio, UART_FUNCSEL_NUM(uart_id, cts_gpio));

    uart_set_hw_flow(uart_id, true, true); // CTS on, RTS on
}

// Disable hardware flow control
void Uart::set_hardware_flow_off(void) {
    flow_control = FLOW_NONE;
    rts_gpio = -1;
    cts_gpio = -1;

    uart_set_hw_flow(uart_id, false, false); // CTS off, RTS off
}

// Register an Rx callback
bool Uart::set_rx_callback(callback_t _rx_callback) {
    // Turn off UART FIFO
    uart_set_fifo_enabled(uart_id, false);

    // Figure out which IRQ to use
    irq_num_t irq;
    if (uart_id == uart0) irq = UART0_IRQ;
    else if (uart_id == uart1) irq = UART1_IRQ;
    else {
        std::cerr << "Uart::set_rx_callback(): Cannot set IRQ for UART - UART isn't 0 or 1?" << std::endl;
        return false;
    }

    // Save the callback procedure
    rx_callback = _rx_callback;

    // Flag that a callback is set
    rx_callback_set = true;

    // Enable receive interrupt on UART
    irq_set_exclusive_handler(irq, rx_callback);
    irq_set_enabled(irq, true);
    uart_set_irq_enables(uart_id, true, false);

    std::cerr << "Uart::set_rx_callback(): Rx Callback registered" << std::endl;

    return true;
}

// Get a character from the UART
uint8_t Uart::getc(void) {
    return uart_getc(uart_id);
}

// Put a character to the UART
void Uart::putc(uint8_t c) {
    uart_putc(uart_id, c);
}

// Put a string to the UART
void Uart::puts(const char* s) {
    while (*s)
        putc(*s++);
}

// Check if UART is readable
bool Uart::is_readable(void) {
    return uart_is_readable(uart_id);
}
