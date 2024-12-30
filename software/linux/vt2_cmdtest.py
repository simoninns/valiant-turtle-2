#************************************************************************ 
#
#   vt2_cmdtest.py
#
#   Automatic command testing
#   Valiant Turtle 2 - Communicator Linux Firmware
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

import logging
import time
from commands_tx import CommandsTx
import sys

def command_test(commands_tx: CommandsTx):
    logging.info("Running command tests...")

    commands_tx.motors(False)
    time.sleep(1)
    commands_tx.motors(True)

    commands_tx.forward(50)
    commands_tx.backward(50)
    commands_tx.left(10)
    commands_tx.right(10)

    commands_tx.arc_left(100, 90)
    commands_tx.arc_right(100, 90)

    commands_tx.heading(20)
    commands_tx.position_x(100)
    commands_tx.position_y(100)
    commands_tx.position(50, 50)
    commands_tx.towards(75, 75)
    
    _, heading = commands_tx.get_heading()
    print(f"Heading: {heading}")
    _, x, y = commands_tx.get_position()
    print(f"Position: {x}, {y}")

    commands_tx.reset_origin()

    # Pen servo test
    commands_tx.pen(False)
    time.sleep(1)
    _, pen_up = commands_tx.get_pen()
    print(f"Pen up: {'up' if pen_up else 'down'}")
    commands_tx.pen(True)
    time.sleep(1)
    _, pen_up = commands_tx.get_pen()
    print(f"Pen up: {'up' if pen_up else 'down'}")

    # Eyes test
    commands_tx.eyes(0, 255, 0, 0)
    time.sleep(1)
    commands_tx.eyes(1, 0, 255, 0)
    time.sleep(1)
    commands_tx.eyes(2, 0, 0, 255)
    time.sleep(1)
    commands_tx.eyes(0, 0, 0, 0)
    time.sleep(1)

    # Power test
    _, mv, ma, mw = commands_tx.get_power()
    print(f"Power: {mv}mV, {ma}mA, {mw}mW")

    # Velocity setting test
    commands_tx.set_linear_velocity(400, 8)
    commands_tx.set_rotational_velocity(400, 8)

    _, target_speed, acceleration = commands_tx.get_linear_velocity()
    print(f"Linear velocity: {target_speed}, {acceleration}")
    _, target_speed, acceleration = commands_tx.get_rotational_velocity()
    print(f"Rotational velocity: {target_speed}, {acceleration}")

    commands_tx.set_linear_velocity(200, 4)
    commands_tx.set_rotational_velocity(200, 4)

    _, target_speed, acceleration = commands_tx.get_linear_velocity()
    print(f"Linear velocity: {target_speed}, {acceleration}")
    _, target_speed, acceleration = commands_tx.get_rotational_velocity()
    print(f"Rotational velocity: {target_speed}, {acceleration}")

    # Calibration test
    commands_tx.set_wheel_diameter_calibration(1234)
    commands_tx.set_axel_distance_calibration(4321)

    _, wheel_diameter = commands_tx.get_wheel_diameter_calibration()
    print(f"Wheel diameter calibration: {wheel_diameter} um")
    _, axel_distance = commands_tx.get_axel_distance_calibration()
    print(f"Axel distance calibration: {axel_distance} um")

    commands_tx.set_wheel_diameter_calibration(0)
    commands_tx.set_axel_distance_calibration(0)

    _, wheel_diameter = commands_tx.get_wheel_diameter_calibration()
    print(f"Wheel diameter calibration: {wheel_diameter} um")
    _, axel_distance = commands_tx.get_axel_distance_calibration()
    print(f"Axel distance calibration: {axel_distance} um")

    commands_tx.set_turtle_id(2)
    _, turtle_id = commands_tx.get_turtle_id()
    print(f"Turtle ID: {turtle_id}")

    commands_tx.set_turtle_id(0)
    _, turtle_id = commands_tx.get_turtle_id()
    print(f"Turtle ID: {turtle_id}")

    commands_tx.load_config()
    commands_tx.save_config()
    commands_tx.reset_config()

    commands_tx.motors(False)

def main():
    # Configure the logging module
    log_format = "[%(asctime)s %(filename)s::%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, filename="vt2_cmdtest.log")

    commands_tx = CommandsTx()

    # Wait for BLE connection
    commands_tx.connect()
    logging.info("Waiting for BLE connection...")
    while not commands_tx.connected:
        time.sleep(1)
    logging.info("Connected to BLE")

    command_test(commands_tx)
    logging.info("Command tests completed. Exiting program.")
    commands_tx.disconnect()
    logging.info("Disconnected from BLE")

    sys.exit(0)

if __name__ == "__main__":
    main()