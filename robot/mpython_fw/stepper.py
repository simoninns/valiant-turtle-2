#************************************************************************ 
#
#   stepper.py
#
#   Stepper motor control (via DRV8825)
#   Valiant Turtle 2 - Raspberry Pi Pico W Firmware
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

from log import log_debug
from log import log_info
from log import log_warn

from velocity import Velocity

from machine import Pin

class Stepper:
    def __init__(self, direction_pin, step_pin, is_left: bool):
        # Configure the GPIOs
        self.direction = Pin(direction_pin, Pin.OUT)
        self.step = Pin(step_pin, Pin.OUT)
        self.direction.value(0)
        self.step.value(0)

        # Orientation of stepper
        self.is_left = is_left

        # Tracking progress
        self.steps_remaining = 0
        self.is_busy = False

    def set_forwards(self):
        if self.is_left: self.direction.value(0)
        else: self.direction.value(1)

    def set_backwards(self):
        if self.is_left: self.direction.value(1)
        else: self.direction.value(0)

    def set_velocity(self, velocity: Velocity) -> bool:
        if self.is_busy:
            log_debug("Stepper::set_velocity - Failed... Stepper is busy")
            return False
        
        # Set the remaining steps
        self.steps_remaining = velocity.total_steps

        return True
        
