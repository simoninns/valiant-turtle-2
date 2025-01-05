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

import picolog
from pulse_generator import PulseGenerator
from drv8825 import Drv8825

from machine import Pin

class Stepper:
    _sm_counter = 0 # Keep track of the next free state-machine
    test_only = False # Set to True to test the acceleration sequence without moving the stepper

    def __init__(self, drv8825: Drv8825, step_pin: Pin, direction_pin: Pin, is_left: bool):
        self.pio = 0

        # Configure the stepper motor direction
        self._is_left = is_left
        self._direction_pin = direction_pin
        self.set_direction_forwards()

        # Stepper busy flag
        self._is_busy = False
        self._direction = True # True = forwards, False = backwards

        # Stepper motion parameters (in steps per interval)
        self._target_speed_spi = 1
        self._acceleration_spi = 1
        self._steps_remaining = 0
        self._current_speed_spi = 1

        # Tracking parameters
        self._acceleration_steps = 0
        self._running_steps = 0
        self._track_actual_steps = 0

        # The number of speed re-calculations per second
        self._intervals_per_second = 16

        # Temporary acceleration and target speed values in case
        # we need to adjust them for a single move
        self._actual_acceleration_spi = self._acceleration_spi
        self._actual_target_speed_spi = self._target_speed_spi

        # Ensure we have a free state-machine
        if Stepper._sm_counter < 4:
            if self._is_left:
                picolog.debug(f"Stepper::__init__ - Left stepper pulse generator using PIO {self.pio} SM {Stepper._sm_counter}")
            else:
                picolog.debug(f"Stepper::__init__ - Right stepper pulse generator using PIO {self.pio} SM {Stepper._sm_counter}")
        else:
            raise RuntimeError("Stepper::__init__ - No more state machines available!")

        # Initialise the pulse generator on PIO 1
        # Note: This controls the step GPIO
        self._state_machine = Stepper._sm_counter
        Stepper._sm_counter += 1
        self.pulse_generator = PulseGenerator(self.pio, self._state_machine, step_pin)
        
        # Set up the pulse generator callback
        self.pulse_generator.callback_subscribe(self.callback)

    @property
    def is_busy(self):
        return self._is_busy
    
    @property
    def direction(self):
        return self._direction
    
    def set_direction_forwards(self):
        if self._is_left:
            self._direction_pin.value(1)
        else:
            self._direction_pin.value(0)
        self._direction = True

    def set_direction_backwards(self):
        if self._is_left:
            self._direction_pin.value(0)
        else:
            self._direction_pin.value(1)
        self._direction = False

    def set_direction_left(self):
        if self._is_left:
            self._direction_pin.value(1)
        else:
            self._direction_pin.value(1)
        if self._is_left: 
            self._direction = True
        else:
            self._direction = False

    def set_direction_right(self):
        if self._is_left:
            self._direction_pin.value(0)
        else:
            self._direction_pin.value(0)
        if self._is_left: 
            self._direction = False
        else:
            self._direction = True

    def set_acceleration_spsps(self, acceleration: float):
        """Set the acceleration in steps per second per second"""
        if acceleration < 1:
            raise ValueError("Stepper::set_acceleration - Acceleration must be greater than 0")
        self._acceleration_spi = acceleration / self._intervals_per_second
        picolog.debug(f"Stepper::set_acceleration - Acceleration set to {acceleration} steps per second per second ({self._acceleration_spi} steps per interval per interval)")

    def set_target_speed_sps(self, target_speed: float):
        """Set the target speed in steps per second"""
        if target_speed < 1:
            raise ValueError("Stepper::set_target_speed - Speed must be greater than 0")
        self._target_speed_spi = target_speed / self._intervals_per_second
        picolog.debug(f"Stepper::set_target_speed - Target speed set to {target_speed} steps per second ({self._target_speed_spi} steps per interval)")

    def move(self, steps: float):
        # Check if the stepper is currently busy
        if self._is_busy:
            raise RuntimeError("Stepper::move - Stepper is currently busy")
        
        if (steps == 0):
            picolog.debug("Stepper::move - Steps must be greater than 0 - not moving")
            return

        # Set the stepper as busy
        self._is_busy = True

        picolog.debug(f"Stepper::move - Moving {steps} steps using {self._intervals_per_second} calculation intervals per second")
        picolog.debug(f"Stepper::move - Maximum acceleration is {self._acceleration_spi} steps per interval and target speed is {self._target_speed_spi} steps per interval")

        self._total_steps = steps
        self._steps_remaining = self._total_steps
        self._current_speed_spi = 0
        self._maximum_available_acceleration_steps = self._total_steps / 2
        one_shot = False
        self._partial_steps = 0
        self._track_actual_steps = 0

        # Save the initial acceleration and target speed in case we need to adjust them
        self._actual_acceleration_spi = self._acceleration_spi
        self._actual_target_speed_spi = self._target_speed_spi

        # Ensure that we have enough steps to accelerate
        if self._total_steps < (2 * self._actual_acceleration_spi):
            if (self._total_steps / 2) >= 1:
                self._actual_acceleration_spi = int(self._total_steps / 2)
                picolog.debug(f"Stepper::move - Adjusting acceleration to {self._actual_acceleration_spi} steps per interval")
            else:
                picolog.debug("Stepper::move - Cannot accelerate: Steps must be greater than or equal to 2")
                one_shot = True
        
        # Range check and adjust the target speed if necessary
        if (self._actual_target_speed_spi <= self._actual_acceleration_spi):
            self._actual_target_speed_spi = self._actual_acceleration_spi
            picolog.debug(f"Stepper::move - Adjusting target speed to {self._actual_target_speed_spi} steps per interval")
        
        if (self._total_steps < self._actual_target_speed_spi):
            self._actual_target_speed_spi = self._total_steps
            picolog.debug(f"Stepper::move - Adjusting target speed to {self._actual_target_speed_spi} steps per interval")

        if one_shot:
            # One-shot move
            picolog.debug(f"Stepper::move - Performing one-shot move of {self._total_steps} steps at {self._intervals_per_second} steps per second)")
            if not Stepper.test_only:
                # Move at a low speed during a one-shot move
                self.pulse_generator.set(self._intervals_per_second, int(round(self._total_steps, 0)))
                self._steps_remaining = 0
                self._track_actual_steps = self._total_steps
        else:
            # Acceleration and deceleration move
            picolog.debug(f"Stepper::move - Beginning initial acceleration on SM {self._state_machine}")
            if not Stepper.test_only:
                self.calculate_next_command()
            else:
                # Just test the acceleration sequence
                self._is_busy = True
                while self._steps_remaining > 0:
                    self.calculate_next_command()
                
                if self._total_steps == self._track_actual_steps:
                    picolog.debug(f"Stepper::move - Acceleration/deceleration sequence completed successfully on SM {self._state_machine}")
                else:
                    picolog.error(f"Stepper::move - Acceleration/deceleration sequence failed on SM {self._state_machine} expected {self._total_steps} steps, performed {self._track_actual_steps} steps")
                self._is_busy = False

    def calculate_next_command(self):
        steps = 0
        speed = 0

        # Accelerating?
        if (self._steps_remaining - self._current_speed_spi) > self._maximum_available_acceleration_steps and (self._current_speed_spi + self._actual_acceleration_spi) < self._actual_target_speed_spi:
            self._current_speed_spi += self._actual_acceleration_spi
            if (self._current_speed_spi > self._actual_target_speed_spi):
                self._current_speed_spi = self._actual_target_speed_spi
            self._steps_remaining -= self._current_speed_spi
            if Stepper.test_only: picolog.debug(f"Stepper::calculate_next_command - Accelerating - Current SPI = {self._current_speed_spi}, steps remaining = {self._steps_remaining}")
            steps = self._current_speed_spi
            speed = self._current_speed_spi

            self._acceleration_steps = self._total_steps - self._steps_remaining
            self._running_steps = self._total_steps - (2 * self._acceleration_steps)
            self._final_acceleration_speed = self._current_speed_spi
        elif (self._steps_remaining > self._acceleration_steps):
            if Stepper.test_only: picolog.debug(f"Stepper::calculate_next_command - Acceleration steps = {self._acceleration_steps}")

            # If acceleration didn't reach target speed, accelerate one more time
            self._current_speed_spi += self._actual_acceleration_spi
            if (self._current_speed_spi > self._actual_target_speed_spi):
                self._current_speed_spi = self._actual_target_speed_spi

            self._steps_remaining -= self._running_steps
            if Stepper.test_only: picolog.debug(f"Stepper::calculate_next_command - Running - Current speed = {self._current_speed_spi}, running steps = {self._running_steps}")
            steps = self._running_steps
            speed = self._current_speed_spi

            # Adjust back to the final acceleration speed to ensure we decelerate correctly
            self._current_speed_spi = self._final_acceleration_speed
        else:
            self._steps_remaining -= self._current_speed_spi
            if Stepper.test_only: picolog.debug(f"Stepper::calculate_next_command - Decelerating - Current speed = {self._current_speed_spi}, steps remaining = {self._steps_remaining}")
            steps = self._current_speed_spi
            speed = self._current_speed_spi

            self._current_speed_spi -= self._actual_acceleration_spi
            if (self._current_speed_spi < 1):
                self._current_speed_spi = 1

        # Deal with a fractional number of steps
        whole_steps = int(steps)
        self._partial_steps += steps - whole_steps
        steps = whole_steps

        # If we have a fractional number of steps greater than 1, add them to the next command
        if self._partial_steps >= 1:
            additional_steps = int(self._partial_steps)
            self._partial_steps -= additional_steps
            steps += additional_steps

        if Stepper.test_only: picolog.debug(f"Stepper::calculate_next_command - Steps = {steps}, Partial steps = {self._partial_steps}")

        # Set the pulse generator
        self._track_actual_steps += steps
        if Stepper.test_only: picolog.debug(f"Stepper::calculate_next_command - Command result: Steps per second = {speed * self._intervals_per_second} ({speed} SPI), Steps = {steps}, Position = {self._track_actual_steps}")
        if not Stepper.test_only: self.pulse_generator.set(int(speed * self._intervals_per_second), steps)

    # Callback when pulse generator needs more sequence information
    def callback(self):
        # Only process the callback if the stepper is currently busy
        if self._steps_remaining > 0:       
            self.calculate_next_command()
        else:
            self._is_busy = False
            error_margin = self._total_steps - self._track_actual_steps
            if int(error_margin) == 0:
                picolog.debug(f"Stepper::callback - Acc/dec completed successfully on SM {self._state_machine} error margin was {error_margin} steps")
            else:
                picolog.error(f"Stepper::callback - Acc/dec completed failed on SM {self._state_machine} error margin was >1 step ({error_margin} steps)")

if __name__ == "__main__":
    from main import main
    main()