#************************************************************************ 
#
#   servo.py
#
#   Control servos using PWM
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

from machine import Pin, PWM

class Servo:
    """
    A class to represent a servo motor controlled via PWM.
    Attributes
    ----------
    is_on : bool
        A flag indicating whether the servo is powered on.
    duty_cycle : float
        The current duty cycle of the PWM signal.
    degrees : float
        The current position of the servo in degrees.
    pwm : PWM
        The PWM object used to control the servo.
    Methods
    -------
    __init__(pin):
        Initializes the servo with the specified pin.
    set_power(is_on: bool):
        Sets the power state of the servo.
    get_power():
        Returns the current power state of the servo.
    set_position(degrees):
        Sets the position of the servo in degrees.
    get_position():
        Returns the current position of the servo in degrees.
    """

    def __init__(self, pin):
        """
        Initializes the Servo object.
        Args:
            pin (int): The GPIO pin number to which the servo is connected.
        Attributes:
            is_on (bool): Indicates whether the servo is currently on.
            duty_cycle (int): The duty cycle of the PWM signal controlling the servo.
            degrees (float): The current angle of the servo in degrees.
            pwm (PWM): The PWM object used to control the servo.
        """

        self.is_on = False
        self.duty_cycle = 4833  # Corresponding duty cycle for 90 degrees
        self.degrees = 90

        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.pwm.duty_u16(int(self.duty_cycle))

    def set_power(self, is_on: bool):
        """
        Sets the power state of the servo.
        Args:
            is_on (bool): If True, turns the servo on by setting the PWM duty cycle to the current duty cycle value.
                          If False, turns the servo off by setting the PWM duty cycle to 0.
        """

        self.is_on = is_on
        if self.is_on:
            self.pwm.duty_u16(int(self.duty_cycle))
        else:
            self.pwm.duty_u16(0)

    def get_power(self) -> bool:
        """
        Check if the servo is powered on.
        Returns:
            bool: True if the servo is on, False otherwise.
        """

        return self.is_on

    def set_position(self, degrees: float):
        """
        Sets the position of the servo motor to the specified angle in degrees.
        Args:
            degrees (float): The desired angle in degrees. Must be between 0 and 180.
                             Values outside this range will be clamped to the nearest limit.
        Sets:
            self.degrees (float): The clamped angle in degrees.
            self.duty_cycle (float): The calculated duty cycle corresponding to the angle.
        If the servo motor is on, updates the PWM duty cycle to move the servo to the specified position.
        """

        if (degrees > 180): degrees = 180
        if (degrees < 0): degrees = 0
        self.degrees = degrees

        max_duty = 7864 # 180 degrees
        min_duty = 1802 # 0 degrees

        self.duty_cycle = min_duty + (((max_duty - min_duty) / 180) * degrees)

        if (self.is_on): 
            self.pwm.duty_u16(int(self.duty_cycle))

    def get_position(self) -> float:
        """
        Get the current position of the servo in degrees.
        Returns:
            float: The current position of the servo in degrees.
        """

        return self.degrees
    
if __name__ == "__main__":
    from main import main
    main()