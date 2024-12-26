#************************************************************************ 
#
#   control.py
#
#   BLE <-> Command interface
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

from ble_peripheral import BlePeripheral
from commands import Commands
import struct

class Control:
    """
    This class is responsible for processing commands received from the central device and 
    calling the appropriate command functions in the Commands class. The commands are then
    responded to with data that is sent back to the central device.
    """
    def __init__(self, ble_peripheral :BlePeripheral, commands :Commands):
        self._ble_peripheral = ble_peripheral
        self._commands = commands

    # Run a task where we wait for BLE c2p queue to have data
    # then process the data as commands which then respond
    # with p2c data
    async def run(self):
        picolog.debug("Control::run - Running")

        while True:
            # Wait for data to arrive in the c2p queue
            while len(self._ble_peripheral.c2p_queue) == 0:
                await asyncio.sleep_ms(250)

            # C2P queue has data - process it
            data = self._ble_peripheral.c2p_queue.pop(0)

            # The first byte is the command ID and the second
            # byte is the sequence number. Unpack the data using struct
            command_id, command_seq = struct.unpack('BB', data[:2])

            if command_id == 1:
                # Command ID 1 = motors
                # Expect a single byte parameter (1 = enable, 0 = disable)
                command_id, command_seq, enable = struct.unpack('BBB', data[:3])
                await self._commands.motors(enable)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 2:
                # Command ID 2 = forward
                # Expect a single float parameter (distance in mm)
                command_id, command_seq, distance_mm = struct.unpack('BBf', data[:6])
                await self._commands.forward(distance_mm)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 3:
                # Command ID 3 = backward
                # Expect a single float parameter (distance in mm)
                command_id, command_seq, distance_mm = struct.unpack('BBf', data[:6])
                await self._commands.backward(distance_mm)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 4:
                # Command ID 4 = left
                # Expect a single float parameter (angle in degrees)
                command_id, command_seq, angle_degrees = struct.unpack('BBf', data[:6])
                await self._commands.left(angle_degrees)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 5:
                # Command ID 5 = right
                # Expect a single float parameter (angle in degrees)
                command_id, command_seq, angle_degrees = struct.unpack('BBf', data[:6])
                await self._commands.right(angle_degrees)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 6:
                # Command ID 6 = heading
                # Expect a single float parameter (heading in degrees)
                command_id, command_seq, heading_degrees = struct.unpack('BBf', data[:6])
                await self._commands.heading(heading_degrees)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 7:
                # Command ID 7 = position_x
                # Expect a single float parameter (x position in mm)
                command_id, command_seq, x_mm = struct.unpack('BBf', data[:6])
                await self._commands.position_x(x_mm)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 8:
                # Command ID 8 = position_y
                # Expect a single float parameter (y position in mm)
                command_id, command_seq, y_mm = struct.unpack('BBf', data[:6])
                await self._commands.position_y(y_mm)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 9:
                # Command ID 9 = position
                # Expect two float parameters (x and y position in mm)
                command_id, command_seq, x_mm, y_mm = struct.unpack('BBff', data[:10])
                await self._commands.position(x_mm, y_mm)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 10:
                # Command ID 10 = towards
                # Expect two float parameters (x and y position in mm)
                command_id, command_seq, x_mm, y_mm = struct.unpack('BBff', data[:10])
                await self._commands.towards(x_mm, y_mm)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 13:
                # Command ID 13 = reset-origin
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                await self._commands.reset_origin()

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 14:
                # Command ID 14 = get-heading
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                heading = await self._commands.get_heading()

                response = struct.pack('Bf', command_seq, heading) + bytes(15)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 15:
                # Command ID 15 = get-position-x
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                x_position, y_position = await self._commands.get_position()

                response = struct.pack('Bf', command_seq, x_position) + bytes(15)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 16:
                # Command ID 16 = get-position-y
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                x_position, y_position = await self._commands.get_position()

                response = struct.pack('Bf', command_seq, y_position) + bytes(15)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 17:
                # Command ID 17 = pen
                # Expect a single byte parameter (0 = down, 1 = up)
                command_id, command_seq, position = struct.unpack('BBB', data[:3])
                await self._commands.pen(position)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 18:
                # Command ID 18 = eyes
                # Expect four byte parameters (eye ID, red, green, blue)
                command_id, command_seq, eye_id, red, green, blue = struct.unpack('BBBBBB', data[:6])
                await self._commands.eyes(eye_id, red, green, blue)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 19:
                # Command ID 19 = get-mv
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                mv = await self._commands.get_mv()

                response = struct.pack('Bf', command_seq, mv) + bytes(15)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 20:
                # Command ID 20 = get-ma
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                ma = await self._commands.get_ma()

                response = struct.pack('Bf', command_seq, ma) + bytes(15)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 21:
                # Command ID 21 = get-mw
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                mw = await self._commands.get_mw()

                response = struct.pack('Bf', command_seq, mw) + bytes(15)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 22:
                # Command ID 22 = get-pen
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                pen_position = await self._commands.get_pen()

                response = struct.pack('BB', command_seq, pen_position) + bytes(18)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 23:
                # Command ID 23 = set-linear-velocity
                # Expect two float parameters (max speed and acceleration in mm/s^2)
                command_id, command_seq, max_speed, acceleration = struct.unpack('BBff', data[:10])
                await self._commands.set_linear_velocity(max_speed, acceleration)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 24:
                # Command ID 24 = set-rotation-velocity
                # Expect two float parameters (max speed and acceleration in mm/s^2)
                command_id, command_seq, max_speed, acceleration = struct.unpack('BBff', data[:10])
                await self._commands.set_rotational_velocity(max_speed, acceleration)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 25:
                # Command ID 25 = get-linear-velocity
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                linear_max_speed, linear_acceleration = await self._commands.get_linear_velocity()

                response = struct.pack('Bff', command_seq, linear_max_speed, linear_acceleration) + bytes(11)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 27:
                # Command ID 27 = get-rotational-velocity
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                rotation_max_speed, rotation_acceleration = await self._commands.get_rotational_velocity()

                response = struct.pack('Bff', command_seq, rotation_max_speed, rotation_acceleration) + bytes(11)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 29:
                # Command ID 29 = set-cali-wheel
                # Expect a single int32 parameter (wheel diameter adjustment in micrometers)
                command_id, command_seq, wheel_diameter = struct.unpack('BBi', data[:6])
                await self._commands.set_wheel_diameter_calibration(wheel_diameter)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 30:
                # Command ID 30 = set-cali-axel
                # Expect a single int32 parameter (axel distance adjustment in micrometers)
                command_id, command_seq, axel_distance = struct.unpack('BBi', data[:6])
                await self._commands.set_axel_distance_calibration(axel_distance)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 31:
                # Command ID 31 = get-wheel-diameter-calibration
                # Expect no parameters
                command_id, command_seq = struct.unpack('BBi', data[:6])
                cali_wheel = await self._commands.get_wheel_diameter_calibration()

                response = struct.pack('Bi', command_seq, cali_wheel) + bytes(15)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 32:
                # Command ID 32 = get-axel-distance-calibration
                # Expect no parameters
                command_id, command_seq = struct.unpack('BBi', data[:6])
                cali_axel = await self._commands.get_axel_distance_calibration()

                response = struct.pack('Bi', command_seq, cali_axel) + bytes(15)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 33:
                # Command ID 33 = set-turtle-id
                # Expect a single byte parameter (ID)
                command_id, command_seq, turtle_id = struct.unpack('BBB', data[:3])
                await self._commands.set_turtle_id(turtle_id)

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 34:
                # Command ID 34 = get-turtle-id
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                turtle_id = await self._commands.get_turtle_id()

                response = struct.pack('BB', command_seq, turtle_id) + bytes(18)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 35:
                # Command ID 35 = load-config
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                await self._commands.load_config()

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 36:
                # Command ID 36 = save-config
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                await self._commands.save_config()

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            elif command_id == 37:
                # Command ID 37 = reset-config
                # Expect no parameters
                command_id, command_seq = struct.unpack('BB', data[:2])
                await self._commands.reset_config()

                response = struct.pack('B', command_seq) + bytes(19)
                self._ble_peripheral.add_to_p2c_queue(response)
            else:
                picolog.debug(f"Control::run - Unknown command ID = {command_id} received from central")