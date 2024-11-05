#************************************************************************ 
#
#   main.py
#
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

from log import log_debug, log_info, log_warn, log_control

from ws2812b import Ws2812b
from pen import Pen
from ina260 import Ina260
from eeprom import Eeprom
from configuration import Configuration
from velocity import Velocity
from drv8825 import Drv8825
from stepper import Stepper
from metric import Metric
from process_timer import Process_timer
from ble_peripheral import demo

from time import sleep
from machine import I2C
from machine import Pin

# GPIO hardware mapping
_GPIO_LEDS = const(7)
_GPIO_PEN = const(16)

_GPIO_SDA0 = const(8)
_GPIO_SCL0 = const(9)
_GPIO_SDA1 = const(10)
_GPIO_SCL1 = const(11)

_GPIO_LM_STEP = const(2)
_GPIO_RM_STEP = const(3)
_GPIO_LM_DIR = const(4)
_GPIO_RM_DIR = const(5)
_GPIO_ENABLE = const(6)
_GPIO_M0 = const(12)
_GPIO_M1 = const(13)
_GPIO_M2 = const(14)

# WS2812b pixel number mapping
_WS2812B_power = const(0)
_WS2812B_left_motor = const(1)
_WS2812B_right_motor = const(2)
_WS2812B_left_eye = const(3)
_WS2812B_right_eye = const(4)

# Fade the power LED on and off...
ticker = 0
def power_led():
    global ticker
    if ticker == 0: ws2812b.set_pixel(_WS2812B_power, 0, 64, 0)
    if ticker == 75: ws2812b.set_pixel(_WS2812B_power, 0, 0, 0)
    if ticker == 100:
        ticker = 0
    else:
        ticker += 1

# Output power monitoring information periodically
ina260_ticker = 0
def ina260_info():
    global ina260_ticker
    if ina260_ticker == 0:
        log_info("INA260: mA =", ina260.current, "/ mV =" , ina260.bus_voltage, "/ mW =", ina260.power)
    ina260_ticker += 1
    if ina260_ticker == 2000: ina260_ticker = 0

# Turn on logging
log_control(True, True, True)

# Initialise the Ws2812b driver on PIO 0, SM 0
ws2812b = Ws2812b(5, 0, 0, _GPIO_LEDS, 10)
ws2812b.set_fade_speed(_WS2812B_power, 5)

# Initialise the pen control
pen = Pen(_GPIO_PEN)
pen.off()

# Initialise the I2C buses
i2c_internal = I2C(0, scl=Pin(_GPIO_SCL0), sda=Pin(_GPIO_SDA0), freq=400000)
i2c_external = I2C(1, scl=Pin(_GPIO_SCL1), sda=Pin(_GPIO_SDA1), freq=400000)

# Initialise the INA260 power monitoring chip
ina260 = Ina260(i2c_internal, 0x40)

# Initialise the EEPROM
eeprom = Eeprom(i2c_internal, 0x50)

# Read the configuration from EEPROM
configuration = Configuration()
if not configuration.unpack(eeprom.read(0, configuration.pack_size)):
    # Current EEPROM image is invalid, write the default
    eeprom.write(0, configuration.pack())

# Set up a process timer
process_timer = Process_timer()

# Use the process timer for all timer based activities:
process_timer.register_callback(power_led) # For fading on and off the power LED
process_timer.register_callback(ina260_info) # Periodic power usage output to debug
process_timer.register_callback(ws2812b.process_pixels) # WS2812 fading process

# Configure the DRV8825
drv8825 = Drv8825(_GPIO_ENABLE, _GPIO_M0, _GPIO_M1, _GPIO_M2)
drv8825.set_steps_per_revolution(800)
drv8825.set_enable(False)

# Configure the steppers
left_stepper = Stepper(_GPIO_LM_DIR, _GPIO_LM_STEP, True)
left_stepper.set_forwards()
right_stepper = Stepper(_GPIO_RM_DIR, _GPIO_RM_STEP, False)
right_stepper.set_forwards()

# Define a velocity sequence
# velocity = Velocity(6400, 32, 2, 1600, 16)

# while True:
#     drv8825.set_enable(True)
#     ws2812b.set_pixel(_WS2812B_left_motor, 0, 64, 0)
#     ws2812b.set_pixel(_WS2812B_right_motor, 0, 64, 0)
#     left_stepper.set_velocity(velocity)
#     right_stepper.set_velocity(velocity)
#     print("Stepper sequence running")

#     # Wait for the stepper to finish
#     while left_stepper.is_busy or right_stepper.is_busy:
#         sleep(0.01)
#     drv8825.set_enable(False)
#     ws2812b.set_pixel(_WS2812B_left_motor, 64, 0, 0)
#     ws2812b.set_pixel(_WS2812B_right_motor, 64, 0, 0)
#     print("Stepper sequence complete")

#     sleep(5)

while True:
    ws2812b.set_pixel(_WS2812B_left_motor, 0, 64, 0)
    ws2812b.set_pixel(_WS2812B_right_motor, 0, 64, 0)
    ws2812b.set_pixel(_WS2812B_left_eye, 64, 0, 0)
    ws2812b.set_pixel(_WS2812B_right_eye, 64, 0, 0)
    sleep(1)
    ws2812b.set_pixel(_WS2812B_left_motor, 64, 0, 0)
    ws2812b.set_pixel(_WS2812B_right_motor, 64, 0, 0)
    ws2812b.set_pixel(_WS2812B_left_eye, 0, 0, 0)
    ws2812b.set_pixel(_WS2812B_right_eye, 0, 0, 0)
    sleep(1)

# BLE test
demo()