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

import picolog

from pen import Pen
from ina260 import Ina260
from eeprom import Eeprom
from configuration import Configuration
from ble_peripheral import BlePeripheral
from led_fx import LedFx
from diffdrive import DiffDrive
from machine import I2C, Pin
from commands_rx import CommandsRx
from control import Control
import asyncio

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

# WS2812b led number mapping
_LED_status = const(0)
_LED_left_motor = const(1)
_LED_right_motor = const(2)
_LED_right_eye = const(3)
_LED_left_eye = const(4)

def main():
    # Async task to monitor the status of the robot and show it in the LEDs
    async def robot_status_task():
        """This task monitors the robot's status and updates the status LEDs accordingly.
    
        The status LED pulses green when BLE central is not connected.  If BLE central is connected,
        the status LED pulses blue.  The left and right motor LEDs indicate the direction of the stepper
        motors, with green indicating forwards and red indicating backwards.  If the motors are not in
        motion but are powered and holding position, the LEDs are yellow. If the motors are disabled,
        the LEDs are off.
        """
        loop = 0
        while True:
            # Show the differential drive status
            if not diff_drive.is_enabled:
                led_fx.set_led_colour(_LED_left_motor, 0, 0, 0)
                led_fx.set_led_colour(_LED_right_motor, 0, 0, 0)
            else:
                left_status, right_status = diff_drive.get_motor_status()
                if left_status == 0:
                    # Motor is idle
                    led_fx.set_led_colour(_LED_left_motor, 20, 20, 0)
                elif left_status == 1:
                    # Motor is moving forwards
                    led_fx.set_led_colour(_LED_left_motor, 0, 64, 0)
                else:
                    # Motor is moving backwards
                    led_fx.set_led_colour(_LED_left_motor, 64, 0, 0)

                if right_status == 0:
                    # Motor is idle
                    led_fx.set_led_colour(_LED_right_motor, 20, 20, 0)
                elif right_status == 1:
                    # Motor is moving forwards
                    led_fx.set_led_colour(_LED_right_motor, 0, 64, 0)
                else:
                    # Motor is moving backwards
                    led_fx.set_led_colour(_LED_right_motor, 64, 0, 0)

            if power_low_event.is_set():
                led_fx.set_led_colour(_LED_status, 255, 0, 0)
            else:
                # Update the BLE status
                if ble_peripheral.is_connected:
                    if loop < 2:
                        led_fx.set_led_colour(_LED_status, 0, 0, 64)
                    else:
                        led_fx.set_led_colour(_LED_status, 0, 0, 32)
                else:
                    if loop < 2:
                        led_fx.set_led_colour(_LED_status, 0, 64, 0)
                    else:
                        led_fx.set_led_colour(_LED_status, 0, 32, 0)

            loop += 1
            if loop > 3: loop = 0
            await asyncio.sleep(0.25)

    # Power monitoring task
    async def power_monitor_task():
        while True:
            # Read the power from the INA260
            current = ina260.current_mA
            voltage = ina260.voltage_mV
            power = ina260.power_mW

            picolog.debug(f"Power monitor: {voltage}mV, {current}mA, {power}mW")

            # Check if the power level is below the minimum allowed
            # cell voltage (3.0V) and set the event flag
            if (voltage < 12000):
                if not power_low_event.is_set():
                    picolog.warning("Power monitor: Power low event set")
                    power_low_event.set()
            else:
                if power_low_event.is_set():
                    picolog.warning("Power monitor: Power low event cleared")
                    power_low_event.clear()

            await asyncio.sleep(5)

    # Async task generation and launch
    async def aio_main():
        tasks = [
            asyncio.create_task(ble_peripheral.run()), # BLE peripheral tasks
            asyncio.create_task(control.run()), # Control task (BLE <-> Commands)
            asyncio.create_task(led_fx.run()), # LED effects task
            asyncio.create_task(robot_status_task()), # Robot status monitoring task
            asyncio.create_task(power_monitor_task()), # Robot power monitoring task
        ]
        await asyncio.gather(*tasks)

    # Configure the picolog module
    picolog.basicConfig(level=picolog.DEBUG)

    # Initialise the pen control
    pen = Pen(Pin(_GPIO_PEN))
    pen.up()

    # Initialise the I2C buses
    i2c_internal = I2C(0, scl=Pin(_GPIO_SCL0), sda=Pin(_GPIO_SDA0), freq=400000)
    i2c_external = I2C(1, scl=Pin(_GPIO_SCL1), sda=Pin(_GPIO_SDA1), freq=400000)

    # Initialise the INA260 power monitoring chip
    ina260 = Ina260(i2c_internal, 0x40)
    power_low_event = asyncio.Event()

    # Initialise the EEPROM
    eeprom = Eeprom(i2c_internal, 0x50)

    # Initialise BLE peripheral
    ble_peripheral = BlePeripheral()

    # Configure the LEDs
    led_fx = LedFx(5, _GPIO_LEDS)

    # Initialise the differential drive motor control
    diff_drive = DiffDrive(_GPIO_ENABLE, _GPIO_M0, _GPIO_M1, _GPIO_M2, _GPIO_LM_STEP, _GPIO_LM_DIR, _GPIO_RM_STEP, _GPIO_RM_DIR)

    # Read the configuration from EEPROM
    configuration = Configuration()
    if not configuration.unpack(eeprom.read(0, configuration.pack_size)):
        # Current EEPROM image is invalid, write the default
        eeprom.write(0, configuration.pack())

    # Initialise the BLE peripheral
    ble_peripheral = BlePeripheral()

    # Initialise the commands handler
    commands = CommandsRx(pen, ina260, eeprom, led_fx, diff_drive, configuration)

    # Initialise the control handler
    control = Control(ble_peripheral, commands, power_low_event)

    # Run
    asyncio.run(aio_main())

main()