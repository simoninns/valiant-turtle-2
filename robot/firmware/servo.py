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
    def __init__(self, pin):
        self.is_on = False
        self.duty_cycle = 0
        self.degrees = 90

        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.pwm.duty_u16(int(self.duty_cycle))

    def set_power(self, is_on: bool):
        self.is_on = is_on
        if (self.is_on):
            self.pwm.duty_u16(int(self.duty_cycle))
        else:
            self.pwm.duty_u16(0)

    def get_power(self):
        return self.is_on

    def set_position(self, degrees):
        if (degrees > 180): degrees = 180
        if (degrees < 0): degrees = 0
        self.degrees = degrees

        max_duty = 7864 # 180 degrees
        min_duty = 1802 # 0 degrees

        self.duty_cycle = min_duty + (((max_duty - min_duty) / 180) * degrees)

        if (self.is_on): 
            self.pwm.duty_u16(int(self.duty_cycle))

    def get_position(self):
        return self.degrees
    
if __name__ == "__main__":
    from main import main
    main()