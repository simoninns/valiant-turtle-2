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
        """
        Initialize the VelocityParameters object with the given parameters.
        Parameters:
        acc_spsps (int): Acceleration in Steps Per Second Per Second.
        minimum_sps (int): Minimum Steps Per Second.
        maximum_sps (int): Maximum Steps Per Second.
        intervals_per_second (int): Number of intervals per second.
        Raises:
        ValueError: If any of the input parameters are invalid.
        This method initializes the velocity parameters with the given values.
        """

        # Range check input parameters
        if acc_spsps < 1:
            raise ValueError("VelocityParameters::__init__ - acceleration in Steps Per Second Per Second must be greater than 0")

        if minimum_sps < 1:
            raise ValueError("VelocityParameters::__init__ - Minimum Steps Per Second must be greater than 0")

        if maximum_sps < 1:
            raise ValueError("VelocityParameters::__init__ - Maximum Steps Per Second must be greater than 0")

        if maximum_sps < acc_spsps:
            raise ValueError("VelocityParameters::__init__ - Maximum Steps Per Second less than acceleration in Steps Per Second Per Second")

        if maximum_sps < minimum_sps:
            raise ValueError("VelocityParameters::__init__ - Maximum Steps Per Second must be greater than minimum Steps Per Second")

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
    FULL_DEBUG = False

    def __init__(self, total_steps: int, parameters: VelocityParameters):
        # Store the parameters
        self._parameters = parameters

        # Initialise lists to hold the velocity sequence
        self.sequence_steps = [] # Number of steps in this period
        self.sequence_spp = [] # Rotational speed in steps per period (for this period)

        # Range check the number of steps
        if total_steps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - The number of required steps must be greater than 0")

        # Show some debug
        logging.debug(f"Velocity::__init__ - Total steps = {total_steps}")
        logging.debug(f"Velocity::__init__ - Acceleration in steps per second per second = {self._parameters.acc_spsps}")
        logging.debug(f"Velocity::__init__ - Minimum steps per second = {self._parameters.minimum_sps}")
        logging.debug(f"Velocity::__init__ - Maximum steps per second = {self._parameters.maximum_sps}")
        logging.debug(f"Velocity::__init__ - Intervals per second = {self._parameters.intervals_per_second}")
        if Velocity.FULL_DEBUG: logging.debug("Velocity::__init__")

        acc_spppp: int = int(self._parameters.acc_spsps / self._parameters.intervals_per_second) # acceleration in steps per period per period
        maximum_spp: int = int(self._parameters.maximum_sps / self._parameters.intervals_per_second) # maximum speed in steps per period
        minimum_spp: int = int(self._parameters.minimum_sps / self._parameters.intervals_per_second) # minimum speed in steps per period
        if acc_spppp < 1: acc_spppp = 1
        if maximum_spp < 1: maximum_spp = 1
        if minimum_spp < 1: minimum_spp = 1

        if Velocity.FULL_DEBUG:
            logging.debug(f"Velocity::__init__ - Acceleration in steps per period per period = {acc_spppp}")
            logging.debug(f"Velocity::__init__ - Minimum steps per period = {minimum_spp}")
            logging.debug(f"Velocity::__init__ - Maximum steps per period = {maximum_spp}")
            logging.debug("Velocity::__init__")

        # Before calculating the actual sequence, we make a base assumption
        # that acceleration can use a maximum of 40% of the total required steps
        # (and that deceleration is a mirror of acceleration):
        acc_stepsf: float = (float(total_steps) / 100.0) * 40.0 # 40%
        run_stepsf: float = (float(total_steps) / 100.0) * 20.0 # 20%
        dec_stepsf: float = (float(total_steps) / 100.0) * 40.0 # 40%
        acc_steps: int = int(acc_stepsf)
        run_steps: int = int(run_stepsf)
        dec_steps: int = int(dec_stepsf)

        if Velocity.FULL_DEBUG:
            logging.debug("Velocity::__init__ - Steps per stage prediction:")
            logging.debug(f"Velocity::__init__ -  ACC steps = {acc_steps}")
            logging.debug(f"Velocity::__init__ -  RUN steps = {run_steps}")
            logging.debug(f"Velocity::__init__ -  DEC steps = {dec_steps}")
            logging.debug("Velocity::__init__")

        # Calculate any error due to division rounding and add it to the runSteps
        diff_steps: int = total_steps - acc_steps - run_steps - dec_steps
        run_steps += diff_steps
        
        # Track the current overall step position
        current_step_position: int = 0

        # Accelerate stepper
        if acc_steps > 0:
            while current_step_position < acc_steps:
                temp_steps: int = 0
                temp_spp: int = 0

                # Accelerate and check for overflow
                if len(self.sequence_steps) == 0: temp_spp = minimum_spp
                else: temp_spp = self.sequence_spp[-1] + acc_spppp
                if temp_spp > maximum_spp: temp_spp = maximum_spp
                temp_steps = temp_spp # When accelerating Steps and SPP are the same

                # Store the result in the dynamic sequence array
                self.sequence_spp.append(temp_spp)
                self.sequence_steps.append(temp_steps)
                current_step_position += temp_steps

                # Show the result for this sequence part
                if Velocity.FULL_DEBUG:
                    logging.debug(f"Velocity::__init__ - ACC [{len(self.sequence_steps)}] ({current_step_position}) Steps = {self.sequence_steps[-1]} - SPP = {self.sequence_spp[-1]}")

            # Count the number of steps in the generated acceleration sequence
            acc_steps = sum(self.sequence_steps)
            dec_steps = acc_steps
            run_steps = total_steps - acc_steps - dec_steps       

            logging.debug("Velocity::__init__ - Steps per stage actual:")
            logging.debug(f"Velocity::__init__ -  ACC steps = {acc_steps}")
            logging.debug(f"Velocity::__init__ -  RUN steps = {run_steps}")
            logging.debug(f"Velocity::__init__ -  DEC steps = {dec_steps}")
            if Velocity.FULL_DEBUG: logging.debug("Velocity::__init__")

        # Run stepper
        temp_steps: int = 0
        temp_spp: int = 0

        # This is a single sequence part to perform the all the run steps
        temp_steps = run_steps
        current_step_position += run_steps

        # Check that the sequence has contents
        if len(self.sequence_spp) > 0:
            # If we have headroom, we can accelerate once more for the run steps
            if (self.sequence_spp[-1] + self._parameters.acc_spsps) < self._parameters.maximum_sps:
                temp_spp = self.sequence_spp[-1] + self._parameters.acc_spsps
                if temp_spp > self._parameters.maximum_sps: temp_spp = self._parameters.maximum_sps
            else:
                # Run at full speed
                temp_spp = self._parameters.maximum_sps
        else:
            # There were no acceleration steps... use minimum speed
            temp_spp = self._parameters.acc_spsps
        
        # Store the RUN result in the dynamic sequence array
        self.sequence_spp.append(temp_spp)
        self.sequence_steps.append(temp_steps)

        # Show the result for this sequence part
        if Velocity.FULL_DEBUG:
            logging.debug(f"Velocity::__init__ - RUN [{len(self.sequence_steps)}] ({current_step_position}) Steps = {self.sequence_steps[-1]} - SPP = {self.sequence_spp[-1]}")

        logging.debug(f"Velocity::__init__ - Maximum achieved RUN speed = {self.sequence_spp[-1] * self._parameters.intervals_per_second} Steps per second")

        # Decelerate stepper
        # (This simply copies the acceleration sequence in reverse)
        if dec_steps > 0:
            for i in range(len(self.sequence_steps) - 1, 0, -1):
                self.sequence_spp.append(self.sequence_spp[i-1])
                self.sequence_steps.append(self.sequence_steps[i-1])

                # Keep track of our current position
                current_step_position += self.sequence_steps[i-1]

                # Show the result for this sequence part
                if Velocity.FULL_DEBUG:
                    logging.debug(f"Velocity::__init__ - DEC [{len(self.sequence_steps)}] ({current_step_position}) Steps = {self.sequence_steps[-1]} - SPP = {self.sequence_spp[-1]}")
                
        # Count the number of steps in the generated acceleration sequence
        logging.debug(f"Velocity::__init__ - Total number of steps = {sum(self.sequence_steps)}")
        if Velocity.FULL_DEBUG: logging.debug("Velocity::__init__")

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