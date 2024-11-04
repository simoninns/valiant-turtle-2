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

from log import log_debug, log_info, log_warn, log_control

from machine import Pin, UART, I2C
from ble_central import demo
from status_led import Status_led
from ir_uart import Ir_uart
from parallel_port import Parallel_port
from process_timer import Process_timer
from configuration import Configuration
from eeprom import Eeprom

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

_GPIO_UART0_TX = const(0)
_GPIO_UART0_RX = const(1)
_GPIO_UART1_TX = const(4)
_GPIO_UART1_RX = const(5)
_GPIO_UART1_RTS = const(7)
_GPIO_UART1_CTS = const(6)

_GPIO_BUTTON0 = const(21)
_GPIO_BUTTON1 = const(20)
_GPIO_BUTTON2 = const(19)

# Fade the power LED on and off...
ticker = 0
def power_led():
    global ticker
    if ticker == 0: green_led.set_brightness(255)
    if ticker == 75: green_led.set_brightness(10)
    if ticker == 100:
        ticker = 0
    else:
        ticker += 1

# Process serial and parallel data to IR
# using the original Valiant Turtle communication
def legacy_mode():
    # Send any received parallel port data via IR
        while(parallel_port.any()):
            blue_led.set_brightness(255)
            ch = parallel_port.read()
            ir_uart.ir_putc(ch)
            #log_debug("Parallel Rx =", ch)
            blue_led.set_brightness(0)

        # Send any received serial data via IR
        while(uart1.any()):
            blue_led.set_brightness(255)
            ch = int(uart1.read(1)[0]) # Get 1 byte, store as int
            ir_uart.ir_putc(ch)
            #log_debug("Serial Rx =", ch)
            blue_led.set_brightness(0)

# Communicate with Valiant Turtle 2 robots
def vt2_mode():
    sleep(1)

# Configure log output to serial UART0
uart0 = UART(0, baudrate=115200, tx=Pin(_GPIO_UART0_TX), rx=Pin(_GPIO_UART0_RX))
log_control(uart0, True, True, True)

# Configure Valiant communication serial UART1
uart1 = UART(1, baudrate=4800, tx=Pin(_GPIO_UART1_TX), rx=Pin(_GPIO_UART1_RX),
    txbuf=1024, rxbuf=1024, bits=8, parity=None, stop=1)

# Ensure IR LED is off
ir_led = Pin(_GPIO_IR_LED, Pin.OUT)
ir_led.value(0)

# Configure IR UART
ir_uart = Ir_uart(_GPIO_IR_LED)

# Configure I2C interfaces
i2c0 = I2C(0, scl=Pin(_GPIO_SCL0), sda=Pin(_GPIO_SDA0), freq=100000) # Internal
i2c1 = I2C(1, scl=Pin(_GPIO_SCL1), sda=Pin(_GPIO_SDA1), freq=100000) # External

# EEPROM
eeprom = Eeprom(i2c0, 0x50)

# Configuration object
configuration = Configuration()

# Read the configuration from EEPROM
if not configuration.unpack(eeprom.read(0, configuration.pack_size)):
    # Current EEPROM image is invalid, write the default
    eeprom.write(0, configuration.pack())

# Configure Valiant communication parallel port
parallel_port = Parallel_port(i2c0, _GPIO_INT0)

# Initialise status LEDs
green_led = Status_led(_GPIO_GREEN_LED, 255, 20)
blue_led = Status_led(_GPIO_BLUE_LED, 0, 20)

# Set up a process timer
process_timer = Process_timer()

# Use the process timer for all timer based activities:
process_timer.register_callback(green_led.led_process)
process_timer.register_callback(blue_led.led_process)
process_timer.register_callback(power_led)

# Which mode are we in?
if configuration.is_legacy_mode == True:
    log_info("Communicator is running in legacy mode")
    while configuration.is_legacy_mode:
        legacy_mode()
        
else:
    log_info("Communicator is running in Valiant Turtle 2 mode")
    while not configuration.is_legacy_mode:
        vt2_mode()