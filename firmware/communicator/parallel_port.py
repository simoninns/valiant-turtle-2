#************************************************************************ 
#
#   parallel_port.py
#
#   Original Valiant parallel port implementation
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

import library.logging as logging
from machine import I2C, Pin
from micropython import const, RingIO
from mcp23017 import Mcp23017

# Parallel port to MCP23017 GPIO mapping
_PARALLEL_UN0 = const(0)
_PARALLEL_UN1 = const(1)
_PARALLEL_NACK = const(2)
_PARALLEL_BUSY = const(3)
_PARALLEL_NDATASTROBE = const(4)
_PARALLEL_5 = const(5)
_PARALLEL_6 = const(6)
_PARALLEL_7 = const(7)
_PARALLEL_DAT0 = const(8)
_PARALLEL_DAT1 = const(9)
_PARALLEL_DAT2 = const(10)
_PARALLEL_DAT3 = const(11)
_PARALLEL_DAT4 = const(12)
_PARALLEL_DAT5 = const(13)
_PARALLEL_DAT6 = const(14)
_PARALLEL_DAT7 = const(15)

class ParallelPort:
    """
    Class to manage the parallel port interface using the MCP23017 GPIO expander.

    Attributes:
        mcp (Mcp23017): Instance of the MCP23017 GPIO expander.
        _is_present (bool): Indicates if the MCP23017 is present.
        _auto_ack (bool): Indicates if auto acknowledgment is enabled.
        rx_rio (RingIO): Ring buffer for storing incoming data.
    """

    def __init__(self, i2c: I2C, interrupt_pin):
        """
        Initialize the Parallel_port class.

        Args:
            i2c (I2C): The I2C interface to communicate with the MCP23017.
            interrupt_pin (Pin): The pin used for interrupt handling.
        """
        self.mcp = Mcp23017(i2c, 0x20)
        self._is_present = self.mcp.is_present
        self._auto_ack = True

        if self._is_present:
            # Define a Rx ring buffer to store incoming data
            self.rx_rio = RingIO(1024)

            # Set pin directions (True = input, False = output)
            self.mcp.mgpio_set_dir(_PARALLEL_UN0, True)
            self.mcp.mgpio_set_dir(_PARALLEL_UN1, True)
            self.mcp.mgpio_set_dir(_PARALLEL_NACK, False)
            self.mcp.mgpio_set_dir(_PARALLEL_BUSY, False)
            self.mcp.mgpio_set_dir(_PARALLEL_NDATASTROBE, True)
            self.mcp.mgpio_set_dir(_PARALLEL_5, True)
            self.mcp.mgpio_set_dir(_PARALLEL_6, True)
            self.mcp.mgpio_set_dir(_PARALLEL_7, True)
            self.mcp.mgpio_set_dir(_PARALLEL_DAT0, True)
            self.mcp.mgpio_set_dir(_PARALLEL_DAT1, True)
            self.mcp.mgpio_set_dir(_PARALLEL_DAT2, True)
            self.mcp.mgpio_set_dir(_PARALLEL_DAT3, True)
            self.mcp.mgpio_set_dir(_PARALLEL_DAT4, True)
            self.mcp.mgpio_set_dir(_PARALLEL_DAT5, True)
            self.mcp.mgpio_set_dir(_PARALLEL_DAT6, True)
            self.mcp.mgpio_set_dir(_PARALLEL_DAT7, True)

            # Set pull ups on inputs
            self.mcp.mgpio_pull_up(_PARALLEL_UN0, True)
            self.mcp.mgpio_pull_up(_PARALLEL_UN1, True)
            self.mcp.mgpio_pull_up(_PARALLEL_NDATASTROBE, True)
            self.mcp.mgpio_pull_up(_PARALLEL_5, True)
            self.mcp.mgpio_pull_up(_PARALLEL_6, True)
            self.mcp.mgpio_pull_up(_PARALLEL_7, True)
            self.mcp.mgpio_pull_up(_PARALLEL_DAT0, True)
            self.mcp.mgpio_pull_up(_PARALLEL_DAT1, True)
            self.mcp.mgpio_pull_up(_PARALLEL_DAT2, True)
            self.mcp.mgpio_pull_up(_PARALLEL_DAT3, True)
            self.mcp.mgpio_pull_up(_PARALLEL_DAT4, True)
            self.mcp.mgpio_pull_up(_PARALLEL_DAT5, True)
            self.mcp.mgpio_pull_up(_PARALLEL_DAT6, True)
            self.mcp.mgpio_pull_up(_PARALLEL_DAT7, True)

            # Set outputs to default
            self.mcp.mgpio_put(_PARALLEL_NACK, False)
            self.mcp.mgpio_put(_PARALLEL_BUSY, True)

            # Set up interrupt on MCP23017 _PARALLEL_NDATASTROBE signal
            self.mcp.interrupt_set_default_value(_PARALLEL_NDATASTROBE, True) # Set default to high
            self.mcp.interrupt_set_type(_PARALLEL_NDATASTROBE, True) # Interrupt type is 'compare to default'
            self.mcp.interrupt_enable(_PARALLEL_NDATASTROBE, True) # Enable interrupt
            self.mcp.interrupt_get_values() # Read INTCAP to clear any pending IRQs

            # Configure Interrupt detection GPIO on RP2040
            self.interrupt_pin = Pin(interrupt_pin, Pin.IN, Pin.PULL_UP)
            self.interrupt_pin.irq(handler=self.__callback, trigger=self.interrupt_pin.IRQ_FALLING)

            logging.info("ParallelPort::__init__ - Parallel port initialised")
        else:
            logging.info("ParallelPort::__init__ - MCP23017 not detected - Parallel port NOT initialised")

    # MCP23017 INTB pin callback
    def __callback(self, p):
        # Get the databus value
        rx_data = self.mcp.mgpio_get_all() >> 8
        self.rx_rio.write(rx_data.to_bytes(1, 'big'))
        if self._auto_ack: self.ack()
        
    # ACK a received byte (M6522 VIA Handshake output mode, pull CB1 low)
    def ack(self):
        self.mcp.mgpio_put(_PARALLEL_BUSY, False)
        self.mcp.mgpio_put(_PARALLEL_BUSY, True)

    # Turn automatic acknowledgement on or off
    def auto_ack(self, state):
        if state: self._auto_ack = True
        else: self._auto_ack = False

    # Returns an integer counting the number of characters that can be read from the rx ring buffer
    def any(self):
        return self.rx_rio.any()
    
    def read(self, num = 1):
        return self.rx_rio.read(num)

if __name__ == "__main__":
    from main import main
    main()