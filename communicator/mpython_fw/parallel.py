#************************************************************************ 
#
#   ir_uart.py
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

from log import log_debug
from log import log_info
from log import log_warn

from machine import I2C, Pin
import mcp23017

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

class Parallel:
    def __init__(self, i2c: I2C, interrupt_pin):
        self.i2c = i2c
        self.mcp = mcp23017.MCP23017(i2c, 0x20)
        self.mcp.config(interrupt_polarity=0, interrupt_mirror=1)

        # Set up MCP23017 GPIO Pins
        self.mcp.pin(_PARALLEL_UN0, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_UN1, mode=1, pullup=True)

        self.mcp.pin(_PARALLEL_NACK, mode=0, value=0)
        self.mcp.pin(_PARALLEL_NACK, mode=0, value=1)

        self.mcp.pin(_PARALLEL_NDATASTROBE, pullup=True,
            interrupt_enable=1, interrupt_compare_default=1, default_value=1)

        self.mcp.pin(_PARALLEL_5, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_6, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_7, mode=1, pullup=True)

        self.mcp.pin(_PARALLEL_DAT0, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_DAT1, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_DAT2, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_DAT3, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_DAT4, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_DAT5, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_DAT6, mode=1, pullup=True)
        self.mcp.pin(_PARALLEL_DAT7, mode=1, pullup=True)

        # Configure the interrupt detect GPIO on the RP2040
        self.int_pin = Pin(interrupt_pin, Pin.IN, Pin.PULL_UP)
        self.int_pin.irq(handler=self._callback, trigger=self.int_pin.IRQ_FALLING)
        self.mcp.interrupt_captured

    def get_data(self):
        # Return the upper 8 bits of the 16-bit GPIO inputs
        return (self.mcp.gpio & 0xFF00) >> 8

    def ack(self):
        # Toggle the BUSY line to ACK
        self.mcp.pin(_PARALLEL_BUSY, value=0)
        self.mcp.pin(_PARALLEL_BUSY, value=1)

    def _callback(self, p):
        # Get the received byte
        ch = self.get_data()

        # ACK the byte
        self.ack()

        # Clear the interrupt by reading INTCAP
        self.mcp.interrupt_captured
        
        # Do something with the byte
        print("PP=", ch)