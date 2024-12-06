#************************************************************************ 
#
#   main.py
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

import library.logging as logging
from micropython import const
from machine import Pin, UART, I2C

from leds import Leds
from ir_uart import IrUart
from parallel_port import ParallelPort

from vt1_mode import Vt1Mode
from vt2_mode import Vt2Mode

# GPIO Hardware mapping
_GPIO_GREEN_LED = const(16)
_GPIO_BLUE_LED = const(18)
_GPIO_IR_LED = const(22)

_GPIO_SDA0 = const(8)
_GPIO_SCL0 = const(9)
_GPIO_SDA1 = const(10)
_GPIO_SCL1 = const(11)

_GPIO_INT0 = const(12)

_GPIO_UART0_TX = const(0)
_GPIO_UART0_RX = const(1)
_GPIO_UART1_TX = const(4)
_GPIO_UART1_RX = const(5)
_GPIO_UART1_RTS = const(7)
_GPIO_UART1_CTS = const(6)

_GPIO_BUTTON0 = const(21)
_GPIO_BUTTON1 = const(20)
_GPIO_BUTTON2 = const(19)

def main():
    """
    Main entry point for the Valiant Turtle 2 Communicator firmware.
    """
    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    i2c0 = I2C(0, scl=Pin(_GPIO_SCL0), sda=Pin(_GPIO_SDA0), freq=400000) # Internal I2C bus
    parallel_port = ParallelPort(i2c0, _GPIO_INT0)

    # Ensure IR LED driver is off
    ir_led = Pin(_GPIO_IR_LED, Pin.OUT)
    ir_led.value(0)

    # Initialise LEDs
    leds = Leds([_GPIO_GREEN_LED, _GPIO_BLUE_LED])

    # True = VT1 IR mode, False = VT2 bluetooth mode
    run_as_legacy = False

    # Which mode are we running in?
    if run_as_legacy:
        # Run in VT1 mode
        uart = UART(1, baudrate=4800, tx=Pin(_GPIO_UART1_TX), rx=Pin(_GPIO_UART1_RX),
            txbuf=1024, rxbuf=1024, bits=8, parity=None, stop=1)
        ir_uart = IrUart(_GPIO_IR_LED)

        vt1_mode = Vt1Mode(uart, parallel_port, ir_uart, leds)
        while True:
            vt1_mode.process()
    else:
        # Run in VT2 mode
        uart = UART(1, baudrate=4800, tx=Pin(_GPIO_UART1_TX), rx=Pin(_GPIO_UART1_RX),
            #cts=Pin(_GPIO_UART1_CTS), rts=Pin(_GPIO_UART1_RTS), flow=(UART.RTS | UART.CTS),
            txbuf=1024, rxbuf=1024, bits=8, parity=None, stop=1)
        vt2_mode = Vt2Mode(uart, parallel_port, leds)
        while True:
            vt2_mode.process()

if __name__ == "__main__":
    main()