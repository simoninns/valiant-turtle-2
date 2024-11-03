#************************************************************************ 
#
#   parallel_port.py
#
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

from log import log_debug, log_info, log_warn

from machine import I2C, Pin
from mcp23017 import Mcp23017
from byte_fifo import Byte_fifo

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

class Parallel_port:
    def __init__(self, i2c: I2C, interrupt_pin):
        self.mcp = Mcp23017(i2c, 0x20)

        # Define an Rx FIFO for storing incoming data
        self.rx_fifo = Byte_fifo(1024)

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

        log_info("Parallel::__init__ - Parallel port initialised")

    # MCP23017 INTB pin callback
    def __callback(self, p):
        # Get the databus value
        rx_data = self.mcp.mgpio_get_all() >> 8
        self.rx_fifo.write(rx_data)
        
        # ACK a received byte (M6522 VIA Handshake output mode, pull CB1 low)
        self.mcp.mgpio_put(_PARALLEL_BUSY, False)
        self.mcp.mgpio_put(_PARALLEL_BUSY, True)

    # Get a byte from the FIFO
    def read(self):
        return self.rx_fifo.read()
    
    # Returns False if fifo is empty
    def any(self) -> bool:
        return self.rx_fifo.any()