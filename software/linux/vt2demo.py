#************************************************************************ 
#
#   main.py
#
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
import asyncio
from ble_central import BleCentral
from commands_tx import CommandsTx

async def command_test(ble_central: BleCentral, commands_tx: CommandsTx):
    while True:
        if ble_central.is_connected:
            result = await commands_tx.motors(False) # 1
            await asyncio.sleep(1)
            result = await commands_tx.motors(True) # 1

            result = await commands_tx.forward(50) # 2
            result = await commands_tx.backward(50) # 3
            result = await commands_tx.left(10) # 4
            result = await commands_tx.right(10) # 5

            result = await commands_tx.heading(20) # 6
            result = await commands_tx.position_x(100) # 7
            result = await commands_tx.position_y(100) # 8
            result = await commands_tx.position(50, 50) # 9
            result = await commands_tx.towards(75, 75) # 10
            
            result, heading = await commands_tx.get_heading() # 12
            print(f"Heading: {heading}")
            result, x, y = await commands_tx.get_position() # 13
            print(f"Position: {x}, {y}")

            result = await commands_tx.reset_origin() # 11

            # Pen servo test
            result = await commands_tx.pen(False) # 14
            await asyncio.sleep(1)
            result, pen_up = await commands_tx.get_pen() # 17
            print(f"Pen up: {'up' if pen_up else 'down'}")
            result = await commands_tx.pen(True) # 14
            await asyncio.sleep(1)
            result, pen_up = await commands_tx.get_pen() # 17
            print(f"Pen up: {'up' if pen_up else 'down'}")

            # Eyes test
            result = await commands_tx.eyes(0, 255, 0, 0) # 15
            await asyncio.sleep(1)
            result = await commands_tx.eyes(1, 0, 255, 0)
            await asyncio.sleep(1)
            result = await commands_tx.eyes(2, 0, 0, 255)
            await asyncio.sleep(1)
            result = await commands_tx.eyes(0, 0, 0, 0)
            await asyncio.sleep(1)

            # Power test
            result, mv, ma, mw = await commands_tx.get_power() # 16
            print(f"Power: {mv}mV, {ma}mA, {mw}mW")

            # Velocity setting test
            result = await commands_tx.set_linear_velocity(400, 8) # 18
            result = await commands_tx.set_rotational_velocity(400, 8) # 19

            result, target_speed, acceleration = await commands_tx.get_linear_velocity() # 20
            print(f"Linear velocity: {target_speed}, {acceleration}")
            result, target_speed, acceleration = await commands_tx.get_rotational_velocity() # 21
            print(f"Rotational velocity: {target_speed}, {acceleration}")

            result = await commands_tx.set_linear_velocity(200, 4) # 18
            result = await commands_tx.set_rotational_velocity(200, 4) # 19

            result, target_speed, acceleration = await commands_tx.get_linear_velocity() # 20
            print(f"Linear velocity: {target_speed}, {acceleration}")
            result, target_speed, acceleration = await commands_tx.get_rotational_velocity() # 21
            print(f"Rotational velocity: {target_speed}, {acceleration}")

            # Calibration test
            result = await commands_tx.set_wheel_diameter_calibration(1234) # 22
            result = await commands_tx.set_axel_distance_calibration(4321) # 23

            result, wheel_diameter = await commands_tx.get_wheel_diameter_calibration() # 24
            print(f"Wheel diameter calibration: {wheel_diameter} um")
            result, axel_distance = await commands_tx.get_axel_distance_calibration() # 25
            print(f"Axel distance calibration: {axel_distance} um")

            result = await commands_tx.set_wheel_diameter_calibration(0) # 22
            result = await commands_tx.set_axel_distance_calibration(0) # 23

            result, wheel_diameter = await commands_tx.get_wheel_diameter_calibration() # 24
            print(f"Wheel diameter calibration: {wheel_diameter} um")
            result, axel_distance = await commands_tx.get_axel_distance_calibration() # 25
            print(f"Axel distance calibration: {axel_distance} um")

            result = await commands_tx.set_turtle_id(2) # 26
            result, turtle_id = await commands_tx.get_turtle_id() # 27
            print(f"Turtle ID: {turtle_id}")

            result = await commands_tx.set_turtle_id(0) # 26
            result, turtle_id = await commands_tx.get_turtle_id() # 27
            print(f"Turtle ID: {turtle_id}")

            result = await commands_tx.load_config() # 28
            result = await commands_tx.save_config() # 29
            result = await commands_tx.reset_config() # 30

        else:
            await asyncio.sleep(1)

async def aio_main():
    logging.info("Running BLE central async tasks") 
    ble_central = BleCentral()
    commands_tx = CommandsTx(ble_central)

    tasks = [
        asyncio.create_task(ble_central.run()),
        asyncio.create_task(command_test(ble_central, commands_tx)),
    ]
    await asyncio.gather(*tasks)

def main():
    # Configure the logging module
    log_format = "[%(asctime)s %(filename)s::%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, filename="vt2demo.log")

    asyncio.run(aio_main())

if __name__ == "__main__":
    main()