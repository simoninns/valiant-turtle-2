#************************************************************************ 
#
#   screen_turtle.py
#
#   Screen Turtle Interface (wrapper class)
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

from turtle import Turtle, Screen
from abstract_turtle import TurtleInterface

class ScreenTurtle(TurtleInterface):
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=841, height=594) # A1 paper size landscape
        self._turtle = Turtle()

        # Give the screen a title
        self.screen.title("Valiant Turtle 2")

    def forward(self, distance: float):
        """Move the turtle forward by a specified distance."""
        self._turtle.forward(distance)

    def backward(self, distance: float):
        """Move the turtle backward by a specified distance."""
        self._turtle.backward(distance)

    def left(self, angle: float):
        """Turn the turtle left by a specified angle."""
        self._turtle.left(angle)

    def right(self, angle: float):
        """Turn the turtle right by a specified angle."""
        self._turtle.right(angle)

    def circle(self, radius: float, extent: float=360):
        """Move the turtle in a circle with a specified radius and extent."""
        self._turtle.circle(radius, extent)

    def setheading(self, angle: float):
        """Set the turtle's heading to a specified angle."""
        self._turtle.setheading(angle)

    def setx(self, x: float):
        """Set the turtle's x-coordinate."""
        self._turtle.setx(x)

    def sety(self, y: float):
        """Set the turtle's y-coordinate."""
        self._turtle.sety(y)

    def setposition(self, x: float, y: float):
        """Set the turtle's position to specified x and y coordinates."""
        self._turtle.setposition(x, y)

    def towards(self, x: float, y: float):
        """Calculate the angle towards a specified position."""
        self._turtle.towards(x, y)

    def reset_origin(self):
        """Reset the turtle's origin."""
        # Get the current position and heading
        current_position = self._turtle.pos()
        current_heading = self._turtle.heading()

        # Hide the turtle, move it to (0, 0) in the new origin system
        self.t.hideturtle()

        # Translate the world so that the current position becomes (0, 0)
        self.screen.setworldcoordinates(
            current_position[0],  # New bottom-left X
            current_position[1],  # New bottom-left Y
            current_position[0] + self.screen.window_width(),  # New top-right X
            current_position[1] + self.screen.window_height()  # New top-right Y
        )

        # Reset the heading
        self._turtle.setheading(current_heading)

        # Make the turtle visible again
        self._turtle.showturtle()

    def heading(self) -> float:
        """Get the turtle's current heading."""
        _, self._angle = self._commands_tx.heading()
        return self._angle

    def position(self) -> tuple[float, float]:
        """Get the turtle's current position."""
        self._x, self._y = self._turtle.position()
        return self._x, self._y

    def penup(self):
        """Lift the pen up."""
        self._turtle.penup()

    def pendown(self):
        """Put the pen down."""
        self._turtle.pendown()

    def isdown(self) -> bool:
        """Check if the pen is down."""
        return self._turtle.isdown()
    
    # Methods that are not implemented by the ScreenTurtle class
    
    def connect(self):
        """Connect to the turtle."""
        pass

    def disconnect(self):
        """Disconnect from the turtle."""
        pass

    def eyes(self, eye: int, red: int, green: int, blue: int):
        """Control the turtle's eyes."""
        pass

    def get_axel_distance_calibration(self) -> int:
        """Get the axel distance calibration."""
        return 0.0

    def get_linear_velocity(self) -> tuple[int, int]:
        """Get the turtle's linear velocity."""
        return 0.0, 0.0

    def get_rotational_velocity(self) -> tuple[int, int]:
        """Get the turtle's rotational velocity."""
        return 0.0, 0.0

    def get_turtle_id(self) -> int:
        """Get the turtle's ID."""
        return 0

    def get_wheel_diameter_calibration(self) -> int:
        """Get the wheel diameter calibration."""
        return 0

    def load_config(self):
        """Load the turtle's configuration."""
        pass

    def motors(self, state: bool):
        """Control the turtle's motors."""
        pass

    def power(self) -> tuple[int, int, int]:
        """Return the turtle's power."""
        return 0, 0, 0

    def reset_config(self):
        """Reset the turtle's configuration."""
        pass

    def save_config(self):
        """Save the turtle's configuration."""
        pass

    def set_axel_distance_calibration(self, calibration):
        """Set the axel distance calibration."""
        pass

    def set_linear_velocity(self, velocity):
        """Set the turtle's linear velocity."""
        pass

    def set_rotational_velocity(self, velocity):
        """Set the turtle's rotational velocity."""
        pass

    def set_turtle_id(self, turtle_id):
        """Set the turtle's ID."""
        pass

    def set_wheel_diameter_calibration(self, calibration):
        """Set the wheel diameter calibration."""
        pass