#************************************************************************ 
#
#   main.py
#
#   Valiant Turtle 2 - Raspberry Pi Pico W Firmware
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

from ws2812b import Ws2812b
from pen import Pen
from ina260 import Ina260
from eeprom import Eeprom
from velocity import Velocity
from drv8825 import Drv8825
from stepper import Stepper
from metric import Metric
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

# Initialise the LEDs and show some colour
leds = Ws2812b(5, 0, _GPIO_LEDS, delay=0)

# Initialise the pen control
pen = Pen(_GPIO_PEN)
pen.off()

# Initialise the I2C buses
i2c_internal = I2C(0, scl=Pin(_GPIO_SCL0), sda=Pin(_GPIO_SDA0), freq=100000)
i2c_external = I2C(1, scl=Pin(_GPIO_SCL1), sda=Pin(_GPIO_SDA1), freq=100000)

# Initialise the INA260 power monitoring chip
ina260 = Ina260(i2c_internal, 0x40)

# Initialise the EEPROM
eeprom = Eeprom(i2c_internal, 0x50)

# wbuffer = bytearray([0,1,2,3,4,5,6,7,8,9])
# eeprom.write(0x0, wbuffer)
# print("Write Buffer = ", "".join("0x%02x " % b for b in wbuffer))
# print("Read Length = ", len(wbuffer))

# rbuffer = eeprom.read(0x0, 10)
# log_info("Read Buffer = ", "".join("0x%02x " % b for b in rbuffer))
# log_info("Read Length = ", len(rbuffer))
# log_info("")

# LED test
leds.set_pixel(0, 255, 0, 0)
leds.set_pixel(1, 0, 255, 0)
leds.set_pixel(2, 0, 0, 255)
leds.set_pixel(3, 255, 0, 0)
leds.set_pixel(4, 0, 255, 0)
leds.show()

# log_info("INA260:")
# log_info("  mA = ", ina260.current)
# log_info("  mV = ", ina260.bus_voltage)
# log_info("  mW = ", ina260.power)
# sleep(1.0)

# Configure the DRV8825
drv8825 = Drv8825(_GPIO_ENABLE, _GPIO_M0, _GPIO_M1, _GPIO_M2)
drv8825.set_steps_per_revolution(800)
drv8825.set_enable(False)

# # Configure the steppers
# left_stepper = Stepper(_GPIO_LM_DIR, _GPIO_LM_STEP, True)
# left_stepper.set_forwards()
# right_stepper = Stepper(_GPIO_RM_DIR, _GPIO_RM_STEP, False)
# right_stepper.set_forwards()

# # Define a velocity sequence
# velocity = Velocity(6400, 32, 2, 1600, 16)

# # Test metric methods
# metric = Metric()
# print("100mm to steps =", metric.mm_to_steps(100))
# print("360 degrees to steps =", metric.degrees_to_steps(360))

# while True:
#     drv8825.set_enable(True)
#     left_stepper.set_velocity(velocity)
#     right_stepper.set_velocity(velocity)
#     print("Stepper sequence running")

#     # Wait for the stepper to finish
#     while left_stepper.is_busy or right_stepper.is_busy:
#         sleep(0.01)
#     drv8825.set_enable(False)
#     print("Stepper sequence complete")

#     sleep(5)

# BLE test
demo()