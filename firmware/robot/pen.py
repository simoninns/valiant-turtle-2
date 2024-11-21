#************************************************************************ 
#
#   pen.py
#
#   Control the pen lift mechanism
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

from servo import Servo
from machine import Pin
import library.logging as logging

class Pen:
    """
    A class to represent a Pen controlled by a servo motor.
    Attributes
    ----------
    servo : Servo
        An instance of the Servo class to control the pen.
    Methods
    -------
    __init__(pin):
        Initializes the Pen with the given servo pin and sets the servo power to off.
    up():
        Raises the pen by setting the servo position to 90 degrees and turning the servo power on.
    down():
        Lowers the pen by setting the servo position to 0 degrees and turning the servo power on.
    off():
        Turns the servo power off.
    """

    def __init__(self, pin: Pin):
        """
        Initializes the Pen object.
        Args:
            pin (Pin): The pin to which the pen servo is connected.
        Initializes the pen servo and sets its power to the off state.
        """

        # Initialise the pen servo to off
        self.servo = Servo(pin)
        self.servo.set_power(False)
        self._is_servo_powered = False
        self._is_servo_up = False

    @property
    def is_servo_up(self) -> bool:
        """
        Returns True if the pen is raised, False otherwise.
        """

        return self._is_servo_up
    
    @property
    def is_servo_powered(self) -> bool:
        """
        Returns True if the servo power is on, False otherwise.
        """

        return self._is_servo_powered

    def up(self):
        """
        Raises the pen by setting the servo position to 90 degrees and turns on the servo power.
        """

        self.servo.set_position(90)
        self.servo.set_power(True)
        self._is_servo_up = True
        self._is_servo_powered = True
        logging.debug("Pen::up - Pen raised")
    
    def down(self):
        """
        Lowers the pen by setting the servo position to 0 degrees and turning on the servo power.
        """

        self.servo.set_position(0)
        self.servo.set_power(True)
        self._is_servo_up = False
        self._is_servo_powered = True
        logging.debug("Pen::down - Pen lowered")

    def off(self):
        """
        Turns off the servo power.
        """

        self.servo.set_power(False)
        self._is_servo_powered = False
        logging.debug("Pen::off - Servo powered off")

if __name__ == "__main__":
    from main import main
    main()