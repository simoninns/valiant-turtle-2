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

import library.logging as logging

from pen import Pen
from ina260 import Ina260
from library.eeprom import Eeprom
from library.robot_comms import PowerMonitor, RobotCommand
from configuration import Configuration
from velocity import Velocity
from drv8825 import Drv8825
from stepper import Stepper
from metric import Metric
from ble_peripheral import BlePeripheral
from led_fx import LedFx

from time import sleep
from machine import I2C, Pin

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
_LED_left_eye = const(3)
_LED_right_eye = const(4)

def main():
    """
    Main entry point for the Valiant Turtle 2 Robot firmware.
    
    This function initializes various components such as the pen control, I2C buses,
    power monitoring chip, EEPROM, BLE peripheral, stepper motor drivers, and LEDs.
    It also configures logging and launches asynchronous tasks for status LED updates,
    power monitoring, and BLE peripheral tasks.
    """

    # Async task to control the robot
    async def robot_control_task():
        metric = Metric()

        while True:
            # Wait for a command to be received
            await ble_peripheral.command_queue_event.wait()
            ble_peripheral.command_queue_event.clear()

            # Process the command
            if ble_peripheral.command_queue:
                robot_command = ble_peripheral.command_queue.pop()

                # Motor power on
                if robot_command.command == "motors-on":
                    logging.debug("Main::robot_control_task - Motors on")
                    drv8825.set_enable(True)

                # Motor power off
                if robot_command.command == "motors-off":
                    logging.debug("Main::robot_control_task - Motors off")
                    drv8825.set_enable(False)

                # Forwards
                if robot_command.command == "forward":
                    logging.debug("Main::robot_control_task - forwards")
                    left_stepper.set_forwards()
                    right_stepper.set_forwards()
                    velocity = Velocity(robot_command.parameters[0], 32, 2, 1600, 16)
                    left_stepper.set_velocity(velocity)
                    right_stepper.set_velocity(velocity)

                    # Wait for the stepper to finish
                    while left_stepper.is_busy or right_stepper.is_busy:
                        await asyncio.sleep_ms(250)

                # Backwards
                if robot_command.command == "backward":
                    logging.debug("Main::robot_control_task - backwards")
                    left_stepper.set_backwards()
                    right_stepper.set_backwards()
                    velocity = Velocity(robot_command.parameters[0], 32, 2, 1600, 16)
                    left_stepper.set_velocity(velocity)
                    right_stepper.set_velocity(velocity)

                    # Wait for the stepper to finish
                    while left_stepper.is_busy or right_stepper.is_busy:
                        await asyncio.sleep_ms(250)

                # Left
                if robot_command.command == "left":
                    logging.debug("Main::robot_control_task - left")
                    left_stepper.set_forwards()
                    right_stepper.set_backwards()
                    velocity = Velocity(metric.degrees_to_steps(robot_command.parameters[0]), 32, 2, 1600, 16)
                    left_stepper.set_velocity(velocity)
                    right_stepper.set_velocity(velocity)

                    # Wait for the stepper to finish
                    while left_stepper.is_busy or right_stepper.is_busy:
                        await asyncio.sleep_ms(250)

                # Right
                if robot_command.command == "right":
                    logging.debug("Main::robot_control_task - right")
                    left_stepper.set_backwards()
                    right_stepper.set_forwards()
                    velocity = Velocity(metric.degrees_to_steps(robot_command.parameters[0]), 32, 2, 1600, 16)
                    left_stepper.set_velocity(velocity)
                    right_stepper.set_velocity(velocity)

                    # Wait for the stepper to finish
                    while left_stepper.is_busy or right_stepper.is_busy:
                        await asyncio.sleep_ms(250)
                
                # Pen up
                if robot_command.command == "penup":
                    logging.debug("Main::robot_control_task - Pen up")
                    pen.up()

                # Pen down
                if robot_command.command == "pendown":
                    logging.debug("Main::robot_control_task - Pen down")
                    pen.down()

    # Async task to monitor the robot
    async def robot_monitor_task():
        while True:
            # Update the BLE peripheral command status
            if left_stepper.is_busy: ble_peripheral.command_status.left_motor_busy = True
            else: ble_peripheral.command_status.left_motor_busy = False

            if right_stepper.is_busy: ble_peripheral.command_status.right_motor_busy = True
            else: ble_peripheral.command_status.right_motor_busy = False

            if left_stepper.is_forwards: ble_peripheral.command_status.left_motor_direction = True
            else: ble_peripheral.command_status.left_motor_direction = False

            if right_stepper.is_forwards: ble_peripheral.command_status.right_motor_direction = True
            else: ble_peripheral.command_status.right_motor_direction = False

            if drv8825.is_enabled: ble_peripheral.command_status.motor_power_enabled = True
            else: ble_peripheral.command_status.motor_power_enabled = False

            if pen._is_servo_powered: ble_peripheral.command_status.pen_servo_on = True
            else: ble_peripheral.command_status.pen_servo_on = False

            if pen._is_servo_up: ble_peripheral.command_status.pen_servo_up = True
            else: ble_peripheral.command_status.pen_servo_up = False

            # Update the stepper motor status LEDs
            if left_stepper.is_busy:
                if left_stepper.is_forwards: led_fx.set_led_colour(_LED_left_motor, 0, 64, 0)
                else: led_fx.set_led_colour(_LED_left_motor, 64, 0, 0)
            else:
                led_fx.set_led_colour(_LED_left_motor, 8, 8, 8)

            if right_stepper.is_busy:
                # Green = forwards, red = backwards, grey = not in motion
                if right_stepper.is_forwards: led_fx.set_led_colour(_LED_right_motor, 0, 64, 0)
                else: led_fx.set_led_colour(_LED_right_motor, 64, 0, 0)
            else:
                led_fx.set_led_colour(_LED_right_motor, 8, 8, 8)

            # Update the BLE status
            if ble_peripheral.is_central_connected:
                led_fx.set_led_colour(_LED_status, 0, 0, 64)
            else:
                led_fx.set_led_colour(_LED_status, 0, 64, 0)

            await asyncio.sleep_ms(250)

    # Async task to monitor power and send updates to BLE central
    async def power_monitor_task():
        while True:
            # Wait 5 seconds before next update
            await asyncio.sleep_ms(5000)

            # Read the INA260 and send an update to BLE central
            ble_peripheral.power_service_update(ina260.power_monitor)

    # Async I/O task generation and launch
    async def aio_main():
        tasks = [
            asyncio.create_task(ble_peripheral.ble_peripheral_task()), # BLE peripheral task
            asyncio.create_task(led_fx.process_leds_task()), # LED effects task

            asyncio.create_task(power_monitor_task()), # Power monitoring task
            asyncio.create_task(robot_monitor_task()), # Robot status monitoring task
            asyncio.create_task(robot_control_task()), # Robot control task
        ]
        await asyncio.gather(*tasks)

    # Stepper test task
    async def stepper_task():
        # Define a velocity sequence
        velocity = Velocity(6400, 32, 2, 1600, 16)

        while True:
            drv8825.set_enable(True)

            left_stepper.set_forwards()
            right_stepper.set_forwards()
            left_stepper.set_velocity(velocity)
            right_stepper.set_velocity(velocity)
            logging.debug("Main::stepper_task - Steppers running forwards")

            # Wait for the stepper to finish
            while left_stepper.is_busy or right_stepper.is_busy:
                await asyncio.sleep_ms(250)

            left_stepper.set_backwards()
            right_stepper.set_backwards()
            left_stepper.set_velocity(velocity)
            right_stepper.set_velocity(velocity)
            logging.debug("Main::stepper_task - Steppers running backwards")

            # Wait for the stepper to finish
            while left_stepper.is_busy or right_stepper.is_busy:
                await asyncio.sleep_ms(250)

            drv8825.set_enable(False)
            logging.debug("Main::stepper_task - Steppers stopped")

            await asyncio.sleep(5)

    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialise the pen control
    pen = Pen(_GPIO_PEN)
    pen.up()

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

    # Initialise BLE peripheral
    ble_peripheral = BlePeripheral()

    # Configure the DRV8825
    drv8825 = Drv8825(_GPIO_ENABLE, _GPIO_M0, _GPIO_M1, _GPIO_M2)
    drv8825.set_steps_per_revolution(800)
    drv8825.set_enable(False)

    # Configure the steppers
    left_stepper = Stepper(_GPIO_LM_DIR, _GPIO_LM_STEP, True)
    left_stepper.set_forwards()
    right_stepper = Stepper(_GPIO_RM_DIR, _GPIO_RM_STEP, False)
    right_stepper.set_forwards()

    # Configure the LEDs
    led_fx = LedFx(5, _GPIO_LEDS)

    logging.info("main - Launching asynchronous tasks...")
    # Run the main asynchronous I/O tasks
    asyncio.run(aio_main())

main()