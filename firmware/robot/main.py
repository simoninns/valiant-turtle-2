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
from ble_peripheral import BlePeripheral
from led_fx import LedFx
from diffdrive import DiffDrive
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

        # Velocity parameters:
        #   Acceleration in millimeters per second per second
        #   Minimum millimeters Per Second
        #   Maximum millimeters Per Second
        #   Update Intervals per second
        # velocity_parameters = VelocityParameters(metric.mm_to_steps(20), metric.mm_to_steps(4), metric.mm_to_steps(400), 16)
        # logging.debug(f"Main::robot_control_task - Velocity parameters (in steps) = {velocity_parameters}")

        while True:
            # Wait for a command to be received
            await ble_peripheral.command_queue_event.wait()
            ble_peripheral.command_queue_event.clear()

            # Set the default command response to -1 (no response)
            command_response = -1

            # Process the command
            if ble_peripheral.command_queue:
                robot_command = ble_peripheral.command_queue.pop()
                logging.info(f"Main::robot_control_task - processing {robot_command}")

                # Motor power control
                if robot_command.command == "motors":
                    if robot_command.parameters[0] == 1:
                        diff_drive.set_enable(True)
                    else:
                        diff_drive.set_enable(False)

                # Forward
                if robot_command.command == "forward":
                    diff_drive.drive_forward(robot_command.parameters[0])

                    # Wait for the drive to finish
                    while diff_drive.is_moving:
                        await asyncio.sleep_ms(250)

                # Backward
                if robot_command.command == "backward":
                    diff_drive.drive_backward(robot_command.parameters[0])

                    # Wait for the drive to finish
                    while diff_drive.is_moving:
                        await asyncio.sleep_ms(250)

                # Left
                if robot_command.command == "left":
                    diff_drive.turn_left(robot_command.parameters[0])

                    # Wait for the drive to finish
                    while diff_drive.is_moving:
                        await asyncio.sleep_ms(250)

                # Right
                if robot_command.command == "right":
                    diff_drive.turn_right(robot_command.parameters[0])

                    # Wait for the drive to finish
                    while diff_drive.is_moving:
                        await asyncio.sleep_ms(250)

                # Linear Velocity
                if robot_command.command == "linear-v":
                    diff_drive.set_linear_velocity(robot_command.parameters[0], robot_command.parameters[1])
                    logging.debug(f"Main::robot_control_task - Setting linear target speed to = {robot_command.parameters[0]} mm/s and acceleration to = {robot_command.parameters[1]} mm/s^2")
                
                # Rotational Velocity
                if robot_command.command == "rotation-v":
                    diff_drive.set_rotational_velocity(robot_command.parameters[0], robot_command.parameters[1])
                    logging.debug(f"Main::robot_control_task - Setting rotational target speed to = {robot_command.parameters[0]} mm/s and acceleration to = {robot_command.parameters[1]} mm/s^2")

                # Pen control
                if robot_command.command == "pen":
                    if robot_command.parameters[0] == 1:
                        pen.up()
                    else:
                        pen.down()

                # Eye colour
                if robot_command.command == "eyes":
                    if robot_command.parameters[0] == 0:
                        # Both eyes
                        led_fx.set_led_colour(_LED_left_eye, robot_command.parameters[1], robot_command.parameters[2], robot_command.parameters[3])
                        led_fx.set_led_colour(_LED_right_eye, robot_command.parameters[1], robot_command.parameters[2], robot_command.parameters[3])
                    elif robot_command.parameters[0] == 1:
                        # Left eye
                        led_fx.set_led_colour(_LED_left_eye, robot_command.parameters[1], robot_command.parameters[2], robot_command.parameters[3])
                    else:
                        # Right eye
                        led_fx.set_led_colour(_LED_right_eye, robot_command.parameters[1], robot_command.parameters[2], robot_command.parameters[3])
           
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

                # Calibrate wheel diameter
                if robot_command.command == "cali-wheel":
                    diff_drive.set_wheel_calibration(robot_command.parameters[0])

                # Calibrate axel distance
                if robot_command.command == "cali-axel":
                    diff_drive.set_axel_calibration(robot_command.parameters[0])

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

    # Configure the LEDs
    led_fx = LedFx(5, _GPIO_LEDS)

    # Initialise the differential drive motor control
    diff_drive = DiffDrive(_GPIO_ENABLE, _GPIO_M0, _GPIO_M1, _GPIO_M2, _GPIO_LM_STEP, _GPIO_LM_DIR, _GPIO_RM_STEP, _GPIO_RM_DIR)

    logging.info("main - Launching asynchronous tasks...")
    # Run the main asynchronous I/O tasks
    asyncio.run(aio_main())

main()