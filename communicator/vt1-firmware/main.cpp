/************************************************************************ 

    main.c

    Valiant Turtle Communicator 2
    Copyright (C) 2024 Simon Inns

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
#include "hardware/i2c.h"

#include "logging.h"
#include "led.h"
#include "uart.h"
#include "ir.h"
#include "i2c.h"
#include "parallel.h"
#include "config.h"

// Initialise logging
log_level_e log_level = log_error;

// Initialise UART 0
Uart uart_debug(uart0, 0, 1, 115200);

// Initialise the DCE UART as global
Uart uart_dce(uart1, 4, 5, 4800);

// Initialise I2C
I2c i2c(i2c0, 8, 9);

// Initialise the IR interface as global
Ir ir(22);

// Initialise Parallel port as global
Parallel parallel;

// Callback when data is received on the serial port
void uart_rx_callback() {
    while (uart_dce.is_readable()) {
        // Get the received byte
        uint8_t ch = uart_dce.getc();

        // Send the byte over IR to the robot
        ir.putc(ch);
    }
}

// Callback when data is received on the parallel port
void parallel_rx_callback() {
    // Get the received byte
    uint8_t ch = parallel.get_data();

    // ACK the byte
    parallel.ack();
    
    // Send the byte over IR to the robot
    ir.putc(ch);
    
    // ACK the IRQ and return
    gpio_acknowledge_irq(MCP23017_INT_GPIO, GPIO_IRQ_EDGE_FALL);
}

int main() {
    stdio_init_all(); // Initialize standard IO

    // Set the maximum overall log level
    //log_level = log_info;
    log_level = log_debug;

    log(log_info) << "";
    log(log_info) << "";
    log(log_info) << "Valiant Turtle 2 - Communicator debug active";
    log(log_info) << "";

    // Initialise the status LEDs
    Led green_led(16); // Green LED on GPIO 16
    Led blue_led(18); // Green LED on GPIO 18

    // Flash the status LEDs in the foreground
    green_led.set_state(true);
    blue_led.set_state(false);

    // Turn on hardware flow control for the DCE UART
    uart_dce.set_hardware_flow_on(6, 7);

    // Register an Rx callback on uart_dce to start
    // copying from the DCE UART to IR
    uart_dce.set_rx_callback(uart_rx_callback);

    // Register an Rx callback on the parallel port
    parallel.set_rx_callback(parallel_rx_callback);

    // Test configuration class
    Config config(i2c0, 0x50);

    int hb = 0;
    while (true) {
        blue_led.set_state(true);
        sleep_ms(750);
        blue_led.set_state(false);
        sleep_ms(250);

        hb++;
        if (hb == 50) hb = 0;
        //log(log_info) << "main(): Heatbeat = " << hb;
    }
}