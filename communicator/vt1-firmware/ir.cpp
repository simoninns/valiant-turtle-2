/************************************************************************ 

    ir.cpp

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
#include "hardware/pio.h"
#include "hardware/clocks.h"

#include "ir.h"
#include "ir_uart.pio.h"

// Initialise the IR
Ir::Ir(uint8_t _ir_gpio) {
    ir_gpio = _ir_gpio;
    gpio_init(ir_gpio);

    // To-do select next free PIO and SM automatically
    // and remove the hard coded selection of PIO0

    pio = pio0;
    sm = 0;
    offset = pio_add_program(pio, &ir_uart_program);
    ir_uart_program_init(pio, sm, offset, ir_gpio);
}

// Put a character to the IR
void Ir::putc(char c)
{
    // Encode the byte into a timing word and pass it to the PIO
    pio_sm_put_blocking(pio, sm, encode(c));
}

// Put string via IR
void Ir::puts(const char *s)
{
    while (*s)
        putc(*s++);
}

// Calculate the parity bit for x
char Ir::parity(char x) {
    char y;

    y = x ^ (x >> 1);
    y = y ^ (y >> 2);
    y = y ^ (y >> 4);
    y = y ^ (y >> 8);
    y = y ^ (y >> 16);

    return y & 1;
}

// Set a bit at a bit position
uint32_t Ir::set_bit(uint32_t in_word, uint32_t bit_position) {
    return in_word | (1 << bit_position);
}

// Check if a bit is set at a bit position
bool Ir::is_bit_set(uint8_t value, uint8_t bitIndex) {
    return (value & (1 << bitIndex)) != 0;
}

// In order to keep the PIO code as simple as possible we first encode
// the required byte into a sequence of 2 bit results:
// 2 bits represent the lead-in (0b00 = 35uS or 0b01 = 60uS)
// 16 bits represent the value's 8 bits (0b00 = 50uS, 0b01 = 75uS or 0b10 = 100uS)
// 6 bits represent the 3 parity pulses (0b00 = 50uS, 0b01 = 75uS or 0b10 = 100uS)
uint32_t Ir::encode(uint8_t tx_byte) {
    uint32_t encoded_word = 0;

	// Note: The data is sent LSB first, so transmission is from
	// bit 0 to bit 6 (7-bit data).  Bit 7 should always be 0

    // Start of frame
    uint8_t bitPointer = 0;
    
    // Send the lead-in period
    //
    // This is 60 if bit 0 is a 0 or 35 if bit 0 is a 1
    if (is_bit_set(tx_byte, bitPointer)) {
        // Encoded result is 00 - do nothing
    } else {
        encoded_word = set_bit(encoded_word, 0);
    }
    
    // Send the data bit periods
    for (bitPointer = 0; bitPointer < 7; bitPointer++)
    {
        // If the current bit is 0 and the next bit is 0 output 75 uS period
        if (is_bit_set(tx_byte, bitPointer) == 0 && is_bit_set(tx_byte, bitPointer+1) == 0) {
            encoded_word = set_bit(encoded_word, (bitPointer*2) + 2);
        }
            
        // If the current bit is 0 and the next bit is 1 output 50 uS period
        if (is_bit_set(tx_byte, bitPointer) == 0 && is_bit_set(tx_byte, bitPointer+1) == 1) {
            // Encoded result is 00 - do nothing
        }
            
        // If the current bit is 1 and the next bit is 0 output 100 uS period
        if (is_bit_set(tx_byte, bitPointer) == 1 && is_bit_set(tx_byte, bitPointer+1) == 0) {
            encoded_word = set_bit(encoded_word, (bitPointer*2) + 3);
        }
            
        // If the current bit is 1 and the next bit is 1 output 75 uS period
        if (is_bit_set(tx_byte, bitPointer) == 1 && is_bit_set(tx_byte, bitPointer+1) == 1) {
            encoded_word = set_bit(encoded_word, (bitPointer*2) + 2);
        }
    }
    
    // Send the lead-out periods:
    if (parity(tx_byte) == 1) {
        // If the parity is even the lead-out periods are 50, 75 and 75
        // Encoded result is 00 - do nothing for 50
        encoded_word = set_bit(encoded_word, 18); // 75
        encoded_word = set_bit(encoded_word, 18+2); // 75
    } else {
        // If the parity is odd the lead-out periods are 50, 75 and 100
        // Encoded result is 00 - do nothing for 50
        encoded_word = set_bit(encoded_word, 18); // 75
        encoded_word = set_bit(encoded_word, 18+2+1); // 100
    }
    
    // End of frame
    return encoded_word;
}