#************************************************************************ 
#
#   ir_uart.py
#
#   Original Valiant IR protocol communication class
#   Valiant Turtle 2 - Communicator firmware
#   Copyright (C) 2024 Simon Inns
#
#   This file is part of Valiant Turtle 2
#
#   This is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Email: simon.inns@gmail.com
#
#************************************************************************

import logging

from machine import Pin
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def ir_uart():
    """
    PIO assembly program for IR UART communication.

    This function defines a PIO (Programmable Input/Output) assembly program
    for handling IR (Infrared) UART (Universal Asynchronous Receiver-Transmitter)
    communication. The program is designed to be run on the RP2040's PIO state machine.

    The program performs the following steps:
    1. Pulls data from the output shift register (OSR) into the state machine.
    2. Sets up a bit loop to handle 8 data bits and 3 parity bits.
    3. Outputs a lead-in signal.
    4. Outputs each bit of the data, with appropriate timing.

    The timing and logic are designed to match the requirements of the Valiant IR protocol.
    """
    pull(block)
    set(x, 10)                # Get ready for the bit loop (8 bits + 3 parity)

    label("leadin")
    set(pins, 1)          [ 4] # Output pin high for 5 clocks
    set(pins, 0)             
    out(y, 2)             [31] # Shift 2 bits from OSR into Y wait 31
    jmp(not_y, "bitloop")      # IF Y == 0 THEN jump to bitloop (35uS leadin)
    nop()                 [24] # wait another 24 cycles (60 uS leadin)

    label("bitloop")
    out(y, 2)                  # Shift in 2 bits from the OSR into y
    set(pins, 1)          [ 4] # Output pin high for 5 clocks
    set(pins, 0)
    nop()                 [23]
    nop()                 [20] # 50 uS (50)
    jmp(y_dec, "delay1")
    jmp("bitdone")

    label("delay1")
    nop()                  [23] # 25 uS (75)
    jmp(y_dec, "delay2")
    jmp("bitdone")

    label("delay2")
    nop()                  [25] # 25 us (100)

    label("bitdone")
    jmp(x_dec, "bitloop")


class IrUart:
    _sm_counter = 0

    def __init__(self, pin):
        # Note: This SM counter is a little rough... it assumes that only this class will
        # consume SMs...
        if IrUart._sm_counter < 4:
            logging.info(f"IrUart::__init__ - Initialised using state-machine {IrUart._sm_counter}")
        else:
            raise RuntimeError("Pulse_generator::__init__ - No more state machines available!")
        
        # Clock divider is /125 so 125,000,000 / 125 = 1,000,000
        self._sm = rp2.StateMachine(IrUart._sm_counter, ir_uart, freq=1000000, set_base=Pin(pin))
        IrUart._sm_counter += 1

        # Activate the state machine
        self._sm.active(1)

    # Output characters via the IR
    def ir_print(self, ch: bytes):
        for c in range(0, len(ch)):
            self._sm.put(self.__encode(ch[c]))

    # Output a single character via the IR
    def ir_putc(self, ch):
        self._sm.put(self.__encode(ch))

    # Calculate the parity bit for x
    # Returns 0 = EVEN or 1 = ODD
    def __parity(self, x):
        y = 0

        y = x ^ (x >> 1)
        y = y ^ (y >> 2)
        y = y ^ (y >> 4)
        y = y ^ (y >> 8)
        y = y ^ (y >> 16)

        return y & 1
    
    # Set a bit at a bit position
    def __set_bit(self, value, bit_position):
        return value | (1 << bit_position)

    # Check if a bit is set at a bit position
    def __is_bit_set(self, value, bit_position) -> bool:
        return ((value >> bit_position & 1) != 0)
    
    # In order to keep the PIO code as simple as possible we first encode
    # the required byte into a sequence of 2 bit results:
    # 2 bits represent the lead-in (0b00 = 35uS or 0b01 = 60uS)
    # 16 bits represent the value's 8 bits (0b00 = 50uS, 0b01 = 75uS or 0b10 = 100uS)
    # 6 bits represent the 3 parity pulses (0b00 = 50uS, 0b01 = 75uS or 0b10 = 100uS)
    def __encode(self, tx_byte):
        encoded_word = 0
        # Note: The data is sent LSB first, so transmission is from
        # bit 0 to bit 6 (7-bit data).  Bit 7 should always be 0

        # Start of frame
        bitPointer = 0
        
        # Send the lead-in period
        #
        # This is 60 if bit 0 is a 0 or 35 if bit 0 is a 1
        if not self.__is_bit_set(tx_byte, bitPointer):
            encoded_word = self.__set_bit(encoded_word, 0)
        
        # Send the data bit periods
        for bitPointer in range(7):
            # If the current bit is 0 and the next bit is 0 output 75 uS period
            if not self.__is_bit_set(tx_byte, bitPointer) and not self.__is_bit_set(tx_byte, bitPointer+1):
                encoded_word = self.__set_bit(encoded_word, (bitPointer*2) + 2)
                
            # # If the current bit is 0 and the next bit is 1 output 50 uS period
            # if not self.__is_bit_set(tx_byte, bitPointer) and self.__is_bit_set(tx_byte, bitPointer+1):
            #     # Encoded result is 00 - do nothing
                
            # If the current bit is 1 and the next bit is 0 output 100 uS period
            if self.__is_bit_set(tx_byte, bitPointer) and not self.__is_bit_set(tx_byte, bitPointer+1):
                encoded_word = self.__set_bit(encoded_word, (bitPointer*2) + 3)
                
            # If the current bit is 1 and the next bit is 1 output 75 uS period
            if self.__is_bit_set(tx_byte, bitPointer) and self.__is_bit_set(tx_byte, bitPointer+1):
                encoded_word = self.__set_bit(encoded_word, (bitPointer*2) + 2)
        
        # Send the lead-out periods:
        if self.__parity(tx_byte) == 0:
            # If the parity is even the lead-out periods are 50, 75 and 100
            # Encoded result is 00 - do nothing for 50
            encoded_word = self.__set_bit(encoded_word, 18) # 75
            encoded_word = self.__set_bit(encoded_word, 18+2+1) # 100
        else:
            # If the parity is odd the lead-out periods are 50, 75 and 75
            # Encoded result is 00 - do nothing for 50
            encoded_word = self.__set_bit(encoded_word, 18) # 75
            encoded_word = self.__set_bit(encoded_word, 18+2) # 75
        
        # End of frame
        return encoded_word

if __name__ == "__main__":
    from main import main
    main()