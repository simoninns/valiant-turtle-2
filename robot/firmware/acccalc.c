/************************************************************************ 

    acccalc.c

    Valiant Turtle 2 - Raspberry Pi Pico W Firmware
    Copyright (C) 2024 Simon Inns

    This file is part of Valiant Turtle 2

    This is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Email: simon.inns@gmail.com

************************************************************************/

#include <stdio.h>

#include "pico/stdlib.h"

#include "acccalc.h"
#include "seqarray.h"
#include "debug.h"

// -----------------------------------------------------------------------------------------------------------

// This function produces a sequence of steps that represent the required number of steps
// and rotational speed needed to accelerate, run and decelerate based on a set number of
// stepper motor steps.
//
// container->steps is an array of the number of steps required for each entry in the sequence
// container->sps is an array of the steps per second required for each entry in the sequence
//
// requiredSteps is the total number of steps requested by the caller
// accSpsps is the maximum acceleration in Steps per Second per Second requested by the caller
// maximumSps is the maximum allowed rotational speed in Steps per Second requested by the caller
//
// The function returns true on success and false on failure
//
bool acccalc_calculate(sequence_array_t* container, int32_t requiredSteps, int32_t accSpsps, int32_t minimumSps, int32_t maximumSps, int32_t updatesPerSecond) {
    // Range check input parameters
    if (requiredSteps < 1) {
        debug_printf("acccalc_calculate(): ERROR - The number of required steps must be greater than 0\n");
        return false;
    }

    if (accSpsps < 1) {
        debug_printf("acccalc_calculate(): ERROR - acceleration in Steps Per Second Per Second must be greater than 0\n");
        return false;
    }

    if (maximumSps < 1) {
        debug_printf("acccalc_calculate(): ERROR - Maximum Steps Per Second must be greater than 0\n");
        return false;
    }

    if (maximumSps < accSpsps) {
        debug_printf("acccalc_calculate(): ERROR - Maximum Steps Per Second less than acceleration in Steps Per Second Per Second\n");
        return false;
    }

    if (minimumSps < 1) {
        debug_printf("acccalc_calculate(): ERROR - Minimum Steps Per Second must be greater than 0\n");
        return false;
    }

    if (minimumSps > maximumSps) {
        debug_printf("acccalc_calculate(): ERROR - Maximum Steps Per Second must be greater than minimum Steps Per Second\n");
        return false;
    }

    // Show some debug:
    debug_printf("acccalc_calculate(): Acceleration is %d steps per second per second\n", accSpsps);
    debug_printf("acccalc_calculate(): Minimum speed is %d steps per second\n", minimumSps);
    debug_printf("acccalc_calculate(): Maximum speed is %d steps per second\n", maximumSps);
    debug_printf("acccalc_calculate(): Using %d updates per second\n", updatesPerSecond);

    int32_t accSpppp = accSpsps / updatesPerSecond; // acceleration in steps per period per period
    int32_t maximumSpp = maximumSps / updatesPerSecond; // maximum speed in steps per period
    int32_t minimumSpp = minimumSps / updatesPerSecond; // minimum speed in steps per period
    if (accSpppp < 1) accSpppp = 1;
    if (maximumSpp < 1) maximumSpp = 1;
    if (minimumSpp < 1) minimumSpp = 1;

    debug_printf("acccalc_calculate(): Acceleration is %d steps per period per period\n", accSpppp);
    debug_printf("acccalc_calculate(): Minimum speed is %d steps per period\n", minimumSpp);
    debug_printf("acccalc_calculate(): Maximum speed is %d steps per period\n", maximumSpp);

    debug_printf("acccalc_calculate(): \n");

    // Before calculating the actual sequence, we make a base assumption
    // that acceleration can use a maximum of 40% of the total required steps
    // (and that deceleration is a mirror of acceleration):
    float accStepsf = ((float)requiredSteps / 100.0) * 40.0; // 40%
    float runStepsf = ((float)requiredSteps / 100.0) * 60.0; // 20%
    float decStepsf = ((float)requiredSteps / 100.0) * 40.0; // 40%
    int32_t accSteps = accStepsf;
    int32_t runSteps = runStepsf;
    int32_t decSteps = decStepsf;

    // Calculate any error due to division rounding and add it to the runSteps
    int32_t difSteps = requiredSteps - accSteps - runSteps - decSteps;
    runSteps += difSteps;

    debug_printf("acccalc_calculate(): Acceleration steps = %d\n", accSteps);
    debug_printf("acccalc_calculate(): Run steps = %d\n", runSteps);
    debug_printf("acccalc_calculate(): Deceleration steps = %d\n", decSteps);
    
    // Variables
    int32_t sequenceNumber = 0;
    int32_t currentStepPosition = 0;
    int32_t lengthOfAccelerationSequence = 0;

    // Scratch variables
    int i;
    int32_t accEnd = 0;
    int tempSteps = 0;
    int tempSpp = 0;

    if (accSteps > 0) {
        // Accelerate
        while (currentStepPosition < accSteps) {
            tempSteps = 0;
            tempSpp = 0;

            // Accelerate and check for overflow
            if (sequenceNumber == 0) tempSpp = minimumSpp; //tempSpp = accSpppp;
            else tempSpp = (seqarray_get_sps(container, sequenceNumber - 1) / updatesPerSecond) + accSpppp;
            if (tempSpp > maximumSpp) tempSpp = maximumSpp;

            // Store the calculated step (the rotation speed in steps per period and steps are the same)
            tempSteps = tempSpp / updatesPerSecond;
            if (tempSteps < 1) tempSteps = 1;
            currentStepPosition += tempSteps;

            // Track the length of the acceleration sequence
            lengthOfAccelerationSequence++;

            // Are we done accelerating?
            if ((tempSpp >= maximumSpp) || (currentStepPosition + accSpppp) > accSteps) {
                currentStepPosition -= tempSteps;
                break;
            }

            // Show the result for this sequence part
            // debug_printf("ACC - [%d] [%d] Steps = %d - SPP = %d\n", sequenceNumber, currentStepPosition, tempSteps, tempSpp);

            // Store the result in the dynamic sequence array
            seqarray_insert(container, tempSteps, tempSpp * updatesPerSecond);

            // On to the next...
            sequenceNumber++;
        }

        // Count the number of steps in the generated acceleration sequence
        accSteps = 0;
        for (i = 0; i < sequenceNumber; i++) {
            accSteps += seqarray_get_steps(container, i);
        }

        accEnd = sequenceNumber - 1;
        decSteps = accSteps;
        runSteps = requiredSteps - accSteps - decSteps;
    }

    // Run
    tempSteps = 0;
    tempSpp = 0;

    // This is a single sequence part to perform the all the run steps
    tempSteps = runSteps;
    currentStepPosition += runSteps;

    // Check that the sequence has contents
    if (seqarray_get_size(container) > 0) {
        // If we have headroom, we can accelerate once more for the run steps
        if ((seqarray_get_sps(container, sequenceNumber-1) + accSpsps) < maximumSps) {
            tempSpp = seqarray_get_sps(container, sequenceNumber-1) + accSpsps;
            if (tempSpp > maximumSps) tempSpp = maximumSps;
        } else {
            // Run at full speed
            tempSpp = maximumSps;
        }
    } else {
        // There were no acceleration steps... use minimum speed
        tempSpp = accSpsps;
    }
    
    //debug_printf("RUN - [%d] [%d] Steps = %d - SPP = %d\n", sequenceNumber, currentStepPosition, tempSteps, tempSpp);

    // Store the result in the dynamic sequence array
    seqarray_insert(container, tempSteps, tempSpp);
    sequenceNumber++;

    if (decSteps > 0) {
        // Decelerate
        for (i = accEnd; i >= 0; i--) {
            tempSteps = 0;
            tempSpp = 0;

            // Move
            currentStepPosition += seqarray_get_steps(container, i);

            // Store the calculated step
            tempSteps = seqarray_get_steps(container, i);
            tempSpp = seqarray_get_sps(container, i);
            //debug_printf("DEC - [%d] [%d] Steps = %d - SPP = %d\n", sequenceNumber, currentStepPosition, tempSteps, tempSpp);

            // Store the result in the dynamic sequence array
            seqarray_insert(container, tempSteps, tempSpp);
            sequenceNumber++;
        }
    }

    // Return successfully
    return true;
}