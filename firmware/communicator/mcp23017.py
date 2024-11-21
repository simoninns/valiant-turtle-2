#************************************************************************ 
#
#   mcp23017.py
#
#   MCP23017 I2C I/O Expander communication class
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

from machine import I2C, Pin

# MCP23017 Registers
_MCP23017_IODIRA     = const(0x00) # Direction of data I/O port A (bits set as: 1 = input, 0 = output)
_MCP23017_IODIRB     = const(0x01) # Direction of data I/O port B (bits set as: 1 = input, 0 = output)
_MCP23017_IPOLA      = const(0x02) # Input polarity register A
_MCP23017_IPOLB      = const(0x03) # Input polarity register B
_MCP23017_GPINTENA   = const(0x04) # Interrupt on change A
_MCP23017_GPINTENB   = const(0x05) # Interrupt on change B
_MCP23017_DEFVALA    = const(0x06) # Default value register A
_MCP23017_DEFVALB    = const(0x07) # Default value register B
_MCP23017_INTCONA    = const(0x08) # Interrupt on change control register A
_MCP23017_INTCONB    = const(0x09) # Interrupt on change control register B
_MCP23017_IOCONA     = const(0x0A) # IO Control register A
_MCP23017_IOCONB     = const(0x0B) # IO Control register B
_MCP23017_GPPUA      = const(0x0C) # Pull-up set internal pull up for input pins on A
_MCP23017_GPPUB      = const(0x0D) # Pull-up set internal pull up for input pins on B
_MCP23017_INTFA      = const(0x0E) # Interrupt Flag A
_MCP23017_INTFB      = const(0x0F) # Interrupt Flag B
_MCP23017_INTCAPA    = const(0x10) # Interrupt Capture A
_MCP23017_INTCAPB    = const(0x11) # Interrupt Capture B
_MCP23017_GPIOA      = const(0x12) # Port Register A - write modifies latch
_MCP23017_GPIOB      = const(0x13) # Port Register B - write modifies latch

# I/O configuration (IOCONA/IOCONB) register bits (bit 0 is unused)
_MCP23017_IOCON_BANK_BIT     = const(7)
_MCP23017_IOCON_MIRROR_BIT   = const(6)
_MCP23017_IOCON_SEQOP_BIT    = const(5)
_MCP23017_IOCON_DISSLW_BIT   = const(4)
_MCP23017_IOCON_HAEN_BIT     = const(3)
_MCP23017_IOCON_ODR_BIT      = const(2)
_MCP23017_IOCON_INTPOL_BIT   = const(1)

class Mcp23017:
    """
    A class to represent and control the MCP23017 I2C I/O Expander.

    Attributes
    ----------
    i2c : I2C
        The I2C bus instance.
    address : int
        The I2C address of the MCP23017.
    _is_present : bool
        Flag indicating if the MCP23017 is present.
    iodir_ab : int
        Direction of data I/O ports A and B.
    gppub_ab : int
        Pull-up configuration for ports A and B.
    gpio_input_ab : int
        Input state of GPIO ports A and B.
    gpio_output_ab : int
        Output state of GPIO ports A and B.
    ipol_ab : int
        Input polarity configuration for ports A and B.
    gpinten_ab : int
        Interrupt on change configuration for ports A and B.
    defval_ab : int
        Default value configuration for ports A and B.
    intcon_ab : int
        Interrupt control configuration for ports A and B.

    Methods
    -------
    __init__(i2c: I2C, address):
        Initializes the MCP23017 with the given I2C bus and address.
    configuration(mirror, seqop):
        Configures the IO Control register.
    """
    
    def __init__(self, i2c: I2C, address):
        self.i2c = i2c
        self.address = address
        self._is_present = False

        # Default our local register representations
        self.iodir_ab = 0
        self.gppub_ab = 0
        self.gpio_input_ab = 0
        self.gpio_output_ab = 0
        self.ipol_ab = 0

        self.gpinten_ab = 0
        self.defval_ab = 0
        self.intcon_ab = 0

        # Check that MCP23017 is present
        devices = i2c.scan()
        for idx in range(len(devices)):
            if devices[idx] == self.address: self._is_present = True

        if self._is_present:
            logging.info(f"Mcp23017::__init__ - MCP23017 detected at address {hex(self.address)}")
        else:
            logging.info("Mcp23017::__init__ - MCP23017 is not present... Cannot initialise!")
            return

        # Configure IO Control
        self.configuration(True, False)

        # Set all pins to output, turn off, turn off all pulls, input polarity same
        self.__write_dual_registers(_MCP23017_IODIRA, self.iodir_ab) # Also writes IODIRB
        self.__write_dual_registers(_MCP23017_GPPUA, self.gppub_ab) # Also writes GPPUB
        self.__write_dual_registers(_MCP23017_GPIOA, self.gpio_output_ab) # Also writes GPIOB
        self.__write_dual_registers(_MCP23017_IPOLA, self.ipol_ab) # Also writes IPOLB
        
        # Default interrupts to 0 default, previous value compare, disabled 
        self.__write_dual_registers(_MCP23017_DEFVALA, self.defval_ab) # Also writes DEFVALB
        self.__write_dual_registers(_MCP23017_INTCONA, self.intcon_ab) # Also writes INTCONB
        self.__write_dual_registers(_MCP23017_GPINTENA, self.gpinten_ab) # Also writes GPINTENB

        logging.info("Mcp23017::__init__ - MCP23017 initialised")

    # Return True is MCP23017 was detected and initialised
    @property
    def is_present(self):
        return self._is_present

    # Set the mirroring and polarity configuration flags
    #
    # Note: If mirroring is true any GPIO interrupt will set both INTA and INTB
    # otherwise INTA is set for an interrupt on GPIOA and INTB for GPIOB
    def configuration(self, int_mirroring: bool, int_polarity: bool):
        io_control_flags = 0x00 # Unused
        io_control_flags = self.__set_bit(io_control_flags, _MCP23017_IOCON_BANK_BIT, False)
        io_control_flags = self.__set_bit(io_control_flags, _MCP23017_IOCON_MIRROR_BIT, int_mirroring) # True = INT pins are internally connected
        io_control_flags = self.__set_bit(io_control_flags, _MCP23017_IOCON_SEQOP_BIT, False)
        io_control_flags = self.__set_bit(io_control_flags, _MCP23017_IOCON_DISSLW_BIT, False)
        io_control_flags = self.__set_bit(io_control_flags, _MCP23017_IOCON_HAEN_BIT, False)
        io_control_flags = self.__set_bit(io_control_flags, _MCP23017_IOCON_ODR_BIT, False)
        io_control_flags = self.__set_bit(io_control_flags, _MCP23017_IOCON_INTPOL_BIT, int_polarity) # True = INT Active high, False = INT Active low

        io_control_flags = (io_control_flags << 8) + io_control_flags # Copy A to B
        self.__write_dual_registers(_MCP23017_IOCONA, io_control_flags) # Also writes IOCONB
        logging.debug(f"Mcp23017::configuration - IOCON = {io_control_flags:08b}")

    # Public method to enable and disable interrupts
    def interrupt_enable(self, gpio, is_set: bool):
        if gpio > 15: gpio = 15
        self.gpinten_ab = self.__set_bit(self.gpinten_ab, gpio, is_set)
        self.__write_dual_registers(_MCP23017_GPINTENA, self.gpinten_ab) # Also writes GPINTENB
        logging.debug(f"Mcp23017::interrupt_enable - GPINTEN = {self.gpinten_ab:016b}")

    # Public method to set default gpio value (false = 0, true = 1) for interrupt comparison
    def interrupt_set_default_value(self, gpio, default_value: bool):
        if gpio > 15: gpio = 15
        self.defval_ab = self.__set_bit(self.defval_ab, gpio, default_value)
        self.__write_dual_registers(_MCP23017_DEFVALA, self.defval_ab) # Also writes DEFVALB
        logging.debug(f"Mcp23017::interrupt_set_default_value - DEFVAL = {self.defval_ab:016b}")

    # Public method to configure the interrupt type (false = compare to previous state, true = compare to default value in DEFVAL)
    def interrupt_set_type(self, gpio, is_default_compared: bool):
        if gpio > 15: gpio = 15
        self.intcon_ab = self.__set_bit(self.intcon_ab, gpio, is_default_compared)
        self.__write_dual_registers(_MCP23017_INTCONA, self.intcon_ab) # Also writes INTCONB
        logging.debug(f"Mcp23017::interrupt_set_type - INTCON = {self.intcon_ab:016b}")
    
    # Method to get the pin values at the time the last interrupt occurred. Note: this has to be
    # read all at once as the read clears the values
    #
    # From the data-sheet:
    # The INTCAP register captures the GPIO port value at the time the interrupt occurred. The register is
    # read-only and is updated only when an interrupt occurs. The register remains unchanged until the
    # interrupt is cleared via a read of INTCAP or GPIO
    #
    # Note: Reading this register also clears the INTA or INTB pin of the MCP23017
    def interrupt_get_values(self):
        return self.__read_dual_registers(_MCP23017_INTCAPA) # Also reads INTCAPB
    
    # Method to get the last gpio that caused an interrupt
    #
    # From the data-sheet:
    # The INTF register reflects the interrupt condition on the port pins of any pin that is enabled for interrupts via the
    # GPINTEN register. A set bit indicates that the associated pin caused the interrupt.
    # This register is read-only. Writes to this register will be ignored
    def interrupt_get_last_gpio(self):
        int_flag = self.__read_dual_registers(_MCP23017_INTFA) # Also reads INTFB

        # Scan for an interrupt and return the GPIO (pin) number
        for pin in range(15):
            if self.__is_bit_set(int_flag, pin):
                return pin
        return -1

    # Public GPIO methods
    def mgpio_set_dir(self, gpio, is_input: bool):
        if gpio > 15: gpio = 15
        self.iodir_ab = self.__set_bit(self.iodir_ab, gpio, is_input)
        self.__write_dual_registers(_MCP23017_IODIRA, self.iodir_ab) # Also writes IODIRB
        logging.debug(f"Mcp23017::mgpio_set_dir - IODIR = {self.iodir_ab:016b}")

    def mgpio_pull_up(self, gpio, is_on: bool):
        if gpio > 15: gpio = 15
        self.gppub_ab = self.__set_bit(self.gppub_ab, gpio, is_on)
        self.__write_dual_registers(_MCP23017_GPPUA, self.gppub_ab) # Also writes GPPUB
        logging.debug(f"Mcp23017::mgpio_pull_up - GPPU = {self.gppub_ab:016b}")

    def mgpio_get(self, gpio):
        if gpio > 15: gpio = 15
        self.gpio_input_ab = self.__read_dual_registers(_MCP23017_GPIOA) # Also reads GPIOB
        return self.__is_bit_set(self.gpio_input_ab, gpio)

    def mgpio_put(self, gpio, value: bool):
        if gpio > 15: gpio = 15
        self.gpio_output_ab = self.__set_bit(self.gpio_output_ab, gpio, value)
        self.__write_dual_registers(_MCP23017_GPIOA, self.gpio_output_ab) # Also writes GPIOB

    def mgpio_put_all(self, value):
        self.gpio_output_ab = value
        self.__write_dual_registers(_MCP23017_GPIOA, self.gpio_output_ab) # Also writes GPIOB

    def mgpio_get_all(self):
        self.gpio_input_ab = self.__read_dual_registers(_MCP23017_GPIOA) # Also reads GPIOB
        return self.gpio_input_ab

    # Private methods
    # Write both A and B registers
    def __write_dual_registers(self, reg, value: int):
        if (value > 65535):
            RuntimeError("mcp23017::__write_dual_registers - Value is more than 16-bits!")

        # Ensure we are always writing 2 bytes
        if (value > 255):
            bvalue = value.to_bytes(2, "little")
        elif (value < 255 and value > 0):
            bvalue = bytes([value,0])
        else:
            bvalue = bytes([0,0])

        self.i2c.writeto_mem(self.address, reg, bvalue)

    # Read both A and B registers
    def __read_dual_registers(self, reg) -> int:
        return int.from_bytes(self.i2c.readfrom_mem(self.address, reg, 2), "little")

    # Set a bit at a bit position
    def __set_bit(self, value, bit_position, set: bool):
        if bit_position >= 0 and bit_position <= 15:
            if set:
                value |= (1 << bit_position)
            else:
                value &= ~(1 << bit_position)
        return value

    # Check if a bit is set at a bit position
    def __is_bit_set(self, value, bit_position) -> bool:
        if bit_position < 8:
            if (value[0] & (1 << bit_position)):
                return True
        else:
            bit_position -= 8
            if (value[1] & (1 << bit_position)):
                return True

        return False
    
if __name__ == "__main__":
    from main import main
    main()