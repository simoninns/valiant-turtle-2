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
#include <string.h>
#include <stdarg.h>
#include "pico/printf.h"
#include "pico/stdlib.h"
#include "pico/stdio/driver.h"
#include "hardware/uart.h"
#include "hardware/irq.h"

#include "uart.h"
#include "btcomms.h"

void uart_initialise()
{
    // Configure UART0 (TTL)
    uart_init(UART0_ID, UART0_BAUD_RATE);
    gpio_set_function(UART0_TX_PIN, UART_FUNCSEL_NUM(UART0_ID, UART0_TX_PIN));
    gpio_set_function(UART0_RX_PIN, UART_FUNCSEL_NUM(UART0_ID, UART0_RX_PIN));

    uart_set_hw_flow(UART0_ID, false, false);
    uart_set_format(UART0_ID, UART0_DATA_BITS, UART0_STOP_BITS, UART0_PARITY);

    // Turn off UART0 FIFO (required for the IRQ to work)
    uart_set_fifo_enabled(UART0_ID, false);

    // Configure UART1 (RS232 DB9)
    uart_init(UART1_ID, UART1_BAUD_RATE);

    gpio_set_function(UART1_TX_PIN, UART_FUNCSEL_NUM(UART1_ID, UART1_TX_PIN));
    gpio_set_function(UART1_RX_PIN, UART_FUNCSEL_NUM(UART1_ID, UART1_RX_PIN));
    gpio_set_function(UART1_RTS_PIN, UART_FUNCSEL_NUM(UART1_ID, UART1_RTS_PIN));
    gpio_set_function(UART1_CTS_PIN, UART_FUNCSEL_NUM(UART1_ID, UART1_CTS_PIN));

    uart_set_hw_flow(UART1_ID, false, false);
    uart_set_format(UART1_ID, UART1_DATA_BITS, UART1_STOP_BITS, UART1_PARITY);

    // Enable receive interrupt on UART0
    irq_set_exclusive_handler(UART0_IRQ, uart_rx_callback);
    irq_set_enabled(UART0_IRQ, true);

    // static void uart_set_irqs_enabled (uart_inst_t *uart, bool rx_has_data, bool tx_needs_data)
    uart_set_irq_enables(UART0_ID, true, false);
}

void uart_rx_callback()
{
    while (uart_is_readable(UART0_ID)) {
        // Get the received byte
        uint8_t ch = uart_getc(UART0_ID);

        // Send the byte over Bluetooth to the robot
        if (btcomms_is_channel_open(0)) {
          btcomms_putchar(0, ch);
        }
    }
}

int printf_debug(const char *format, ...) {

  char buffer[256];
  
  va_list va;
  va_start(va, format);
  const int ret = vsnprintf(buffer, sizeof(buffer), format, va);
  va_end(va);

  // Send to USB
  printf(buffer);
}

int printf_uart0(const char *format, ...) {

  char buffer[256];
  
  va_list va;
  va_start(va, format);
  const int ret = vsnprintf(buffer, sizeof(buffer), format, va);
  va_end(va);

  // Send to UART0
  uart_puts(UART0_ID, buffer);
}

int printf_uart1(const char *format, ...) {

  char buffer[256];
  
  va_list va;
  va_start(va, format);
  const int ret = vsnprintf(buffer, sizeof(buffer), format, va);
  va_end(va);

  // Send to UART1
  uart_puts(UART1_ID, buffer);
}