#************************************************************************ 
#
#   eeprom.py
#
#   24LC16 I2C EEPROM Communication
#   Valiant Turtle 2 - Robot firmware
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
from machine import I2C
from time import sleep

class Eeprom:
    """
    A class to represent a 24LC16 I2C EEPROM.

    Attributes
    ----------
    i2c : I2C
        The I2C bus instance.
    i2c_address : int
        The I2C address of the EEPROM.
    _is_present : bool
        Flag indicating if the EEPROM is present.
    _maximum_address : int
        The maximum address value for the 24LC16 EEPROM.

    Methods
    -------
    __init__(i2c_bus: I2C, address: int = 0x50):
        Initializes the EEPROM with the given I2C bus and address.
    """

    def __init__(self, i2c_bus: I2C, address: int = 0x50):
        """
        Constructs all the necessary attributes for the EEPROM object.

        Parameters
        ----------
        i2c_bus : I2C
            The I2C bus instance.
        address : int, optional
            The I2C address of the EEPROM (default is 0x50).
        """
        self.i2c = i2c_bus
        self.i2c_address = address

        # Check that the EEPROM is present
        self._is_present = False

        devices = self.i2c.scan()
        for idx in range(len(devices)):
            if devices[idx] == self.i2c_address: self._is_present = True

        if self._is_present:
            logging.info(f"Eeprom::__init__ - 24LC16 EEPROM detected at address {hex(self.i2c_address)}")
        else:
            logging.info("Eeprom::__init__ - 24LC16 EEPROM is not present... Cannot initialise!")

        self._maximum_address = 2048 # Maximum address value for the 24LC16
        self._page_size = 16 # The page size for the 24LC16

    # Return True is 24LC16 EEPROM was detected and initialised
    @property
    def is_present(self):
        return self._is_present
    
    def read(self, address, number_of_bytes) -> bytes:
        # Ensure the whole read is within the memory's boundaries
        if address + number_of_bytes > self._maximum_address:
            raise ValueError("Eeprom::read - Requested address exceeds the maximum allowed")
        if address < 0:
            raise ValueError("Eeprom::read - Requested address is less than zero")
        
        # Determine the device address (including the block) and intra-block address
        self._devaddr = bytearray(1)
        self._blockaddr = bytearray(1)
        self._devaddr[0] = self.i2c_address | (address >> 8) # Device address
        self._blockaddr[0] = (address & 0xFF); # Block address

        # Read from the EEPROM and return the collected data
        logging.debug(f"Eeprom::read - Address = {address} - number of bytes = {number_of_bytes}")

        sleep(0.01)
        self.i2c.writeto(self._devaddr[0], self._blockaddr, False)
        return self.i2c.readfrom(self._devaddr[0], number_of_bytes, True)
    
    def write(self, address, data: bytes):
        # Ensure the whole write is within the memory's boundaries
        if address + len(data) > self._maximum_address:
            raise ValueError("Eeprom::write - Requested address exceeds the maximum allowed")
        if address < 0:
            raise ValueError("Eeprom::write - Requested address is less than zero")
        
        remaining_data = len(data) # Keep track of what's left to write
        data_pointer = 0
        logging.debug(f"Eeprom::write - Writing address = {address} - write length = {remaining_data}")

        while remaining_data > 0:
            # Determine the device address (including the block) and intra-block address
            self._addr = bytearray(2)
            self._addr[0] = self.i2c_address | (address >> 8) # Device address
            self._addr[1] = (address & 0xFF) # Block address

            # Maximum write length is the page size
            write_length = self._page_size
            if (remaining_data < self._page_size): 
                write_length = remaining_data

            # If the required read would cross and block boundary, lower the 
            # write length to prevent this happening
            bytes_until_boundary = self._page_size - address % self._page_size
            if (write_length > bytes_until_boundary): write_length = bytes_until_boundary

            # Copy the start address and the data into the page buffer
            page_buffer = bytearray(write_length+1)
            page_buffer[0] = self._addr[1]
            for i in range(0, write_length):
                page_buffer[i+1] = data[data_pointer]
                data_pointer += 1

            logging.debug(f"Eeprom::write - Page write @ address = {address} - write length = {write_length}")

            # Perform a write
            sleep(0.01)
            self.i2c.writeto(self._addr[0], page_buffer, True)

            # Continue if required
            remaining_data -= write_length
            address += write_length

if __name__ == "__main__":
    from main import main
    main()