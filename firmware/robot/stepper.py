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
from velocity import Velocity
from pulse_generator import PulseGenerator

from machine import Pin

class Stepper:
    """
    A class to represent a stepper motor controller.
    Attributes
    ----------
    pio : int
        The Programmable I/O (PIO) instance used for the stepper motor.
    direction : Pin
        The GPIO pin used to control the direction of the stepper motor.
    is_left : bool
        Indicates if the stepper motor is oriented to the left.
    _is_forwards : bool
        Indicates if the stepper motor is moving forwards.
    steps_remaining : int
        The number of steps remaining in the current sequence.
    is_busy_flag : bool
        Indicates if the stepper motor is currently busy.
    sequence_index : int
        The current index in the velocity sequence.
    pulse_generator : PulseGenerator
        The pulse generator used to control the step pin of the stepper motor.
    velocity : Velocity
        The velocity profile for the stepper motor.
    Methods
    -------
    __init__(direction_pin, step_pin, is_left: bool):
        Initializes the stepper motor with the given direction and step pins and orientation.
    set_forwards():
        Sets the stepper motor to move forwards.
    set_backwards():
        Sets the stepper motor to move backwards.
    is_busy() -> bool:
        Returns whether the stepper motor is currently busy.
    is_forwards() -> bool:
        Returns whether the stepper motor is moving forwards.
    set_velocity(velocity: Velocity) -> bool:
        Sets the velocity profile for the stepper motor and starts the pulse generator.
    callback():
        Callback function for the pulse generator to provide more sequence information.
    """

    _sm_counter = 0 # Keep track of the next free state-machine

    def __init__(self, direction_pin: int, step_pin: int, is_left: bool):
        """
        Initializes the Stepper object.
        Args:
            direction_pin (int): The GPIO pin number used to control the direction of the stepper motor.
            step_pin (int): The GPIO pin number used to control the steps of the stepper motor.
            is_left (bool): A flag indicating the orientation of the stepper motor.
        Raises:
            RuntimeError: If no more state machines are available.
        """

        self.pio = 0

        # Configure the direction GPIO
        self.direction = Pin(direction_pin, Pin.OUT)
        self.direction.value(0)

        # Orientation of stepper
        self.is_left = is_left

        # Direction of stepper
        self._is_forwards = True
        self.set_forwards()

        # Tracking progress
        self.steps_remaining = 0
        self.is_busy_flag = False
        self.sequence_index = 0

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

    def set_forwards(self):
        """
        Sets the stepper motor to move forwards.
        This method sets the internal flag `_is_forwards` to True and updates the 
        direction of the motor based on whether it is configured as left or right.
        If the motor is on the left, the direction value is set to 1.
        If the motor is on the right, the direction value is set to 0.
        """

        self._is_forwards = True
        if self.is_left: self.direction.value(1)
        else: self.direction.value(0)

    def set_backwards(self):
        """
        Sets the stepper motor to move backwards.
        This method sets the internal flag `_is_forwards` to `False` and updates
        the direction of the motor based on whether it is configured as left or right.
        If the motor is on the left, the direction value is set to 0.
        If the motor is on the right, the direction value is set to 1.
        """

        self._is_forwards = False
        if self.is_left: self.direction.value(0)
        else: self.direction.value(1)

    @property
    def is_busy(self) -> bool:
        """
        Check if the stepper motor is currently busy.
        Returns:
            bool: True if the stepper motor is busy, False otherwise.
        """
        
        return self.is_busy_flag
    
    @property
    def is_forwards(self) -> bool:
        """
        Check if the stepper motor is moving forwards.
        Returns:
            bool: True if the stepper motor is moving forwards, False otherwise.
        """

        return self._is_forwards

    def set_velocity(self, velocity: Velocity) -> bool:
        """
        Sets the velocity of the stepper motor.
        This method configures the stepper motor to run at the specified velocity.
        If the stepper motor is currently busy, the method will log a debug message
        and return False. Otherwise, it will set the velocity, initialize the sequence
        index, and start the pulse generator.
        Args:
            velocity (Velocity): The desired velocity settings for the stepper motor.
        Returns:
            bool: True if the velocity was successfully set, False if the stepper motor is busy.
        """

        if self.is_busy_flag:
            logging.debug("Stepper::set_velocity - Failed... Stepper is busy")
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
        """
        Callback function to handle the stepper motor sequence.
        This function is called to process the stepper motor's movement sequence.
        It increments the sequence index and updates the pulse generator with the
        next step and speed values if the sequence is still in progress. If the
        sequence is completed, it sets the busy flag to False.
        Returns:
            None
        """

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

if __name__ == "__main__":
    from main import main
    main()