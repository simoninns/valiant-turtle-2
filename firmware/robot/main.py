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
from configuration import Configuration
from velocity import Velocity, VelocityParameters
from drv8825 import Drv8825
from stepper import Stepper
from metric import Metric
from ble_peripheral import BlePeripheral
from led_fx import LedFx
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
_LED_right_eye = const(3)
_LED_left_eye = const(4)

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
        """ This task processes robot commands received from the BLE central device."""

        # Create a metric object for unit conversion with default calibration values
        metric = Metric()

        # Velocity parameters:
        #   Acceleration in millimeters per second per second
        #   Minimum millimeters Per Second
        #   Maximum millimeters Per Second
        #   Update Intervals per second
        velocity_parameters = VelocityParameters(metric.mm_to_steps(20), metric.mm_to_steps(4), metric.mm_to_steps(400), 16)
        logging.debug(f"Main::robot_control_task - Velocity parameters (in steps) = {velocity_parameters}")

        while True:
            # Wait for a command to be received
            await ble_peripheral.command_queue_event.wait()
            ble_peripheral.command_queue_event.clear()

            # Set the default command response to -1 (no response)
            command_response = -1

            # Process the command
            if ble_peripheral.command_queue:
                robot_command = ble_peripheral.command_queue.pop()
                logging.debug(f"Main::robot_control_task - processing {robot_command}")

                # Motor power on
                if robot_command.command == "motors-on":
                    drv8825.set_enable(True)

                # Motor power off
                if robot_command.command == "motors-off":
                    drv8825.set_enable(False)

                # Forwards
                if robot_command.command == "forward":
                    left_stepper.set_forwards()
                    right_stepper.set_forwards()
                    velocity = Velocity(metric.mm_to_steps(robot_command.parameters[0]), velocity_parameters)
                    left_stepper.set_velocity(velocity)
                    right_stepper.set_velocity(velocity)

                    # Wait for the stepper to finish
                    while left_stepper.is_busy or right_stepper.is_busy:
                        await asyncio.sleep_ms(250)

                # Backwards
                if robot_command.command == "backward":
                    left_stepper.set_backwards()
                    right_stepper.set_backwards()
                    velocity = Velocity(metric.mm_to_steps(robot_command.parameters[0]), velocity_parameters)
                    left_stepper.set_velocity(velocity)
                    right_stepper.set_velocity(velocity)

                    # Wait for the stepper to finish
                    while left_stepper.is_busy or right_stepper.is_busy:
                        await asyncio.sleep_ms(250)

                # Left
                if robot_command.command == "left":
                    left_stepper.set_forwards()
                    right_stepper.set_backwards()
                    velocity = Velocity(metric.degrees_to_steps(robot_command.parameters[0]), velocity_parameters)
                    left_stepper.set_velocity(velocity)
                    right_stepper.set_velocity(velocity)

                    # Wait for the stepper to finish
                    while left_stepper.is_busy or right_stepper.is_busy:
                        await asyncio.sleep_ms(250)

                # Right
                if robot_command.command == "right":
                    left_stepper.set_backwards()
                    right_stepper.set_forwards()
                    velocity = Velocity(metric.degrees_to_steps(robot_command.parameters[0]), velocity_parameters)
                    left_stepper.set_velocity(velocity)
                    right_stepper.set_velocity(velocity)

                    # Wait for the stepper to finish
                    while left_stepper.is_busy or right_stepper.is_busy:
                        await asyncio.sleep_ms(250)

                # Velocity
                if robot_command.command == "velocity":
                    # Update the velocity parameters (parameters are in mm, so we convert to steps)
                    velocity_parameters.acc_spsps = metric.mm_to_steps(robot_command.parameters[0])
                    velocity_parameters.minimum_sps = metric.mm_to_steps(robot_command.parameters[1])
                    velocity_parameters.maximum_sps = metric.mm_to_steps(robot_command.parameters[2])
                    logging.debug(f"Main::robot_control_task - velocity parameters (steps) = {velocity_parameters}")
                
                # Pen up
                if robot_command.command == "penup":
                    pen.up()

                # Pen down
                if robot_command.command == "pendown":
                    pen.down()

                # Left eye colour
                if robot_command.command == "left-eye":
                    led_fx.set_led_colour(_LED_left_eye, robot_command.parameters[0], robot_command.parameters[1], robot_command.parameters[2])

                # Right eye colour
                if robot_command.command == "right-eye":
                    led_fx.set_led_colour(_LED_right_eye, robot_command.parameters[0], robot_command.parameters[1], robot_command.parameters[2])

                # Get power monitor voltage
                if robot_command.command == "get-mv":
                    command_response = int(ina260.voltage_mV)

                # Get power monitor current
                if robot_command.command == "get-ma":
                    command_response = int(ina260.current_mA)

                # Get power monitor watts
                if robot_command.command == "get-mw":
                    command_response = int(ina260.power_mW)

                # Get pen position
                if robot_command.command == "get-pen":
                    if pen.is_servo_up:
                        command_response = 1
                    else:    
                        command_response = 0

                # Set the last processed command UID
                ble_peripheral.last_processed_command_uid = robot_command.command_uid
                ble_peripheral.last_processed_command_response = command_response

    # Async task to monitor the robot
    async def robot_monitor_task():
        """This task monitors the robot's status and updates the status LEDs accordingly.
        
        The status LED pulses green when BLE central is not connected.  If BLE central is connected,
        the status LED pulses blue.  The left and right motor LEDs indicate the direction of the stepper
        motors, with green indicating forwards and red indicating backwards.  If the motors are not in
        motion but are powered and holding position, the LEDs are yellow. If the motors are disabled,
        the LEDs are off.
        """
        loop = 0
        while True:
            if not drv8825.is_enabled:
                led_fx.set_led_colour(_LED_left_motor, 0, 0, 0)
                led_fx.set_led_colour(_LED_right_motor, 0, 0, 0)
            else:
                # Update the stepper motor status LEDs
                if left_stepper.is_busy:
                    if left_stepper.is_forwards: led_fx.set_led_colour(_LED_left_motor, 0, 64, 0)
                    else: led_fx.set_led_colour(_LED_left_motor, 64, 0, 0)
                else:
                    led_fx.set_led_colour(_LED_left_motor, 20, 20, 0)

                if right_stepper.is_busy:
                    # Green = forwards, red = backwards, grey = not in motion
                    if right_stepper.is_forwards: led_fx.set_led_colour(_LED_right_motor, 0, 64, 0)
                    else: led_fx.set_led_colour(_LED_right_motor, 64, 0, 0)
                else:
                    led_fx.set_led_colour(_LED_right_motor, 20, 20, 0)

            # Update the BLE status
            if ble_peripheral.is_central_connected:
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
            await asyncio.sleep_ms(250)

    # Async I/O task generation and launch
    async def aio_main():
        tasks = [
            asyncio.create_task(ble_peripheral.ble_peripheral_task()), # BLE peripheral task
            asyncio.create_task(led_fx.process_leds_task()), # LED effects task

            asyncio.create_task(robot_monitor_task()), # Robot status monitoring task
            asyncio.create_task(robot_control_task()), # Robot control task
        ]
        await asyncio.gather(*tasks)

    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialise the pen control
    pen = Pen(Pin(_GPIO_PEN))
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