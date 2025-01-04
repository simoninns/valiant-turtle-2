#************************************************************************ 
#
#   commands_tx.py
#
#   Command Tx handling
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

import asyncio
import logging
import struct
import threading
from ble_central import BleCentral

# Note: The commands are defined in the BLE peripheral firmware
# and the ControlRx class must match the ControlTx class otherwise
# bad things will happen :)

class CommandsTx:
    def __init__(self):
        self._ble_central = BleCentral()
        self._command_sequence = 1

        self._short_timeout = 5.0
        self._long_timeout = 60.0

        self._connect = False
        
    def connect(self):
        if not self._connect:
            logging.info("CommandsTx::connect - Staring the BLE central role")
            # Start the BleCentral event loop in the background
            self._loop = asyncio.new_event_loop()
            self._thread = threading.Thread(target=self._start_event_loop, args=(self._loop,))
            self._thread.start()
            self._loop.call_soon_threadsafe(self._loop.create_task, self._ble_central.run())
            self._connect = True

    def disconnect(self):
        if self._connect:
            # Disconnect the BLE
            logging.info("CommandsTx::disconnect - Disconnecting BLE")
            self._ble_central.disconnect()
            
            # Stop the event loop
            logging.info("CommandsTx::disconnect - Stopping event loop")
            self._loop.call_soon_threadsafe(self._loop.stop)
            
            # Wait for the thread to finish
            logging.info("CommandsTx::disconnect - Waiting for thread to finish")
            self._thread.join()

            logging.info("CommandsTx::disconnect - Stopped the BLE central role")
            self._loop = None
            self._thread = None
            self._connect = False

    def _start_event_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def __next_seq(self) -> int:
        self._command_sequence += 1
        if self._command_sequence > 255:
            self._command_sequence = 1
        return self._command_sequence
    
    async def __wait_for_command_response(self, seq_id: int) -> bytes:
        while True:
            await self._ble_central._p2c_queue_event.wait()
            try:
                data = self._ble_central._p2c_queue.pop(0)
            except IndexError:
                logging.error("CommandsTx::__wait_for_command_response - Got P2C queue event but the queue was empty?")
                seq_id_rx = 0
                return None

            self._ble_central._p2c_queue_event.clear()
            seq_id_rx = data[0]

            # Check if the sequence ID matches
            if seq_id_rx == seq_id:
                #logging.info(f"CommandsTx::__wait_for_command_response - Sequence ID = {seq_id_rx} matched")
                return data
            else:
                logging.info(f"CommandsTx::__wait_for_command_response - Sequence ID = {seq_id_rx} did not match received sequence ID = {seq_id}")

    @property
    def connected(self):
        return self._ble_central.connected

    # Synchronous methods to call the asynchronous methods ------------------------------------------------------------

    def motors(self, enable: bool) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::motors - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._motors(enable), self._loop).result()

    def forward(self, distance_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::forward - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._forward(distance_mm), self._loop).result()

    def backward(self, distance_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::backward - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._backward(distance_mm), self._loop).result()

    def left(self, angle_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::left - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._left(angle_degrees), self._loop).result()

    def right(self, angle_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::right - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._right(angle_degrees), self._loop).result()
    
    def circle(self, radius_mm: float, extent_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::circle - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._circle(radius_mm, extent_degrees), self._loop).result()

    def setheading(self, angle_degrees: float) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::setheading - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._setheading(angle_degrees), self._loop).result()

    def setx(self, x_mm: float) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::setx - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._setx(x_mm), self._loop).result()

    def sety(self, y_mm: float) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::sety - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._sety(y_mm), self._loop).result()

    def setposition(self, x_mm: float, y_mm: float) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::setposition - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._goto(x_mm, y_mm), self._loop).result()

    def towards(self, x_mm: float, y_mm: float) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::towards - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._towards(x_mm, y_mm), self._loop).result()

    def reset_origin(self) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::reset_origin - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._reset_origin(), self._loop).result()

    def heading(self) -> tuple[bool, float]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::heading - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._heading(), self._loop).result()

    def position(self) -> tuple[bool, float, float]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::position - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._position(), self._loop).result()

    def penup(self) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::penup - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._penup(), self._loop).result()
    
    def pendown(self) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::pendown - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._pendown(), self._loop).result()

    def eyes(self, eye_id, red, green, blue) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::eyes - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._eyes(eye_id, red, green, blue), self._loop).result()

    def power(self) -> tuple[bool, int, int, int]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::power - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._power(), self._loop).result()

    def isdown(self) -> tuple[bool, bool]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::isdown - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._isdown(), self._loop).result()

    def set_linear_velocity(self, target_speed: int, acceleration: int) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::set_linear_velocity - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._set_linear_velocity(target_speed, acceleration), self._loop).result()

    def set_rotational_velocity(self, target_speed: int, acceleration: int) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::set_rotational_velocity - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._set_rotational_velocity(target_speed, acceleration), self._loop).result()

    def get_linear_velocity(self) -> tuple[bool, int, int]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::get_linear_velocity - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._get_linear_velocity(), self._loop).result()

    def get_rotational_velocity(self) -> tuple[bool, int, int]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::get_rotational_velocity - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._get_rotational_velocity(), self._loop).result()

    def set_wheel_diameter_calibration(self, wheel_diameter: int) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::set_wheel_diameter_calibration - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._set_wheel_diameter_calibration(wheel_diameter), self._loop).result()

    def set_axel_distance_calibration(self, axel_distance: int) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::set_axel_distance_calibration - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._set_axel_distance_calibration(axel_distance), self._loop).result()

    def get_wheel_diameter_calibration(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::get_wheel_diameter_calibration - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._get_wheel_diameter_calibration(), self._loop).result()

    def get_axel_distance_calibration(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::get_axel_distance_calibration - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._get_axel_distance_calibration(), self._loop).result()

    def set_turtle_id(self, turtle_id: int) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::set_turtle_id - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._set_turtle_id(turtle_id), self._loop).result()

    def get_turtle_id(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::get_turtle_id - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._get_turtle_id(), self._loop).result()

    def load_config(self) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::load_config - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._load_config(), self._loop).result()

    def save_config(self) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::save_config - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._save_config(), self._loop).result()

    def reset_config(self) -> bool:
        if not self._ble_central.connected:
            raise RuntimeError("CommandsTx::reset_config - The connect method must be called before sending commands")
        return asyncio.run_coroutine_threadsafe(self._reset_config(), self._loop).result()
    
    # Asynchronous methods to send commands to the BLE peripheral -----------------------------------------------------

    async def _motors(self, enable: bool) -> bool:
        if not self._ble_central.connected:
            logging.info("CommandsTx::motors - Not connected to a robot")
            return False
        
        command_id = 1

        # Command to enable or disable the motors
        if enable:
            parameter = 1
        else:
            parameter = 0

        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBB", seq_id, command_id, parameter)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::motors - Command ID = {command_id}, Sequence ID = {seq_id}, enable = {enable}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::motors - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True

    async def _forward(self, distance_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_forward - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 2

        # Command to move the robot forward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_forward - Command ID = {command_id}, Sequence ID = {seq_id}, distance = {distance_mm}")

        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_forward - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_forward - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_forward - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def _backward(self, distance_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_backward - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 3

        # Command to move the robot backward
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, distance_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_backward - Command ID = {command_id}, Sequence ID = {seq_id}, distance = {distance_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_backward - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_backward - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_backward - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def _left(self, angle_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_left - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 4

        # Command to turn the robot left
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_left - Command ID = {command_id}, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_left - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_left - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_left - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def _right(self, angle_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_right - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 5

        # Command to turn the robot right
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_right - Command ID = {command_id}, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_right - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_right - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_right - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def _circle(self, radius_mm: float, extent_degrees: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_circle - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 6

        # Command to turn the robot left on an arc
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, command_id, radius_mm, extent_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_circle - Command ID = {command_id}, Sequence ID = {seq_id}, radius = {radius_mm}, extent = {extent_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_circle - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_circle - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_circle - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading

    async def _setheading(self, angle_degrees: float) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_setheading - Not connected to a robot")
            return False
        
        command_id = 7

        # Command to set the robot heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, angle_degrees)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_setheading - Command ID = {command_id}, Sequence ID = {seq_id}, angle = {angle_degrees}")
        
        # Wait for the command to be processed with a long timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_setheading - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def _setx(self, x_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_setx - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 8

        # Command to set the robot X position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, x_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_setx - Command ID = {command_id}, Sequence ID = {seq_id}, x = {x_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_setx - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_setx - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_setx - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def _sety(self, y_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_sety - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 9

        # Command to set the robot Y position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBf", seq_id, command_id, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_sety - Command ID = {command_id}, Sequence ID = {seq_id}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_sety - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_sety - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_sety - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def _goto(self, x_mm: float, y_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_setposition - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 10

        # Command to set the robot position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, command_id, x_mm, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_setposition - Command ID = {command_id}, Sequence ID = {seq_id}, x = {x_mm}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_setposition - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_setposition - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_setposition - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def _towards(self, x_mm: float, y_mm: float) -> tuple[bool, float, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_towards - Not connected to a robot")
            return False, 0.0, 0.0, 0.0
        
        command_id = 11

        # Command to move the robot towards a point
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBff", seq_id, command_id, x_mm, y_mm)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_towards - Command ID = {command_id}, Sequence ID = {seq_id}, x = {x_mm}, y = {y_mm}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_towards - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0, 0.0

        # Extract the position and heading from the response
        try:
            seq_id, x, y, heading = struct.unpack("<Bfff", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_towards - Error unpacking response: {e}")
            return False, 0.0, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_towards - X = {x}, Y = {y}, heading = {heading}")
        return True, x, y, heading
    
    async def _reset_origin(self) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_reset_origin - Not connected to a robot")
            return False
        
        command_id = 12

        # Command to reset the x,y origin and heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_reset_origin - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_reset_origin - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def _heading(self) -> tuple[bool, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_heading - Not connected to a robot")
            return False, 0.0
        
        command_id = 13

        # Command to get the robot heading
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_heading - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_heading - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0

        # Extract the heading from the response
        try:
            seq_id, heading = struct.unpack("<Bf", response[:5])
        except ValueError as e:
            logging.error(f"CommandsTx::_heading - Error unpacking response: {e}")
            return False, 0.0
        
        heading = round(heading, 2)
        logging.info(f"CommandsTx::_heading - Heading = {heading}")
        return True, heading
    
    async def _position(self) -> tuple[bool, float, float]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_position - Not connected to a robot")
            return False, 0.0, 0.0
        
        command_id = 14

        # Command to get the robot position
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_position - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a long timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._long_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_position - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0.0, 0.0

        # Extract the position from the response
        try:
            seq_id, x, y = struct.unpack("<Bff", response[:9])
        except ValueError as e:
            logging.error(f"CommandsTx::_position - Error unpacking response: {e}")
            return False, 0.0, 0.0
        
        x = round(x, 2)
        y = round(y, 2)
        logging.info(f"CommandsTx::_position - X = {x}, Y = {y}")
        return True, x, y
    
    async def _penup(self) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_penup - Not connected to a robot")
            return False
        
        command_id = 15

        # Command to raise the pen
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_penup - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_penup - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def _pendown(self) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_pendown - Not connected to a robot")
            return False
        
        command_id = 16

        # Command to raise the pen
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_pendown - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_pendown - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def _eyes(self, eye_id, red, green, blue) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_eyes - Not connected to a robot")
            return False
        
        command_id = 17

        # Command to set the eye colour
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBBBBB", seq_id, command_id, eye_id, red, green, blue)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_eyes - Command ID = {command_id}, Sequence ID = {seq_id}, eye_id = {eye_id}, red = {red}, green = {green}, blue = {blue}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_eyes - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def _power(self) -> tuple[bool, int, int, int]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_power - Not connected to a robot")
            return False, 0, 0, 0
        
        command_id = 18

        # Command to get the robot power
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_power - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_power - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0, 0, 0

        # Extract the power from the response
        try:
            seq_id, mv, ma, mw = struct.unpack("<Blll", response[:13])
        except ValueError as e:
            logging.error(f"CommandsTx::_power - Error unpacking response: {e}")
            return False, 0, 0, 0
        logging.info(f"CommandsTx::_power - mV = {mv}, mA = {ma}, mW = {mw}")
        return True, mv, ma, mw 
    
    async def _isdown(self) -> tuple[bool, bool]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_isdown - Not connected to a robot")
            return False, False
        
        command_id = 19

        # Command to get the pen status (True = down, False = up)
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_isdown - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_isdown - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, False

        # Extract the pen status from the response
        try:
            seq_id, pen_down = struct.unpack("<BB", response[:2])
        except ValueError as e:
            logging.error(f"CommandsTx::_isdown - Error unpacking response: {e}")
            return False, False
        logging.info(f"CommandsTx::_isdown - Pen down = {pen_down}")
        return True, pen_down
    
    async def _set_linear_velocity(self, target_speed: int, acceleration: int) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_set_linear_velocity - Not connected to a robot")
            return False
        
        command_id = 20

        # Command to set the linear velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBll", seq_id, command_id, target_speed, acceleration)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::set_linear_velocity - Command ID = {command_id}, Sequence ID = {seq_id}, target_speed = {target_speed}, acceleration = {acceleration}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::set_linear_velocity - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def _set_rotational_velocity(self, target_speed: int, acceleration: int) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_set_rotational_velocity - Not connected to a robot")
            return False
        
        command_id = 21

        # Command to set the rotational velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BBll", seq_id, command_id, target_speed, acceleration)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_set_rotational_velocity - Command ID = {command_id}, Sequence ID = {seq_id}, target_speed = {target_speed}, acceleration = {acceleration}")
        
        # Wait for the command to be processed with a short timeout
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_set_rotational_velocity - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        # This command does not return any data, so we don't need to return any
        return True
    
    async def _get_linear_velocity(self) -> tuple[bool, int, int]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_get_linear_velocity - Not connected to a robot")
            return False, 0, 0
        
        command_id = 22

        # Command to get the linear velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_get_linear_velocity - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_get_linear_velocity - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0, 0

        # Extract the linear velocity from the response
        try:
            seq_id, target_speed, acceleration = struct.unpack("<Bll", response[:9])
        except ValueError as e:
            logging.error(f"CommandsTx::_get_linear_velocity - Error unpacking response: {e}")
            return False, 0, 0
        logging.info(f"CommandsTx::_get_linear_velocity - Target speed = {target_speed}, Acceleration = {acceleration}")
        return True, target_speed, acceleration
    
    async def _get_rotational_velocity(self) -> tuple[bool, int, int]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_get_rotational_velocity - Not connected to a robot")
            return False, 0, 0
        
        command_id = 23

        # Command to get the rotational velocity
        # Generate a sequence ID and queue the command
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_get_rotational_velocity - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        # Wait for the command to be processed with a short timeout
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_get_rotational_velocity - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0, 0

        # Extract the rotational velocity from the response
        try:
            seq_id, target_speed, acceleration = struct.unpack("<Bll", response[:9])
        except ValueError as e:
            logging.error(f"CommandsTx::_get_rotational_velocity - Error unpacking response: {e}")
            return False, 0, 0
        logging.info(f"CommandsTx::_get_rotational_velocity - Target speed = {target_speed}, Acceleration = {acceleration}")
        return True, target_speed, acceleration

    async def _set_wheel_diameter_calibration(self, wheel_diameter: int) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_set_wheel_diameter_calibration - Not connected to a robot")
            return False
        
        command_id = 24

        # Command to set the wheel diameter calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BBi", seq_id, command_id, wheel_diameter)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_set_wheel_diameter_calibration - Command ID = {command_id}, Sequence ID = {seq_id}, wheel_diameter = {wheel_diameter}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_set_wheel_diameter_calibration - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def _set_axel_distance_calibration(self, axel_distance: int) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_set_axel_distance_calibration - Not connected to a robot")
            return False
        
        command_id = 25

        # Command to set the axel distance calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BBi", seq_id, command_id, axel_distance)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_set_axel_distance_calibration - Command ID = {command_id}, Sequence ID = {seq_id}, axel_distance = {axel_distance}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_set_axel_distance_calibration - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def _get_wheel_diameter_calibration(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_get_wheel_diameter_calibration - Not connected to a robot")
            return False, 0
        
        command_id = 26

        # Command to get the wheel diameter calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_get_wheel_diameter_calibration - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_get_wheel_diameter_calibration - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0

        try:
            seq_id, cali_wheel = struct.unpack("<Bi", response[:5])
        except ValueError as e:
            logging.error(f"CommandsTx::_get_wheel_diameter_calibration - Error unpacking response: {e}")
            return False, 0
        logging.info(f"CommandsTx::_get_wheel_diameter_calibration - Calibration wheel diameter = {cali_wheel}")
        return True, cali_wheel

    async def _get_axel_distance_calibration(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_get_axel_distance_calibration - Not connected to a robot")
            return False, 0
        
        command_id = 27

        # Command to get the axel distance calibration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_get_axel_distance_calibration - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_get_axel_distance_calibration - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0

        try:
            seq_id, cali_axel = struct.unpack("<Bi", response[:5])
        except ValueError as e:
            logging.error(f"CommandsTx::_get_axel_distance_calibration - Error unpacking response: {e}")
            return False, 0
        logging.info(f"CommandsTx::_get_axel_distance_calibration - Calibration axel distance = {cali_axel}")
        return True, cali_axel

    async def _set_turtle_id(self, turtle_id: int) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_set_turtle_id - Not connected to a robot")
            return False
        
        command_id = 28

        # Command to set the turtle ID
        seq_id = self.__next_seq()
        data = struct.pack("<BBB", seq_id, command_id, turtle_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_set_turtle_id - Command ID = {command_id}, Sequence ID = {seq_id}, turtle_id = {turtle_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_set_turtle_id - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def _get_turtle_id(self) -> tuple[bool, int]:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_get_turtle_id - Not connected to a robot")
            return False, 0
        
        command_id = 29

        # Command to get the turtle ID
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_get_turtle_id - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            response = await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_get_turtle_id - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False, 0

        try:
            seq_id, turtle_id = struct.unpack("<BB", response[:2])
        except ValueError as e:
            logging.error(f"CommandsTx::_get_turtle_id - Error unpacking response: {e}")
            return False, 0
        logging.info(f"CommandsTx::_get_turtle_id - Turtle ID = {turtle_id}")
        return True, turtle_id

    async def _load_config(self) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_load_config - Not connected to a robot")
            return False
        
        command_id = 30

        # Command to load the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_load_config - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_load_config - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def _save_config(self) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_save_config - Not connected to a robot")
            return False
        
        command_id = 31

        # Command to save the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_save_config - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_save_config - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True

    async def _reset_config(self) -> bool:
        if not self._ble_central.connected:
            logging.error("CommandsTx::_reset_config - Not connected to a robot")
            return False
        
        command_id = 32

        # Command to reset the configuration
        seq_id = self.__next_seq()
        data = struct.pack("<BB", seq_id, command_id)
        self._ble_central.add_to_c2p_queue(data)
        logging.info(f"CommandsTx::_reset_config - Command ID = {command_id}, Sequence ID = {seq_id}")
        
        try:
            await asyncio.wait_for(self.__wait_for_command_response(seq_id), timeout=self._short_timeout)
        except asyncio.TimeoutError:
            logging.error(f"CommandsTx::_reset_config - Command ID = {command_id}, Sequence ID = {seq_id} timed out")
            self._ble_central.disconnect()
            return False

        return True