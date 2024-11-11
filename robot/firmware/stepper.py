#************************************************************************ 
#
#   stepper.py
#
#   Stepper motor control (via DRV8825)
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

from log import log_debug, log_info, log_warn

from velocity import Velocity
from pulse_generator import Pulse_generator

from machine import Pin

class Stepper:
    _sm_counter = 0 # Keep track of the next free state-machine

    def __init__(self, direction_pin, step_pin, is_left: bool):
        self.pio = 1

        # Configure the direction GPIO
        self.direction = Pin(direction_pin, Pin.OUT)
        self.direction.value(0)

        # Orientation of stepper
        self.is_left = is_left

        # Tracking progress
        self.steps_remaining = 0
        self.is_busy_flag = False
        self.sequence_index = 0

        # Ensure we have a free state-machine
        if Stepper._sm_counter < 4:
            log_info("Stepper::__init__ - Using PIO", self.pio,"SM", Stepper._sm_counter)
        else:
            raise RuntimeError("Stepper::__init__ - No more state machines available!")

        # Initialise the pulse generator on PIO 1
        # Note: This controls the step GPIO
        self.pulse_generator = Pulse_generator(self.pio, Stepper._sm_counter, step_pin)
        Stepper._sm_counter += 1

        # Set up the pulse generator callback
        self.pulse_generator.callback_subscribe(self.callback)

    def set_forwards(self):
        if self.is_left: self.direction.value(1)
        else: self.direction.value(0)

    def set_backwards(self):
        if self.is_left: self.direction.value(0)
        else: self.direction.value(1)

    @property
    def is_busy(self) -> bool:
        return self.is_busy_flag

    def set_velocity(self, velocity: Velocity) -> bool:
        if self.is_busy:
            log_debug("Stepper::set_velocity - Failed... Stepper is busy")
            return False
        
        self.velocity = velocity
        self.sequence_index = 0
        
        # Set the remaining steps
        self.steps_remaining = self.velocity.total_steps

        # Start the pulse generator (updates are via callback)
        self.is_busy_flag = True
        self.pulse_generator.set(self.velocity.sequence_spp[self.sequence_index] * self.velocity.intervals_per_second, self.velocity.sequence_steps[self.sequence_index])
        self.steps_remaining -= self.velocity.sequence_steps[self.sequence_index]

        return True
    
    # Callback when pulse generator needs more sequence information
    def callback(self):
        # Only process the callback if the stepper is currently busy
        if self.is_busy_flag:
            #print("Stepper callback - Steps remaining =", self.steps_remaining)
            self.sequence_index += 1
            if self.sequence_index < len(self.velocity.sequence_steps):
                # Sequence in progress
                self.pulse_generator.set(self.velocity.sequence_spp[self.sequence_index] * self.velocity.intervals_per_second, self.velocity.sequence_steps[self.sequence_index])
                self.steps_remaining -= self.velocity.sequence_steps[self.sequence_index]
            else:
                # Sequence completed
                self.is_busy_flag = False