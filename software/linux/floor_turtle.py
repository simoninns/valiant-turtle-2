#************************************************************************ 
#
#   floor_turtle.py
#
#   Floor Turtle Interface (wrapper class)
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

from abstract_turtle import TurtleInterface 
from commands_tx import CommandsTx
import time
import math

class FloorTurtle(TurtleInterface):
    def __init__(self, commands_tx: CommandsTx):
        self._commands_tx = commands_tx

    def connect(self):
        """Establish a BLE connection to the turtle."""
        print("connect()")
        self._commands_tx.connect()
        while not self._commands_tx.connected:
            time.sleep(1)

    def disconnect(self):
        """Terminate the BLE connection to the turtle."""
        print("disconnect()")
        self._commands_tx.disconnect()

    def motors(self, state: bool):
        """Control the state of the motors."""
        print(f"motors(state={state})")
        self._commands_tx.motors(state)

    def forward(self, distance: float):
        """Move the turtle forward by a specified distance."""
        print(f"forward(distance={distance})")
        self._commands_tx.forward(distance)

    def backward(self, distance: float):
        """Move the turtle backward by a specified distance."""
        print(f"backward(distance={distance})")
        self._commands_tx.backward(distance)

    def left(self, angle: float):
        """Turn the turtle left by a specified angle."""
        print(f"left(angle={angle})")
        self._commands_tx.left(angle)

    def right(self, angle: float):
        """Turn the turtle right by a specified angle."""
        print(f"right(angle={angle})")
        self._commands_tx.right(angle)

    def circle(self, radius: float, extent: float=360, steps: int=None):
        """Move the turtle in a circle with a specified radius and extent."""
        if steps is None or extent != 360:
            print(f"circle(radius={radius}, extent={extent})")
            self._commands_tx.circle(radius, extent)
        else:
            # This implementation attempts to match the behaviour of turtle.circle()
            # by using a series of straight lines to approximate the circle

            print(f"circle(radius={radius}, extent={extent}, steps={steps})")
            
            # Calculate the angle to turn at each step
            step_angle = 360 / steps
            
            # Adjust starting angle for consistency with turtle.circle()
            start_angle = step_angle / 2  # Pre-rotation applied by turtle.circle()
            turn_direction = -1 if radius < 0 else 1  # Reverse turn for negative radius
            
            # Use chord length for accurate radius
            step_length = 2 * abs(radius) * math.sin(math.pi / steps)
            
            # Rotate to match turtle.circle() starting orientation
            self._commands_tx.left(start_angle * turn_direction)

            for _ in range(steps):
                self._commands_tx.forward(step_length)
                self._commands_tx.left(turn_direction * step_angle)
            
            # Reset the initial rotation to match turtle.circle() final state
            self._commands_tx.right(start_angle * turn_direction)

    def setheading(self, angle: float):
        """Set the turtle's heading to a specified angle."""
        print(f"setheading(angle={angle})")
        self._angle = angle % 360
        self._commands_tx.setheading(self._angle)

    def setx(self, x: float):
        """Set the turtle's x-coordinate."""
        print(f"setx(x={x})")
        self._commands_tx.setx(x)

    def sety(self, y: float):
        """Set the turtle's y-coordinate."""
        print(f"sety(y={y})")
        self._commands_tx.sety(y)

    def setposition(self, x: float, y: float):
        """Set the turtle's position to specified x and y coordinates."""
        print(f"setposition(x={x}, y={y})")
        self._commands_tx.setposition(x, y)

    def towards(self, x: float, y: float):
        """Calculate the angle towards a specified position."""
        print(f"towards(x={x}, y={y})")
        self._commands_tx.towards(x, y)

    def reset_origin(self):
        """Reset the turtle's origin."""
        print("reset_origin()")
        self._commands_tx.reset_origin()

    def heading(self) -> float:
        """Get the turtle's current heading."""
        print("heading()")
        _, self._angle = self._commands_tx.heading()
        return self._angle

    def position(self) -> tuple[float, float]:
        """Get the turtle's current position."""
        _, self._x, self._y = self._commands_tx.position()
        print(f"position() = {self._x}, {self._y}")
        return self._x, self._y

    def penup(self):
        """Lift the pen up."""
        print("penup()")
        self._commands_tx.penup()

    def pendown(self):
        """Put the pen down."""
        print("pendown()")
        self._commands_tx.pendown()

    def eyes(self, eye: int, red: int, green: int, blue: int):
        """Set the color of the turtle's eyes."""
        print(f"eyes(eye={eye}, red={red}, green={green}, blue={blue})")
        if eye < 0 or eye > 2:
            raise ValueError("Eye value must be between 0 and 2")
        red = max(0, min(255, red))
        green = max(0, min(255, green))
        blue = max(0, min(255, blue))
        self._commands_tx.eyes(eye, red, green, blue)

    def power(self) -> tuple[int, int, int]:
        """Returns the power state of the turtle."""
        _, mv, ma, mw = self._commands_tx.power()
        print(f"power() = {mv}mV, {ma}mA, {mw}mW")
        return mv, ma, mw

    def isdown(self) -> bool:
        """Check if the pen is down."""
        is_down = self._commands_tx.isdown()
        print(f"isdown() = {'down' if is_down else 'up'}")
        return is_down

    def set_linear_velocity(self, target_speed: int, acceleration: int):
        """Set the turtle's linear velocity."""
        print(f"set_linear_velocity(target_speed={target_speed}, acceleration={acceleration})")
        self._commands_tx.set_linear_velocity(target_speed, acceleration)

    def set_rotational_velocity(self, target_speed: int, acceleration: int):
        """Set the turtle's rotational velocity."""
        print(f"set_rotational_velocity(target_speed={target_speed}, acceleration={acceleration})")
        self._commands_tx.set_rotational_velocity(target_speed, acceleration)

    def get_linear_velocity(self) -> tuple[int, int]:
        """Get the turtle's current linear velocity."""
        _, target_speed, acceleration = self._commands_tx.get_linear_velocity()
        print(f"get_linear_velocity() = {target_speed}, {acceleration}")
        return target_speed, acceleration

    def get_rotational_velocity(self) -> tuple[int, int]:
        """Get the turtle's current rotational velocity."""
        _, target_speed, acceleration = self._commands_tx.get_rotational_velocity()
        print(f"get_rotational_velocity() = {target_speed}, {acceleration}")
        return target_speed, acceleration

    def set_wheel_diameter_calibration(self, diameter: int):
        """Set the calibration for the wheel diameter."""
        print(f"set_wheel_diameter_calibration(diameter={diameter})")
        self._commands_tx.set_wheel_diameter_calibration(diameter)

    def set_axel_distance_calibration(self, distance: int):
        """Set the calibration for the axel distance."""
        print(f"set_axel_distance_calibration(distance={distance})")
        self._commands_tx.set_axel_distance_calibration(distance)

    def get_wheel_diameter_calibration(self) -> int:
        """Get the current wheel diameter calibration."""
        _, wheel_diameter = self._commands_tx.get_wheel_diameter_calibration()
        print(f"get_wheel_diameter_calibration() = {wheel_diameter}")
        return wheel_diameter

    def get_axel_distance_calibration(self) -> int:
        """Get the current axel distance calibration."""
        _, axel_distance = self._commands_tx.get_axel_distance_calibration()
        print(f"get_axel_distance_calibration() = {axel_distance}")
        return axel_distance

    def set_turtle_id(self, turtle_id: int):
        """Set the turtle's ID."""
        print(f"set_turtle_id(turtle_id={turtle_id})")
        self._commands_tx.set_turtle_id(turtle_id)

    def get_turtle_id(self) -> int:
        """Get the turtle's ID."""
        _, turtle_id = self._commands_tx.get_turtle_id()
        print(f"get_turtle_id() = {turtle_id}")
        return turtle_id

    def load_config(self):
        """Load the turtle's configuration."""
        print("load_config()")
        self._commands_tx.load_config()

    def save_config(self):
        """Save the turtle's configuration."""
        print("save_config()")
        self._commands_tx.save_config()

    def reset_config(self):
        """Reset the turtle's configuration to default."""
        print("reset_config()")
        self._commands_tx.reset_config()

    def speed(self, speed: int):
        """Set the turtle's speed."""
        print(f"speed(speed={speed})")

        if isinstance(speed, int):
            if speed < 0 or speed > 10:
                raise ValueError("Speed must be an integer between 0 and 10")
        elif isinstance(speed, str):
            speed_aliases = {
            "fastest": 0,
            "fast": 10,
            "normal": 6,
            "slow": 3,
            "slowest": 1
            }
            if speed not in speed_aliases:
                raise ValueError("Invalid speed string. Use one of: 'fastest', 'fast', 'normal', 'slow', 'slowest'")
            speed = speed_aliases[speed]
        else:
            raise TypeError("Speed must be an integer or a string")

        if speed == 0:
            speed = 10

        if speed <= 3:
            self._commands_tx.set_linear_velocity(100, 2)
            self._commands_tx.set_rotational_velocity(50, 2)
        elif speed <= 6:
            self._commands_tx.set_linear_velocity(200, 4)
            self._commands_tx.set_rotational_velocity(100, 4)
        elif speed <= 8:
            self._commands_tx.set_linear_velocity(400, 8)
            self._commands_tx.set_rotational_velocity(200, 4)
        else:
            self._commands_tx.set_linear_velocity(600, 16)
            self._commands_tx.set_rotational_velocity(300, 8)
