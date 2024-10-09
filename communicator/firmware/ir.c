/************************************************************************ 

    ir.c

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

#include "debug.h"
#include "ir.h"

void ir_initialise(void)
{
    // Not doing anything yet
}

void ir_pulse(int32_t delay_time_us)
{
    // Send 2.5 uS pulse
    // Followed by delay_time_us pause
    debug_printf("%d,", delay_time_us);
}

// Function to test if a bit is set to 1 in a byte
bool ir_isBitSet(uint8_t value, uint8_t bitIndex)
{
	return (value & (1 << bitIndex)) != 0;
}

// Function to calculate the parity of a byte
// Returns 0 if parity is odd and 1 if parity is even
uint8_t ir_parity(uint8_t x)
{
   uint8_t y;
   
   y = x ^ (x >> 1);
   y = y ^ (y >> 2);
   y = y ^ (y >> 4);
   y = y ^ (y >> 8);
   y = y ^ (y >> 16);

   return y & 1;
}

// Send a byte via IR
// The Tx byte should be between 0 and 127 (7 bits)
void ir_send_byte(uint8_t tx_byte)
{
	// Note: The data is sent LSB first, so transmission is from
	// bit 0 to bit 6 (7-bit data).  Bit 7 should always be 0

    // Start of frame
    uint8_t bitPointer = 0;
    debug_printf("IR send byte 0x%02x: ", tx_byte);
    
    // Send the lead-in period
    //
    // This is 60 if bit 0 is a 0 or 35 if bit 0 is a 1
    if (ir_isBitSet(tx_byte, bitPointer)) ir_pulse(35);
    else ir_pulse(60);
    
    // Send the data bit periods
    for (bitPointer = 0; bitPointer < 7; bitPointer++)
    {
        // If the current bit is 0 and the next bit is 0 output 75 uS period
        if (ir_isBitSet(tx_byte, bitPointer) == 0 && ir_isBitSet(tx_byte, bitPointer+1) == 0)
            ir_pulse(75);
            
        // If the current bit is 0 and the next bit is 1 output 50 uS period
        if (ir_isBitSet(tx_byte, bitPointer) == 0 && ir_isBitSet(tx_byte, bitPointer+1) == 1)
            ir_pulse(50);
            
        // If the current bit is 1 and the next bit is 0 output 100 uS period
        if (ir_isBitSet(tx_byte, bitPointer) == 1 && ir_isBitSet(tx_byte, bitPointer+1) == 0)
            ir_pulse(100);
            
        // If the current bit is 1 and the next bit is 1 output 75 uS period
        if (ir_isBitSet(tx_byte, bitPointer) == 1 && ir_isBitSet(tx_byte, bitPointer+1) == 1)
            ir_pulse(75);
    }
    
    // Send the lead-out periods:
    if (ir_parity(tx_byte) == 1) {
        // If the parity is even the lead-out periods are 50, 75 and 75
        ir_pulse(50);
        ir_pulse(75);
        ir_pulse(75);
    } else {
        // If the parity is odd the lead-out periods are 50, 75 and 100
        ir_pulse(50);
        ir_pulse(75);
        ir_pulse(100);
    }
    
    // End of frame
    debug_printf("\n");
}