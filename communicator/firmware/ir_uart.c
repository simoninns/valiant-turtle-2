/************************************************************************ 

    ir_uart.c

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
#include "hardware/pio.h"
#include "hardware/clocks.h"

#include "ir_uart.h"
#include "ir_uart.pio.h"
#include "debug.h"

// Globals
PIO pio;
uint sm;
uint offset;

// Initialise the IR UART
void ir_uart_initialise()
{
    // Initialise the IR output GPIO
    gpio_init(IR_GPIO);

    pio = pio0;
    sm = 0;
    offset = pio_add_program(pio, &ir_uart_program);
    ir_uart_program_init(pio, sm, offset, IR_GPIO);
}

void ir_uart_pulse(int32_t delay_time_us)
{
    // Send 2.5 uS pulse
    // Followed by delay_time_us pause
    debug_printf("%d ", delay_time_us);
}

// Function to calculate the parity of a byte
// Returns 0 if parity is odd and 1 if parity is even
char ir_uart_parity(char x)
{
   char y;
   
   y = x ^ (x >> 1);
   y = y ^ (y >> 2);
   y = y ^ (y >> 4);
   y = y ^ (y >> 8);
   y = y ^ (y >> 16);

   return y & 1;
}

// Put character via IR UART
void ir_uart_putc(char c)
{
    // Encode the byte into a timing word and pass it to the PIO
    pio_sm_put_blocking(pio, sm, ir_uart_encode(c));
}

// Put string via IR UART
void ir_uart_puts(const char *s)
{
    while (*s)
        ir_uart_putc(*s++);
}

uint32_t ir_uart_setbit(uint32_t in_word, uint32_t bit_position)
{
    return in_word | (1 << bit_position);
}

// Function to test if a bit is set to 1 in a byte
bool ir_uart_isBitSet(uint8_t value, uint8_t bitIndex)
{
	return (value & (1 << bitIndex)) != 0;
}

// In order to keep the PIO code as simple as possible we first encode
// the required byte into a sequence of 2 bit results:
// 2 bits represent the leadin (0b00 = 35uS or 0b01 = 60uS)
// 16 bits represent the value's 8 bits (0b00 = 50uS, 0b01 = 75uS or 0b10 = 100uS)
// 6 bits represent the 3 parity pulses (0b00 = 50uS, 0b01 = 75uS or 0b10 = 100uS)
uint32_t ir_uart_encode(uint8_t tx_byte)
{
    uint32_t encoded_word = 0;

	// Note: The data is sent LSB first, so transmission is from
	// bit 0 to bit 6 (7-bit data).  Bit 7 should always be 0

    // Start of frame
    uint8_t bitPointer = 0;
    debug_printf("ir_uart_encode(): 0x%02x: ", tx_byte);
    
    // Send the lead-in period
    //
    // This is 60 if bit 0 is a 0 or 35 if bit 0 is a 1
    if (ir_uart_isBitSet(tx_byte, bitPointer)) {
        ir_uart_pulse(35);
    } else {
        ir_uart_pulse(60);
        encoded_word = ir_uart_setbit(encoded_word, 0);
    }
    
    // Send the data bit periods
    for (bitPointer = 0; bitPointer < 7; bitPointer++)
    {
        // If the current bit is 0 and the next bit is 0 output 75 uS period
        if (ir_uart_isBitSet(tx_byte, bitPointer) == 0 && ir_uart_isBitSet(tx_byte, bitPointer+1) == 0) {
            ir_uart_pulse(75);
            encoded_word = ir_uart_setbit(encoded_word, (bitPointer*2) + 2);
        }
            
        // If the current bit is 0 and the next bit is 1 output 50 uS period
        if (ir_uart_isBitSet(tx_byte, bitPointer) == 0 && ir_uart_isBitSet(tx_byte, bitPointer+1) == 1) {
            ir_uart_pulse(50);
            // Encoded result is 00 - do nothing
        }
            
        // If the current bit is 1 and the next bit is 0 output 100 uS period
        if (ir_uart_isBitSet(tx_byte, bitPointer) == 1 && ir_uart_isBitSet(tx_byte, bitPointer+1) == 0) {
            ir_uart_pulse(100);
            encoded_word = ir_uart_setbit(encoded_word, (bitPointer*2) + 3);
        }
            
        // If the current bit is 1 and the next bit is 1 output 75 uS period
        if (ir_uart_isBitSet(tx_byte, bitPointer) == 1 && ir_uart_isBitSet(tx_byte, bitPointer+1) == 1) {
            ir_uart_pulse(75);
            encoded_word = ir_uart_setbit(encoded_word, (bitPointer*2) + 2);
        }
    }
    
    //Send the lead-out periods:
    if (ir_uart_parity(tx_byte) == 1) {
        // If the parity is even the lead-out periods are 50, 75 and 75
        ir_uart_pulse(50);
        ir_uart_pulse(75);
        encoded_word = ir_uart_setbit(encoded_word, 18);
        ir_uart_pulse(75);
        encoded_word = ir_uart_setbit(encoded_word, 18+2);
    } else {
        // If the parity is odd the lead-out periods are 50, 75 and 100
        ir_uart_pulse(50);
        ir_uart_pulse(75);
        encoded_word = ir_uart_setbit(encoded_word, 18);
        ir_uart_pulse(100);
        encoded_word = ir_uart_setbit(encoded_word, 18+2+1);
    }
    
    // End of frame
    debug_printf("= %d\n", encoded_word);
    return encoded_word;
}