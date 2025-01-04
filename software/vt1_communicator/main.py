#************************************************************************ 
#
#   main.py
#
#   Valiant Turtle 1 - Commander Emulator
#   Copyright (C) 2025 Simon Inns
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

import picolog
from micropython import const
from machine import Pin, UART, I2C

from leds import Leds
from ir_uart import IrUart
from parallel_port import ParallelPort

from options import Options

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

_GPIO_OPTION0 = const(26)
_GPIO_OPTION1 = const(27)
_GPIO_OPTION2 = const(28)

def main():
    # Configure the options object
    options = Options(_GPIO_OPTION0, _GPIO_OPTION1, _GPIO_OPTION2)

    # If the option 2 header is closed, output debug information to UART0
    # otherwise output to the REPL
    if options.option2:
        uart0 = UART(0, baudrate=115200, tx=Pin(_GPIO_UART0_TX), rx=Pin(_GPIO_UART0_RX),
            txbuf=1024, rxbuf=1024, bits=8, parity=None, stop=1)
    else:
        uart0 = None

    # Configure the picolog module
    picolog.basicConfig(level=picolog.DEBUG, uart=uart0)

    # Show the options now debug is running
    options.show_options()

    # Configure the parallel port
    i2c0 = I2C(0, scl=Pin(_GPIO_SCL0), sda=Pin(_GPIO_SDA0), freq=400000) # Internal I2C bus
    parallel_port = ParallelPort(i2c0, _GPIO_INT0)

    # Ensure IR LED driver is off
    ir_led = Pin(_GPIO_IR_LED, Pin.OUT)
    ir_led.value(0)

    # Initialise LEDs
    leds = Leds([_GPIO_GREEN_LED, _GPIO_BLUE_LED])

    # Configure the UART1 for serial <-> host communication
    uart1 = UART(1, baudrate=4800, tx=Pin(_GPIO_UART1_TX), rx=Pin(_GPIO_UART1_RX),
            txbuf=1024, rxbuf=1024, bits=8, parity=None, stop=1)
    
    # Configure the IR UART
    ir_uart = IrUart(_GPIO_IR_LED)

    picolog.info("Running VT1 legacy mode for serial and parallel to IR")
    leds.set_brightness(0, 255) # Power LED on
    parallel_port.auto_ack(False) # Turn off auto-ACK
    
    while True:
        # Send any received parallel port data via IR
        while(parallel_port.any()):
            leds.set_brightness(1, 100)
            ch = parallel_port.read(1)[0]
            ir_uart.ir_putc(ch)
            parallel_port.ack()
            leds.set_brightness(1, 0)

        # Send any received serial data via IR
        while(uart1.any()):
            leds.set_brightness(1, 100)
            ch = int(uart1.read(1)[0])
            ir_uart.ir_putc(ch)
            leds.set_brightness(1, 0)

if __name__ == "__main__":
    main()