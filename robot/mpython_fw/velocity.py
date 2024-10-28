#************************************************************************ 
#
#   velocity.py
#
#   Stepper motor velocity calculations
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
    def __init__(self, totalSteps: int, accSpsps: int, minimumSps: int, maximumSps: int, intervalsPerSecond: int):
        # Initialise lists to hold the velocity sequence
        self.sequence_steps = [] # Number of steps in this period
        self.sequence_spp = [] # Rotational speed in steps per period (for this period)
        self._intervals_per_second = intervalsPerSecond

        # Range check input parameters
        if totalSteps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - The number of required steps must be greater than 0")

        if accSpsps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - acceleration in Steps Per Second Per Second must be greater than 0")

        if minimumSps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - Minimum Steps Per Second must be greater than 0")

        if maximumSps < 1:
            raise RuntimeError("Velocity::__init__ - ERROR - Maximum Steps Per Second must be greater than 0")

        if maximumSps < accSpsps:
            raise RuntimeError("Velocity::__init__ - ERROR - Maximum Steps Per Second less than acceleration in Steps Per Second Per Second")

        if maximumSps < minimumSps:
            raise RuntimeError("Velocity::__init__ - ERROR - Maximum Steps Per Second must be greater than minimum Steps Per Second")

        # Show some debug
        log_debug("Velocity::__init__ - Total steps = ", totalSteps)
        log_debug("Velocity::__init__ - Acceleration in steps per second per second = ", accSpsps)
        log_debug("Velocity::__init__ - Minimum steps per second = ", minimumSps)
        log_debug("Velocity::__init__ - Maximum steps per second = ", maximumSps)
        log_debug("Velocity::__init__ - Intervals per second = ", intervalsPerSecond)
        log_debug("")

        accSpppp: int = int(accSpsps / intervalsPerSecond) # acceleration in steps per period per period
        maximumSpp: int = int(maximumSps / intervalsPerSecond) # maximum speed in steps per period
        minimumSpp: int = int(minimumSps / intervalsPerSecond) # minimum speed in steps per period
        if accSpppp < 1: accSpppp = 1
        if maximumSpp < 1: maximumSpp = 1
        if minimumSpp < 1: minimumSpp = 1

        log_debug("Velocity::__init__ - Acceleration in steps per period per period = ", accSpppp)
        log_debug("Velocity::__init__ - Minimum steps per period = ", minimumSpp)
        log_debug("Velocity::__init__ - Maximum steps per period = ", maximumSpp)
        log_debug("")

        # Before calculating the actual sequence, we make a base assumption
        # that acceleration can use a maximum of 40% of the total required steps
        # (and that deceleration is a mirror of acceleration):
        accStepsf: float = (float(totalSteps) / 100.0) * 40.0 # 40%
        runStepsf: float = (float(totalSteps) / 100.0) * 20.0 # 20%
        decStepsf: float = (float(totalSteps) / 100.0) * 40.0 # 40%
        accSteps: int = int(accStepsf)
        runSteps: int = int(runStepsf)
        decSteps: int = int(decStepsf)

        log_debug("Velocity::__init__ - Steps per stage prediction:")
        log_debug("Velocity::__init__ -  ACC steps = ", accSteps)
        log_debug("Velocity::__init__ -  RUN steps = ", runSteps)
        log_debug("Velocity::__init__ -  DEC steps = ", decSteps)
        log_debug("")

        # Calculate any error due to division rounding and add it to the runSteps
        difSteps: int = totalSteps - accSteps - runSteps - decSteps
        runSteps += difSteps
        
        # Track the current overall step position
        currentStepPosition: int = 0

        # Accelerate stepper
        if accSteps > 0:
            while currentStepPosition < accSteps:
                tempSteps: int = 0
                tempSpp: int = 0

                # Accelerate and check for overflow
                if len(self.sequence_steps) == 0: tempSpp = minimumSpp
                else: tempSpp = self.sequence_spp[-1] + accSpppp
                if tempSpp > maximumSpp: tempSpp = maximumSpp
                tempSteps = tempSpp # When accelerating Steps and SPP are the same

                # Store the result in the dynamic sequence array
                self.sequence_spp.append(tempSpp)
                self.sequence_steps.append(tempSteps)
                currentStepPosition += tempSteps

                # Show the result for this sequence part
                log_debug("Velocity::__init__ - ACC [", len(self.sequence_steps), "] (", currentStepPosition, ") Steps =",
                      self.sequence_steps[-1], "- SPP =", self.sequence_spp[-1])

            # Count the number of steps in the generated acceleration sequence
            accSteps = 0
            for i in range(0, len(self.sequence_steps)):
                accSteps += self.sequence_steps[i]
            decSteps = accSteps
            runSteps = totalSteps - accSteps - decSteps       

            log_debug("Velocity::__init__ - Steps per stage actual:")
            log_debug("Velocity::__init__ -  ACC steps = ", accSteps)
            log_debug("Velocity::__init__ -  RUN steps = ", runSteps)
            log_debug("Velocity::__init__ -  DEC steps = ", decSteps)
            log_debug("")

        # Run stepper
        tempSteps: int = 0
        tempSpp: int = 0

        # This is a single sequence part to perform the all the run steps
        tempSteps = runSteps
        currentStepPosition += runSteps

        # Check that the sequence has contents
        if len(self.sequence_spp) > 0:
            # If we have headroom, we can accelerate once more for the run steps
            if (self.sequence_spp[-1] + accSpsps) < maximumSps:
                tempSpp = self.sequence_spp[-1] + accSpsps
                if tempSpp > maximumSps: tempSpp = maximumSps
            else:
                # Run at full speed
                tempSpp = maximumSps
        else:
            # There were no acceleration steps... use minimum speed
            tempSpp = accSpsps
        
        # Store the RUN result in the dynamic sequence array
        self.sequence_spp.append(tempSpp)
        self.sequence_steps.append(tempSteps)

        # Show the result for this sequence part
        log_debug("Velocity::__init__ - RUN [", len(self.sequence_steps), "] (", currentStepPosition, ") Steps =",
                      self.sequence_steps[-1], "- SPP =", self.sequence_spp[-1])
        log_debug("Velocity::__init__ - Maximum achieved RUN speed =",self.sequence_spp[-1] * intervalsPerSecond,"Steps per second")

        # Decelerate stepper
        # (This simply copies the acceleration sequence in reverse)
        if decSteps > 0:
            for i in range(len(self.sequence_steps) - 1, 0, -1):
                self.sequence_spp.append(self.sequence_spp[i-1])
                self.sequence_steps.append(self.sequence_steps[i-1])

                # Keep track of our current position
                currentStepPosition += self.sequence_steps[i-1]

                # Show the result for this sequence part
                log_debug("Velocity::__init__ - DEC [", len(self.sequence_steps), "] (", currentStepPosition, ") Steps =",
                      self.sequence_steps[-1], "- SPP =", self.sequence_spp[-1])
                
        # Count the number of steps in the generated acceleration sequence
        finalTotal = 0
        for i in range(0, len(self.sequence_steps)):
            finalTotal += self.sequence_steps[i]
        log_debug("Velocity::__init__ - Total number of steps = ", finalTotal)
        log_debug("")

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