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

import logging

# This function produces a sequence of steps that represent the required number of steps
# and rotational speed needed to accelerate, run and decelerate based on a set number of
# stepper motor steps.
#
# required_steps is the total number of steps requested
# acc_spsps is the maximum acceleration in Steps per second per second
# maximum_sps is the maximum allowed rotational speed in Steps per second
# minimum_sps is the minimum allowed rotational speed in steps per second
# intervals_per_second is the number of intervals per second (which sets the period of each update)
class Velocity:
    def __init__(self, total_steps: int, acc_spsps: int, minimum_sps: int, maximum_sps: int, intervals_per_second: int):
        # Initialise lists to hold the velocity sequence
        self.sequence_steps = [] # Number of steps in this period
        self.sequence_spp = [] # Rotational speed in steps per period (for this period)
        self._intervals_per_second = intervals_per_second

        # Range check input parameters
        if total_steps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - The number of required steps must be greater than 0")

        if acc_spsps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - acceleration in Steps Per Second Per Second must be greater than 0")

        if minimum_sps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - Minimum Steps Per Second must be greater than 0")

        if maximum_sps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - Maximum Steps Per Second must be greater than 0")

        if maximum_sps < acc_spsps:
            raise RuntimeError("Velocity::__init__ - ERROR - Maximum Steps Per Second less than acceleration in Steps Per Second Per Second")

        if maximum_sps < minimum_sps:
            raise RuntimeError("Velocity::__init__ - ERROR - Maximum Steps Per Second must be greater than minimum Steps Per Second")

        # Show some debug
        logging.debug(f"Velocity::__init__ - Total steps = ", total_steps)
        logging.debug(f"Velocity::__init__ - Acceleration in steps per second per second = {acc_spsps}")
        logging.debug(f"Velocity::__init__ - Minimum steps per second = {minimum_sps}")
        logging.debug(f"Velocity::__init__ - Maximum steps per second = {maximum_sps}")
        logging.debug(f"Velocity::__init__ - Intervals per second = {intervals_per_second}")
        logging.debug("")

        acc_spppp: int = int(acc_spsps / intervals_per_second) # acceleration in steps per period per period
        maximum_spp: int = int(maximum_sps / intervals_per_second) # maximum speed in steps per period
        minimum_spp: int = int(minimum_sps / intervals_per_second) # minimum speed in steps per period
        if acc_spppp < 1: acc_spppp = 1
        if maximum_spp < 1: maximum_spp = 1
        if minimum_spp < 1: minimum_spp = 1

        logging.debug(f"Velocity::__init__ - Acceleration in steps per period per period = {acc_spppp}")
        logging.debug(f"Velocity::__init__ - Minimum steps per period = {minimum_spp}")
        logging.debug(f"Velocity::__init__ - Maximum steps per period = {maximum_spp}")
        logging.debug("")

        # Before calculating the actual sequence, we make a base assumption
        # that acceleration can use a maximum of 40% of the total required steps
        # (and that deceleration is a mirror of acceleration):
        acc_stepsf: float = (float(total_steps) / 100.0) * 40.0 # 40%
        run_stepsf: float = (float(total_steps) / 100.0) * 20.0 # 20%
        dec_stepsf: float = (float(total_steps) / 100.0) * 40.0 # 40%
        acc_steps: int = int(acc_stepsf)
        run_steps: int = int(run_stepsf)
        dec_steps: int = int(dec_stepsf)

        logging.debug("Velocity::__init__ - Steps per stage prediction:")
        logging.debug(f"Velocity::__init__ -  ACC steps = {acc_steps}")
        logging.debug(f"Velocity::__init__ -  RUN steps = {run_steps}")
        logging.debug(f"Velocity::__init__ -  DEC steps = {dec_steps}")
        logging.debug("")

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
                logging.debug(f"Velocity::__init__ - ACC [{len(self.sequence_steps)}] ({current_step_position}) Steps = {self.sequence_steps[-1]} - SPP = {self.sequence_spp[-1]}")

            # Count the number of steps in the generated acceleration sequence
            acc_steps = 0
            for i in range(0, len(self.sequence_steps)):
                acc_steps += self.sequence_steps[i]
            dec_steps = acc_steps
            run_steps = total_steps - acc_steps - dec_steps       

            logging.debug("Velocity::__init__ - Steps per stage actual:")
            logging.debug(f"Velocity::__init__ -  ACC steps = {acc_steps}")
            logging.debug(f"Velocity::__init__ -  RUN steps = {run_steps}")
            logging.debug(f"Velocity::__init__ -  DEC steps = {dec_steps}")
            logging.debug("")

        # Run stepper
        temp_steps: int = 0
        temp_spp: int = 0

        # This is a single sequence part to perform the all the run steps
        temp_steps = run_steps
        current_step_position += run_steps

        # Check that the sequence has contents
        if len(self.sequence_spp) > 0:
            # If we have headroom, we can accelerate once more for the run steps
            if (self.sequence_spp[-1] + acc_spsps) < maximum_sps:
                temp_spp = self.sequence_spp[-1] + acc_spsps
                if temp_spp > maximum_sps: temp_spp = maximum_sps
            else:
                # Run at full speed
                temp_spp = maximum_sps
        else:
            # There were no acceleration steps... use minimum speed
            temp_spp = acc_spsps
        
        # Store the RUN result in the dynamic sequence array
        self.sequence_spp.append(temp_spp)
        self.sequence_steps.append(temp_steps)

        # Show the result for this sequence part
        logging.debug(f"Velocity::__init__ - RUN [{len(self.sequence_steps)}] ({current_step_position}) Steps ={self.sequence_steps[-1]} - SPP ={self.sequence_spp[-1]}")
        logging.debug(f"Velocity::__init__ - Maximum achieved RUN speed ={self.sequence_spp[-1] * intervals_per_second} Steps per second")

        # Decelerate stepper
        # (This simply copies the acceleration sequence in reverse)
        if dec_steps > 0:
            for i in range(len(self.sequence_steps) - 1, 0, -1):
                self.sequence_spp.append(self.sequence_spp[i-1])
                self.sequence_steps.append(self.sequence_steps[i-1])

                # Keep track of our current position
                current_step_position += self.sequence_steps[i-1]

                # Show the result for this sequence part
                logging.debug(f"Velocity::__init__ - DEC [{len(self.sequence_steps)}] ({current_step_position}) Steps ={self.sequence_steps[-1]} - SPP ={self.sequence_spp[-1]}")
                
        # Count the number of steps in the generated acceleration sequence
        finalTotal = 0
        for i in range(0, len(self.sequence_steps)):
            finalTotal += self.sequence_steps[i]
        logging.debug(f"Velocity::__init__ - Total number of steps = {finalTotal}")
        logging.debug("")

    # Return the total number of steps in the velocity sequence
    @property
    def total_steps(self) -> int:
        step_count = 0
        for i in range(0, len(self.sequence_steps)):
            step_count += self.sequence_steps[i]
        return step_count
    
    # Return the length of the velocity sequence
    @property
    def length(self) -> int:
        return len(self.sequence_steps) # Both steps and spp are the same length
    
    # Return the intervals per second for the velocity sequence
    @property
    def intervals_per_second(self) -> int:
        return self._intervals_per_second
    
if __name__ == "__main__":
    from main import main
    main()