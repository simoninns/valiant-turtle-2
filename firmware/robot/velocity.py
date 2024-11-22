#************************************************************************ 
#
#   velocity.py
#
#   Stepper motor velocity calculations
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

class VelocityParameters:
    """
    A class to represent the velocity parameters for a stepper motor.
    Attributes
    ----------
    acc_spsps : int
        Acceleration in Steps Per Second Per Second.
    minimum_sps : int
        Minimum Steps Per Second.
    maximum_sps : int
        Maximum Steps Per Second.
    intervals_per_second : int
        Number of intervals per second.
    Methods
    -------
    """

    def __init__(self, acc_spsps: int, minimum_sps: int, maximum_sps: int, intervals_per_second: int):
        # Range check input parameters
        if acc_spsps < 1:
            logging.info("VelocityParameters::__init__ - Acceleration in Steps Per Second Per Second must be greater than 0")
            acc_spsps = 1
        
        if minimum_sps < 1:
            logging.info("VelocityParameters::__init__ - Minimum Steps Per Second must be greater than 0")
            minimum_sps = 1

        # There must be at least one step per interval minimum
        if minimum_sps <= intervals_per_second:
            logging.info("VelocityParameters::__init__ - Minimum Steps Per Second must be equal or greater than intervals per second")
            minimum_sps = intervals_per_second

        if maximum_sps < 1:
            logging.info("VelocityParameters::__init__ - Maximum Steps Per Second must be greater than 0")
            maximum_sps = 1

        if maximum_sps < acc_spsps:
            logging.info("VelocityParameters::__init__ - Maximum Steps Per Second less than acceleration in Steps Per Second Per Second")
            maximum_sps = acc_spsps

        if maximum_sps <= minimum_sps:
            logging.info("VelocityParameters::__init__ - Maximum Steps Per Second must be equal or greater than minimum Steps Per Second")
            maximum_sps = minimum_sps

        # Store the parameters
        self._acc_spsps = acc_spsps
        self._minimum_sps = minimum_sps
        self._maximum_sps = maximum_sps
        self._intervals_per_second = intervals_per_second

    @property
    def acc_spsps(self) -> int:
        """
        Get the acceleration in Steps Per Second Per Second.
        Returns:
            int: The acceleration in Steps Per Second Per Second.
        """

        return self._acc_spsps
    
    @acc_spsps.setter
    def acc_spsps(self, value: int):
        """
        Set the acceleration in Steps Per Second Per Second.
        Parameters:
            value (int): The acceleration in Steps Per Second Per Second.
        Raises:
            ValueError: If the value is less than 1.
        """

        if value < 1:
            raise ValueError("VelocityParameters::acc_spsps - acceleration in Steps Per Second Per Second must be greater than 0")

        self._acc_spsps = value

    @property
    def minimum_sps(self) -> int:
        """
        Get the minimum Steps Per Second.
        Returns:
            int: The minimum Steps Per Second.
        """
        return self._minimum_sps

    @minimum_sps.setter
    def minimum_sps(self, value: int):
        """
        Set the minimum Steps Per Second.
        Parameters:
            value (int): The minimum Steps Per Second.
        Raises:
            ValueError: If the value is less than 1.
        """
        if value < 1:
            raise ValueError("VelocityParameters::minimum_sps - Minimum Steps Per Second must be greater than 0")
        self._minimum_sps = value

    @property
    def maximum_sps(self) -> int:
        """
        Get the maximum Steps Per Second.
        Returns:
            int: The maximum Steps Per Second.
        """
        return self._maximum_sps

    @maximum_sps.setter
    def maximum_sps(self, value: int):
        """
        Set the maximum Steps Per Second.
        Parameters:
            value (int): The maximum Steps Per Second.
        Raises:
            ValueError: If the value is less than 1 or less than acceleration.
        """
        if value < 1:
            raise ValueError("VelocityParameters::maximum_sps - Maximum Steps Per Second must be greater than 0")
        if value < self._acc_spsps:
            raise ValueError("VelocityParameters::maximum_sps - Maximum Steps Per Second less than acceleration in Steps Per Second Per Second")
        self._maximum_sps = value

    @property
    def intervals_per_second(self) -> int:
        """
        Get the number of intervals per second.
        Returns:
            int: The number of intervals per second.
        """
        return self._intervals_per_second

    @intervals_per_second.setter
    def intervals_per_second(self, value: int):
        """
        Set the number of intervals per second.
        Parameters:
            value (int): The number of intervals per second.
        Raises:
            ValueError: If the value is less than 1.
        """
        if value < 1:
            raise ValueError("VelocityParameters::intervals_per_second - Number of intervals per second must be greater than 0")
        self._intervals_per_second = value

    def __str__(self) -> str:
        """
        Return a string representation of the velocity parameters.
        Returns:
            str: A string representation of the velocity parameters.
        """
        return f"acc_spsps = {self._acc_spsps}, minimum_sps = {self._minimum_sps}, maximum_sps = {self._maximum_sps}, intervals_per_second = {self._intervals_per_second}"

class Velocity:
    """
    The Velocity class is responsible for calculating and managing the velocity sequence for a stepper motor.
    It takes into account acceleration, running, and deceleration phases to generate a sequence of steps and speeds.
    Attributes:
        FULL_DEBUG (bool): Set to True to enable full debug output from the velocity calculations.
    Methods:
        __init__(total_steps: int, parameters: VelocityParameters):
            Initializes the Velocity instance with the given total steps and velocity parameters.
        total_steps() -> int:
        length() -> int:
    """

    # Set to True to enable full debug output from the velocity calculations
    FULL_DEBUG = True

    def __init__(self, total_steps: int, parameters: VelocityParameters):
        self._parameters = parameters

        # Initialise lists to hold the velocity sequence
        self.sequence_steps = [] # Number of steps in this period
        self.sequence_spi = [] # Rotational speed in steps per period (for this period)

        # Range check the number of steps
        if total_steps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - The number of required steps must be greater than 0")
        
        # Convert the velocity parameters to per interval rather than per second
        self._acc_spipi: int = int(parameters.acc_spsps / parameters.intervals_per_second) # acceleration in steps per interval per interval
        self._minimum_spi: int = int(parameters.minimum_sps / parameters.intervals_per_second) # minimum speed in steps per interval
        self._maximum_spi: int = int(parameters.maximum_sps / parameters.intervals_per_second) # maximum speed in steps per interval
        self._intervals_per_second: int = parameters.intervals_per_second

        # Range check the interval parameters
        if self._acc_spipi < 1: self._acc_spipi = 1
        if self._minimum_spi < 1: self._minimum_spi = 1
        if self._maximum_spi < 1: self._maximum_spi = 1
        if self._intervals_per_second < 1: self._intervals_per_second = 1

        # Show some debug
        logging.debug(f"Velocity::__init__ - Total required steps = {total_steps}")
        logging.debug(f"Velocity::__init__ - Maximum allowed velocity = {self._parameters.maximum_sps} steps per second")
        logging.debug("Velocity::__init__")
        logging.debug(f"Velocity::__init__ - Acceleration in steps per interval per interval = {self._acc_spipi}")
        logging.debug(f"Velocity::__init__ - Minimum steps per interval = {self._minimum_spi}")
        logging.debug(f"Velocity::__init__ - Maximum steps per interval = {self._maximum_spi}")
        logging.debug(f"Velocity::__init__ - Intervals per second = {self._intervals_per_second}")
        if Velocity.FULL_DEBUG: logging.debug("Velocity::__init__")

        # Before calculating the actual sequence, we make a base assumption
        # that acceleration can use a maximum of 40% of the total required steps
        # (and that deceleration is a mirror of acceleration):
        acc_stepsf: float = (float(total_steps) / 100.0) * 40.0 # 40%
        run_stepsf: float = (float(total_steps) / 100.0) * 20.0 # 20%
        dec_stepsf: float = (float(total_steps) / 100.0) * 40.0 # 40%
        acc_steps: int = int(acc_stepsf)
        run_steps: int = int(run_stepsf)
        dec_steps: int = int(dec_stepsf)

        # Calculate any error due to division rounding and add it to the runSteps
        diff_steps: int = total_steps - acc_steps - run_steps - dec_steps
        run_steps += diff_steps

        if Velocity.FULL_DEBUG:
            logging.debug("Velocity::__init__ - Steps per stage prediction:")
            logging.debug(f"Velocity::__init__ -  ACC steps = {acc_steps}")
            logging.debug(f"Velocity::__init__ -  RUN steps = {run_steps}")
            logging.debug(f"Velocity::__init__ -  DEC steps = {dec_steps}")
            logging.debug("Velocity::__init__")
        
        # Track the current overall step position
        current_step_position: int = 0

        # Accelerate stepper
        if acc_steps > 0:
            while (current_step_position + self._acc_spipi) < acc_steps:
                temp_steps: int = 0
                temp_spi: int = 0

                # Accelerate and check for overflow
                if len(self.sequence_steps) == 0: temp_spi = self._minimum_spi
                else: temp_spi = self.sequence_spi[-1] + self._acc_spipi
                if temp_spi > self._maximum_spi: temp_spi = self._maximum_spi
                temp_steps = temp_spi # When accelerating Steps and SPI (steps per interval) are the same

                # Store the result in the dynamic sequence array
                self.sequence_spi.append(temp_spi)
                self.sequence_steps.append(temp_steps)
                current_step_position += temp_steps

                # Show the result for this sequence part
                if Velocity.FULL_DEBUG:
                    logging.debug(f"Velocity::__init__ - ACC [{len(self.sequence_steps)}] ({current_step_position}) Steps = {self.sequence_steps[-1]} - SPI = {self.sequence_spi[-1]}")

            # Count the number of steps in the generated acceleration sequence
            acc_steps = sum(self.sequence_steps)
            dec_steps = acc_steps
            run_steps = total_steps - acc_steps - dec_steps       

            logging.debug("Velocity::__init__")
            logging.debug("Velocity::__init__ - Steps per stage actual:")
            logging.debug(f"Velocity::__init__ -  ACC steps = {acc_steps}")
            logging.debug(f"Velocity::__init__ -  RUN steps = {run_steps}")
            logging.debug(f"Velocity::__init__ -  DEC steps = {dec_steps}")
            if Velocity.FULL_DEBUG: logging.debug("Velocity::__init__")

        # Run stepper
        temp_steps: int = 0
        temp_spi: int = 0

        # This is a single sequence part to perform the all the run steps
        temp_steps = run_steps
        current_step_position += run_steps

        # Check that the sequence has contents
        if len(self.sequence_spi) > 0:
            # If we have headroom, we can accelerate once more for the run steps
            if (self.sequence_spi[-1] + self._acc_spipi) < self._maximum_spi:
                temp_spi = self.sequence_spi[-1] + self._acc_spipi
                if temp_spi > self._maximum_spi: temp_spi = self._maximum_spi
            else:
                # Run at full speed
                temp_spi = self._maximum_spi
        else:
            # There were no acceleration steps... use minimum acceleration as SPI
            temp_spi = self._acc_spipi
        
        # Store the RUN result in the dynamic sequence array
        self.sequence_spi.append(temp_spi)
        self.sequence_steps.append(temp_steps)

        # Show the result for this sequence part
        if Velocity.FULL_DEBUG:
            logging.debug(f"Velocity::__init__ - RUN [{len(self.sequence_steps)}] ({current_step_position}) Steps = {self.sequence_steps[-1]} - SPI = {self.sequence_spi[-1]}")

        logging.debug(f"Velocity::__init__ - Maximum achieved RUN speed = {self.sequence_spi[-1] * self._intervals_per_second} Steps per second")
        logging.debug("Velocity::__init__")

        # Decelerate stepper
        # (This simply copies the acceleration sequence in reverse)
        if dec_steps > 0:
            for i in range(len(self.sequence_steps) - 1, 0, -1):
                self.sequence_spi.append(self.sequence_spi[i-1])
                self.sequence_steps.append(self.sequence_steps[i-1])

                # Keep track of our current position
                current_step_position += self.sequence_steps[i-1]

                # Show the result for this sequence part
                if Velocity.FULL_DEBUG:
                    logging.debug(f"Velocity::__init__ - DEC [{len(self.sequence_steps)}] ({current_step_position}) Steps = {self.sequence_steps[-1]} - SPI = {self.sequence_spi[-1]}")
                
        # Count the number of steps in the generated acceleration sequence
        if Velocity.FULL_DEBUG: logging.debug("Velocity::__init__")
        logging.debug(f"Velocity::__init__ - Total number of steps = {sum(self.sequence_steps)}")

    # Return the total number of steps in the velocity sequence
    @property
    def total_steps(self) -> int:
        """
        Calculate the total number of steps in the sequence.
        Returns:
            int: The sum of all steps in the sequence.
        """

        return sum(self.sequence_steps)
    
    # Return the length of the velocity sequence
    @property
    def length(self) -> int:
        """
        Calculate the length of the sequence steps.
        Returns:
            int: The length of the sequence steps.
        """

        return len(self.sequence_steps) # Both steps and spp are the same length
    
    # Return the velocity parameters
    @property
    def parameters(self) -> VelocityParameters:
        """
        Get the velocity parameters.
        Returns:
            VelocityParameters: The velocity parameters.
        """

        return self._parameters

if __name__ == "__main__":
    from main import main
    main()