/************************************************************************ 

    parallel.cpp

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
#include "hardware/i2c.h"

#include "parallel.h"
#include "mcp23017.h"
#include "logging.h"

// Initialise the parallel port interface
Parallel::Parallel(void) {
    // Initialise MCP23017
    mcp23017 = new Mcp23017(i2c0, 0x20);

    // Default the callback flag
    rx_callback_set = false;

    // Set pin directions (true = input, false = output)
    mcp23017->mgpio_set_dir(PARALLEL_UN0, true);
    mcp23017->mgpio_set_dir(PARALLEL_UN1, true);
    mcp23017->mgpio_set_dir(PARALLEL_NACK, false);
    mcp23017->mgpio_set_dir(PARALLEL_BUSY, false);
    mcp23017->mgpio_set_dir(PARALLEL_NDATASTROBE, true);
    mcp23017->mgpio_set_dir(PARALLEL_5, true);
    mcp23017->mgpio_set_dir(PARALLEL_6, true);
    mcp23017->mgpio_set_dir(PARALLEL_7, true);
    mcp23017->mgpio_set_dir(PARALLEL_DAT0, true);
    mcp23017->mgpio_set_dir(PARALLEL_DAT1, true);
    mcp23017->mgpio_set_dir(PARALLEL_DAT2, true);
    mcp23017->mgpio_set_dir(PARALLEL_DAT3, true);
    mcp23017->mgpio_set_dir(PARALLEL_DAT4, true);
    mcp23017->mgpio_set_dir(PARALLEL_DAT5, true);
    mcp23017->mgpio_set_dir(PARALLEL_DAT6, true);
    mcp23017->mgpio_set_dir(PARALLEL_DAT7, true);

    // Set pull ups on inputs
    mcp23017->mgpio_pull_up(PARALLEL_UN0);
    mcp23017->mgpio_pull_up(PARALLEL_UN1);
    mcp23017->mgpio_pull_up(PARALLEL_NDATASTROBE);
    mcp23017->mgpio_pull_up(PARALLEL_DAT0);
    mcp23017->mgpio_pull_up(PARALLEL_DAT1);
    mcp23017->mgpio_pull_up(PARALLEL_DAT2);
    mcp23017->mgpio_pull_up(PARALLEL_DAT3);
    mcp23017->mgpio_pull_up(PARALLEL_DAT4);
    mcp23017->mgpio_pull_up(PARALLEL_DAT5);
    mcp23017->mgpio_pull_up(PARALLEL_DAT6);
    mcp23017->mgpio_pull_up(PARALLEL_DAT7);

    // Set outputs to default
    mcp23017->mgpio_put(PARALLEL_NACK, false);
    mcp23017->mgpio_put(PARALLEL_BUSY, true);

    // Set up interrupt on PARALLEL_NDATASTROBE signal
    mcp23017->interrupt_set_default_value(PARALLEL_NDATASTROBE, true); // Set default to high
    mcp23017->interrupt_set_type(PARALLEL_NDATASTROBE, true); // Interrupt type is 'compare to default'
    mcp23017->interrupt_enable(PARALLEL_NDATASTROBE, true); // Enable interrupt

    log(log_debug) << "Parallel::Parallel(): Parallel port initialised";
}

// Get the current 8-bit data value from the parallel port
uint8_t Parallel::get_data(void) {
    uint16_t all_pins = mcp23017->mgpio_get_all();
    all_pins = (all_pins & 0xFF00) >> 8;

    return static_cast<uint8_t>(all_pins);
}

// Register an Rx callback
bool Parallel::set_rx_callback(callback_t _rx_callback) {
    // Save the callback procedure
    rx_callback = _rx_callback;

    // Set the callback
    mcp23017->set_interrupt_callback(rx_callback);

    // Flag that a callback is set
    rx_callback_set = true;

    log(log_debug) << "Parallel::set_rx_callback(): Rx Callback registered";

    return true;
}

// ACK a received byte (M6522 Handshake output mode, pull CB1 low)
void Parallel::ack() {
    mcp23017->mgpio_put(PARALLEL_BUSY, false);
    mcp23017->mgpio_put(PARALLEL_BUSY, true);
}