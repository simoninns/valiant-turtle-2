#************************************************************************ 
#
#   abstract_turtle.py
#
#   Abstract Turtle Interface (base class)
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

from abc import ABC, abstractmethod
from typing import NoReturn

class TurtleInterface(ABC):
    @abstractmethod
    def connect(self) -> NoReturn:
        """Establish a BLE connection to the turtle."""
        pass

    @abstractmethod
    def disconnect(self) -> NoReturn:
        """Terminate the BLE connection to the turtle."""
        pass

    @abstractmethod
    def motors(self, state: bool) -> NoReturn:
        """Control the state of the motors."""
        pass

    @abstractmethod
    def forward(self, distance: float) -> NoReturn:
        """Move the turtle forward by a specified distance."""
        pass

    # Alias for forward
    def fd(self, distance: float) -> NoReturn:
        return self.forward(distance)

    @abstractmethod
    def backward(self, distance: float) -> NoReturn:
        """Move the turtle backward by a specified distance."""
        pass

    # Alias for backward
    def bk(self, distance: float) -> NoReturn:
        return self.backward(distance)

    @abstractmethod
    def left(self, angle: float) -> NoReturn:
        """Turn the turtle left by a specified angle."""
        pass

    # Alias for left
    def lt(self, angle: float) -> NoReturn:
        return self.left(angle)

    @abstractmethod
    def right(self, angle: float) -> NoReturn:
        """Turn the turtle right by a specified angle."""
        pass

    # Alias for right
    def rt(self, angle: float) -> NoReturn:
        return self.right(angle)

    @abstractmethod
    def circle(self, radius: float, extent: float, steps: int) -> NoReturn:
        """Move the turtle in a circle with a specified radius and extent."""
        pass

    @abstractmethod
    def setheading(self, angle: float) -> NoReturn:
        """Set the turtle's heading to a specified angle."""
        pass

    # Alias for setheading
    def seth(self, angle: float) -> NoReturn:
        return self.setheading(angle)

    @abstractmethod
    def setx(self, x: float) -> NoReturn:
        """Set the turtle's x-coordinate."""
        pass

    @abstractmethod
    def sety(self, y: float) -> NoReturn:
        """Set the turtle's y-coordinate."""
        pass

    @abstractmethod
    def setposition(self, x: float, y: float) -> NoReturn:
        """Set the turtle's position to specified x and y coordinates."""
        pass

    # Alias for setposition
    def goto(self, x: float, y: float) -> NoReturn:
        return self.setposition(x, y)
    
    def setpos(self, x: float, y: float) -> NoReturn:
        return self.setposition(x, y)  

    @abstractmethod
    def towards(self, x: float, y: float) -> NoReturn:
        """Calculate the angle towards a specified position."""
        pass

    @abstractmethod
    def reset_origin(self) -> NoReturn:
        """Reset the turtle's origin."""
        pass

    @abstractmethod
    def heading(self) -> float:
        """Get the turtle's current heading."""
        pass

    @abstractmethod
    def position(self) -> tuple[float, float]:
        """Get the turtle's current position."""
        pass

    # Alias for position
    def pos(self) -> tuple[float, float]:
        return self.position()
    
    def xcor(self) -> float:
        return self.position()[0]
    
    def ycor(self) -> float:
        return self.position()[1]

    @abstractmethod
    def penup(self) -> NoReturn:
        """Lift the pen up."""
        pass

    # Alias for penup
    def pu(self) -> NoReturn:
        return self.penup()
    
    def up(self) -> NoReturn:
        return self.penup()

    @abstractmethod
    def pendown(self) -> NoReturn:
        """Put the pen down."""
        pass

    # Alias for pendown
    def pd(self) -> NoReturn:
        return self.pendown()
    
    def down(self) -> NoReturn:
        return self.pendown()

    @abstractmethod
    def eyes(self, eye: int, red: int, green :int, blue :int) -> NoReturn:
        """Set the color of the turtle's eyes."""
        pass

    @abstractmethod
    def power(self) -> tuple[int, int, int]:
        """Returns the power state of the turtle."""
        pass

    @abstractmethod
    def isdown(self) -> bool:
        """Check if the pen is down."""
        pass

    @abstractmethod
    def set_linear_velocity(self, target_speed: int, acceleration: int) -> NoReturn:
        """Set the turtle's linear velocity."""
        pass

    @abstractmethod
    def set_rotational_velocity(self, target_speed: int, acceleration: int) -> NoReturn:
        """Set the turtle's rotational velocity."""
        pass

    @abstractmethod
    def get_linear_velocity(self) -> tuple[int, int]:
        """Get the turtle's current linear velocity."""
        pass

    @abstractmethod
    def get_rotational_velocity(self) -> tuple[int, int]:
        """Get the turtle's current rotational velocity."""
        pass

    @abstractmethod
    def set_wheel_diameter_calibration(self, diameter: int) -> NoReturn:
        """Set the calibration for the wheel diameter."""
        pass

    @abstractmethod
    def set_axel_distance_calibration(self, distance: int) -> NoReturn:
        """Set the calibration for the axel distance."""
        pass

    @abstractmethod
    def get_wheel_diameter_calibration(self) -> int:
        """Get the current wheel diameter calibration."""
        pass

    @abstractmethod
    def get_axel_distance_calibration(self) -> int:
        """Get the current axel distance calibration."""
        pass

    @abstractmethod
    def set_turtle_id(self, turtle_id: int) -> NoReturn:
        """Set the turtle's ID."""
        pass

    @abstractmethod
    def get_turtle_id(self) -> int:
        """Get the turtle's ID."""
        pass

    @abstractmethod
    def load_config(self) -> NoReturn:
        """Load the turtle's configuration."""
        pass

    @abstractmethod
    def save_config(self) -> NoReturn:
        """Save the turtle's configuration."""
        pass

    @abstractmethod
    def reset_config(self) -> NoReturn:
        """Reset the turtle's configuration to default."""
        pass

    @abstractmethod
    def speed(self, speed) -> NoReturn:
        """Set the turtle's speed."""
        pass