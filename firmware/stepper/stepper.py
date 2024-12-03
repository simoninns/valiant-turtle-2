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

import library.logging as logging
from pulse_generator import PulseGenerator
from drv8825 import Drv8825

from machine import Pin

class Stepper:
    _sm_counter = 0 # Keep track of the next free state-machine

    def __init__(self, drv8825: Drv8825, step_pin: Pin, direction_pin: Pin, is_left: bool):
        self.pio = 0

        # Configure the stepper motor direction
        self._direction_pin = direction_pin
        self._is_forwards = True
        self._is_left = is_left
        self.set_direction_forwards()

        # Stepper busy flag
        self._is_busy = False

        # Stepper motion parameters
        self._target_speed_sps = 1
        self._acceleration_sps = 1
        self._steps_remaining = 0
        self._current_speed_sps = 1

        # Tracking parameters
        self._acceleration_steps = 0
        self._running_steps = 0
        self._deceleration_steps = 0

        # Ensure we have a free state-machine
        if Stepper._sm_counter < 4:
            logging.debug(f"Stepper::__init__ - Using PIO {self.pio} SM {Stepper._sm_counter}")
        else:
            raise RuntimeError("Stepper::__init__ - No more state machines available!")

        # Initialise the pulse generator on PIO 1
        # Note: This controls the step GPIO
        self.pulse_generator = PulseGenerator(self.pio, Stepper._sm_counter, step_pin)
        Stepper._sm_counter += 1

        # Set up the pulse generator callback
        self.pulse_generator.callback_subscribe(self.callback)

    @property
    def is_busy(self):
        return self._is_busy

    def set_direction_forwards(self):
        if self._is_left:
            self._direction_pin.value(0)
        else:
            self._direction_pin.value(1)
        self._is_forwards = True

    def set_direction_backwards(self):
        if self._is_left:
            self._direction_pin.value(1)
        else:
            self._direction_pin.value(0)
        self._is_forwards = False

    def set_acceleration(self, acceleration: int):
        if acceleration < 1:
            raise ValueError("Stepper::set_acceleration - Acceleration must be greater than 0")
        self._acceleration_sps = acceleration
        logging.debug(f"Stepper::set_acceleration - Acceleration set to {acceleration}")

    def set_target_speed(self, target_speed: int):
        if target_speed < 1:
            raise ValueError("Stepper::set_target_speed - Speed must be greater than 0")
        self._target_speed_sps = target_speed
        logging.debug(f"Stepper::set_target_speed - Target speed set to {target_speed}")

    def move(self, steps: int):
        # Check if the stepper is currently busy
        if self._is_busy:
            raise RuntimeError("Stepper::move - Stepper is currently busy")
        
        if (steps < 1):
            raise ValueError("Stepper::move - Steps must be greater than 0")

        # Set the stepper as busy
        self._is_busy = True

        logging.debug(f"Stepper::move - Moving {steps} steps")
        logging.debug(f"Stepper::move - Maximum acceleration is {self._acceleration_sps} steps per second and target speed is {self._target_speed_sps} steps per second")

        self._total_steps = steps
        self._steps_remaining = self._total_steps
        self._current_speed_sps = 0
        self._maximum_available_acceleration_steps = self._total_steps / 2
        one_shot = False

        # Check the input parameters and decide if acceleration is required
        if self._total_steps < (2 * self._acceleration_sps):
            logging.debug("Stepper::move - Cannot accelerate: Steps must be greater than or equal to twice the acceleration rate")
            one_shot = True
        
        if (self._target_speed_sps <= self._acceleration_sps):
            logging.debug("Stepper::move - Cannot accelerate: Target speed must be greater than the acceleration rate")
            one_shot = True
        
        if (self._total_steps < self._target_speed_sps):
            logging.debug("Stepper::move - Cannot accelerate: Steps must be greater than or equal to the target speed")
            one_shot = True

        if one_shot:
            # One-shot move
            self.pulse_generator.set(self._target_speed_sps, self._total_steps)
        else:
            # Acceleration and deceleration move
            self.calculate_next_command()

    def calculate_next_command(self):
        steps = 0
        speed = 0

        # Accelerating?
        if (self._steps_remaining - self._current_speed_sps) > self._maximum_available_acceleration_steps and (self._current_speed_sps + self._acceleration_sps) < self._target_speed_sps:
            self._current_speed_sps += self._acceleration_sps
            if (self._current_speed_sps > self._target_speed_sps):
                self._current_speed_sps = self._target_speed_sps
            self._steps_remaining -= self._current_speed_sps
            logging.debug(f"Stepper::calculate_next_command - Accelerating - Current speed = {self._current_speed_sps}, steps remaining = {self._steps_remaining}")
            steps = self._current_speed_sps
            speed = self._current_speed_sps

            self._acceleration_steps = self._total_steps - self._steps_remaining
            self._running_steps = self._total_steps - (2 * self._acceleration_steps)
            self._final_acceleration_speed = self._current_speed_sps
        elif (self._steps_remaining > self._acceleration_steps):
            logging.debug(f"Stepper::calculate_next_command - Acceleration steps = {self._acceleration_steps}")

            # If acceleration didn't reach target speed, accelerate one more time
            self._current_speed_sps += self._acceleration_sps
            if (self._current_speed_sps > self._target_speed_sps):
                self._current_speed_sps = self._target_speed_sps

            self._steps_remaining -= self._running_steps
            logging.debug(f"Stepper::calculate_next_command - Running - Current speed = {self._current_speed_sps}, running steps = {self._running_steps}")
            steps = self._running_steps
            speed = self._current_speed_sps

            # Adjust back to the final acceleration speed to ensure we decelerate correctly
            self._current_speed_sps = self._final_acceleration_speed
        else:
            self._steps_remaining -= self._current_speed_sps
            logging.debug(f"Stepper::calculate_next_command - Decelerating - Current speed = {self._current_speed_sps}, steps remaining = {self._steps_remaining}")
            steps = self._current_speed_sps
            speed = self._current_speed_sps

            self._current_speed_sps -= self._acceleration_sps
            if (self._current_speed_sps < 1):
                self._current_speed_sps = 1

        # Set the pulse generator
        logging.debug(f"Stepper::calculate_next_command - Command result: Speed = {speed}, Steps = {steps}")
        self.pulse_generator.set(speed, steps)

    # Callback when pulse generator needs more sequence information
    def callback(self):
        # Only process the callback if the stepper is currently busy
        if self._steps_remaining > 0:       
            self.calculate_next_command()
        else:
            self._is_busy = False
            logging.debug("Stepper::callback - Sequence completed")

if __name__ == "__main__":
    from main import main
    main()