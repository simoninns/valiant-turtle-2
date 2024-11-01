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

from log import log_debug
from log import log_info
from log import log_warn

from machine import Pin, UART, I2C
from ble_central import demo
from status_led import Status_led
from ir_uart import Ir_uart
from parallel_port import Parallel_port

from time import sleep

# GPIO Hardware mapping
_GPIO_GREEN_LED = const(16)
_GPIO_BLUE_LED = const(18)
_GPIO_IR_LED = const(22)

_GPIO_SDA0 = const(8)
_GPIO_SCL0 = const(9)
_GPIO_SDA1 = const(10)
_GPIO_SCL1 = const(11)

_GPIO_INT0 = const(12)

_GPIO_UART1_TX = const(4)
_GPIO_UART1_RX = const(5)
_GPIO_UART1_RTS = const(7)
_GPIO_UART1_CTS = const(6)

_GPIO_BUTTON0 = const(21)
_GPIO_BUTTON1 = const(20)
_GPIO_BUTTON2 = const(19)

# Make sure the LEDs and IR LEDs are off
green_led = Status_led(_GPIO_GREEN_LED)
blue_led = Status_led(_GPIO_BLUE_LED)
ir_led = Pin(_GPIO_IR_LED, Pin.OUT)

# Green and blue are inverted logic - IR is not
green_led.set(True)
blue_led.set(False)
ir_led.value(0)

# Configure serial UART
uart = UART(1, baudrate=4800, tx=Pin(_GPIO_UART1_TX), rx=Pin(_GPIO_UART1_RX),
    txbuf=1024, rxbuf=1024, bits=8, parity=None, stop=1)

# Configure IR UART
ir_uart = Ir_uart(_GPIO_IR_LED)

# Configure I2C interfaces
i2c0 = I2C(0, scl=Pin(_GPIO_SCL0), sda=Pin(_GPIO_SDA0), freq=100000) # Internal
i2c1 = I2C(1, scl=Pin(_GPIO_SCL1), sda=Pin(_GPIO_SDA1), freq=100000) # External

# Configure parallel port
parallel_port = Parallel_port(i2c0, _GPIO_INT0)

while True:
    print("GPIOs =", '{0:016b}'.format(parallel_port.get_all_gpios()))

    blue_led.set(True)
    sleep(2)
    blue_led.set(False)
    sleep(2)