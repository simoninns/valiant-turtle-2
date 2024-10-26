#************************************************************************ 
#
#   eeprom.py
#
#   24LC16 I2C EEPROM Communication
#   Valiant Turtle 2 - Raspberry Pi Pico W Firmware
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

from machine import I2C
import sys
from time import sleep

class Eeprom:
    def __init__(self, i2c_bus: I2C, i2c_address: int = 0x50):
        self.i2c = i2c_bus
        self.i2c_address = i2c_address

    def read(self, address: int, number_of_bytes: int) -> bytes:
        # Ensure the address is not out of bounds
        if ((address + number_of_bytes) > (256*8)):
            raise RuntimeError("Eeprom::read - Requested address is out of bounds!")

        # Determine the device address (including the block) and intra-block address
        self._devaddr = bytearray(1)
        self._blockaddr = bytearray(1)
        self._devaddr[0] = self.i2c_address | (address >> 8) # Device address
        self._blockaddr[0] = (address & 0xFF); # Block address

        sleep(0.01)
        self.i2c.writeto(self._devaddr[0], self._blockaddr, False)
        buffer = self.i2c.readfrom(self._devaddr[0], number_of_bytes, True)

        return buffer

    def write(self, address: int, buffer: bytearray):
         # Ensure the address is not out of bounds
        if ((address + len(buffer)) > (256*8)):
            raise RuntimeError("Eeprom::write - Requested address is out of bounds!")
    
        remaining_data = len(buffer)
        data_pointer = 0

        while remaining_data > 0:
            # Determine the device address (including the block) and intra-block address
            self._addr = bytearray(2)
            self._addr[0] = self.i2c_address | (address >> 8) # Device address
            self._addr[1] = (address & 0xFF) # Block address

            # Initialise an array to store the start address and a page of data
            # If we have less that 16 bytes of remaining data, lower the write length
            if (remaining_data < 16): 
                write_length = remaining_data
                self._page = bytearray(write_length+1)
            else:
                self._page = bytearray(16+1)
                self.write_length = 16

            # If we would cross a block boundary, lower the write length to avoid
            if ((self._addr[1]+write_length) > 255): write_length -= (self._addr[1]+write_length) - 256

            # Copy the start address and the data into the page
            self._page[0] = self._addr[1];
            for i in range(0, write_length):
                self._page[i+1] = buffer[data_pointer]
                data_pointer += 1

            # Perform a page write
            sleep(0.01)
            self.i2c.writeto(self._addr[0], self._page, True)

            # Continue if required
            remaining_data -= write_length