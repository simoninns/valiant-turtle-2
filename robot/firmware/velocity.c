/************************************************************************ 

    velocity.c

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
#include <stdlib.h>

#include "pico/stdlib.h"

#include "velocity.h"
#include "debug.h"

// Initialise the velocity array
void velocity_calculator_init(velocity_sequence_t** container) {
    velocity_sequence_t *_container; 

    _container = (velocity_sequence_t*)malloc(sizeof(velocity_sequence_t)); 
    if(!_container) { 
        debug_printf("velocity_calculator_init(): Memory Allocation Failed\n"); 
        exit(0); 
    } 
  
    _container->size = 0; 
    _container->capacity = INITIAL_SEQUENCE_SIZE; 

    // Initialise memory for steps
    _container->steps = (int32_t *)malloc(INITIAL_SEQUENCE_SIZE * sizeof(int32_t));
    if (!_container->steps){ 
        debug_printf("velocity_calculator_init(): Memory Allocation Failed\n"); 
        exit(0); 
    }

    // Initialise memory for spp
    _container->sps = (int32_t *)malloc(INITIAL_SEQUENCE_SIZE * sizeof(int32_t));
    if (!_container->sps){ 
        debug_printf("velocity_calculator_init(): Memory Allocation Failed\n"); 
        exit(0); 
    } 
  
    *container = _container;

    debug_printf("velocity_calculator_init(): Container allocated and initialised\n");
}

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
// The function returns the number of intervals in the generated sequence array
int32_t velocity_calculator(velocity_sequence_t* container, int32_t totalSteps, int32_t accSpsps, int32_t minimumSps, int32_t maximumSps, int32_t intervalsPerSecond) {
    // Range check input parameters
    if (totalSteps < 1) {
        debug_printf("velocity_calculator(): ERROR - The number of required steps must be greater than 0\n");
        return false;
    }

    if (accSpsps < 1) {
        debug_printf("velocity_calculator(): ERROR - acceleration in Steps Per Second Per Second must be greater than 0\n");
        return false;
    }

    if (maximumSps < 1) {
        debug_printf("velocity_calculator(): ERROR - Maximum Steps Per Second must be greater than 0\n");
        return false;
    }

    if (maximumSps < accSpsps) {
        debug_printf("velocity_calculator(): ERROR - Maximum Steps Per Second less than acceleration in Steps Per Second Per Second\n");
        return false;
    }

    if (minimumSps < 1) {
        debug_printf("velocity_calculator(): ERROR - Minimum Steps Per Second must be greater than 0\n");
        return false;
    }

    if (minimumSps > maximumSps) {
        debug_printf("velocity_calculator(): ERROR - Maximum Steps Per Second must be greater than minimum Steps Per Second\n");
        return false;
    }

    // Show some debug:
    debug_printf("velocity_calculator(): Total steps = %d - Acceleration in steps per second per second = %d\n", totalSteps, accSpsps);
    debug_printf("velocity_calculator(): Minimum steps per second = %d - Maximum steps per second = %d\n", minimumSps, maximumSps);
    debug_printf("velocity_calculator(): Intervals per second = %d\n", intervalsPerSecond);

    int32_t accSpppp = accSpsps / intervalsPerSecond; // acceleration in steps per period per period
    int32_t maximumSpp = maximumSps / intervalsPerSecond; // maximum speed in steps per period
    int32_t minimumSpp = minimumSps / intervalsPerSecond; // minimum speed in steps per period
    if (accSpppp < 1) accSpppp = 1;
    if (maximumSpp < 1) maximumSpp = 1;
    if (minimumSpp < 1) minimumSpp = 1;

    // Before calculating the actual sequence, we make a base assumption
    // that acceleration can use a maximum of 40% of the total required steps
    // (and that deceleration is a mirror of acceleration):
    float accStepsf = ((float)totalSteps / 100.0) * 40.0; // 40%
    float runStepsf = ((float)totalSteps / 100.0) * 60.0; // 20%
    float decStepsf = ((float)totalSteps / 100.0) * 40.0; // 40%
    int32_t accSteps = accStepsf;
    int32_t runSteps = runStepsf;
    int32_t decSteps = decStepsf;

    // Calculate any error due to division rounding and add it to the runSteps
    int32_t difSteps = totalSteps - accSteps - runSteps - decSteps;
    runSteps += difSteps;
    
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
            else tempSpp = (velocity_get_sps(container, sequenceNumber - 1) / intervalsPerSecond) + accSpppp;
            if (tempSpp > maximumSpp) tempSpp = maximumSpp;

            // Store the calculated step (the rotation speed in steps per period and steps are the same)
            tempSteps = tempSpp / intervalsPerSecond;
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
            velocity_sequence_insert(container, tempSteps, tempSpp * intervalsPerSecond);

            // On to the next...
            sequenceNumber++;
        }

        // Count the number of steps in the generated acceleration sequence
        accSteps = 0;
        for (i = 0; i < sequenceNumber; i++) {
            accSteps += velocity_get_steps(container, i);
        }

        accEnd = sequenceNumber - 1;
        decSteps = accSteps;
        runSteps = totalSteps - accSteps - decSteps;
    }

    // Run
    tempSteps = 0;
    tempSpp = 0;

    // This is a single sequence part to perform the all the run steps
    tempSteps = runSteps;
    currentStepPosition += runSteps;

    // Check that the sequence has contents
    if (velocity_get_size(container) > 0) {
        // If we have headroom, we can accelerate once more for the run steps
        if ((velocity_get_sps(container, sequenceNumber-1) + accSpsps) < maximumSps) {
            tempSpp = velocity_get_sps(container, sequenceNumber-1) + accSpsps;
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
    velocity_sequence_insert(container, tempSteps, tempSpp);
    sequenceNumber++;

    if (decSteps > 0) {
        // Decelerate
        for (i = accEnd; i >= 0; i--) {
            tempSteps = 0;
            tempSpp = 0;

            // Move
            currentStepPosition += velocity_get_steps(container, i);

            // Store the calculated step
            tempSteps = velocity_get_steps(container, i);
            tempSpp = velocity_get_sps(container, i);
            //debug_printf("DEC - [%d] [%d] Steps = %d - SPP = %d\n", sequenceNumber, currentStepPosition, tempSteps, tempSpp);

            // Store the result in the dynamic sequence array
            velocity_sequence_insert(container, tempSteps, tempSpp);
            sequenceNumber++;
        }
    }

    // Return the length of the sequence
    return velocity_get_size(container);
}

// Free the generated velocity array
void velocity_calculator_free(velocity_sequence_t* container) { 
    free(container->steps);
    free(container->sps); 
    free(container);
}

// Get the steps from the dynamic array
int32_t velocity_get_steps(velocity_sequence_t* container, int32_t index) 
{ 
    if(index >= container->size) { 
        debug_printf("velocity_sequence_get_steps(): Index Out of Bounds\n"); 
        return -1; 
    } 
    return container->steps[index]; 
} 

// Get the SPS from the dynamic array
int32_t velocity_get_sps(velocity_sequence_t* container, int32_t index) 
{ 
    if(index >= container->size) { 
        debug_printf("velocity_sequence_get_sps(): Index Out of Bounds\n"); 
        return -1; 
    } 
    return container->sps[index]; 
}

// Get the current size of the dynamic array
int32_t velocity_get_size(velocity_sequence_t* container) 
{ 
    return container->size; 
}

// Container operations (internal) --------------------------------------------------------------------------------------

// Insert a step and spp value into the sequence dynamic array
void velocity_sequence_insert(velocity_sequence_t* container, int32_t steps, int32_t spp) 
{ 
    // If the array is at capacity - expand it
    if (container->size == container->capacity) { 
        
        int32_t *tempSteps = container->steps;
        int32_t *tempSps = container->sps; 

        // Increase capacity
        container->capacity <<= 1;
        
        // Reallocate the steps array
        container->steps = realloc(container->steps, container->capacity * sizeof(int32_t)); 
        if(!container->steps) { 
            debug_printf("velocity_sequence_insert(): realloc failed\n"); 
            container->steps = tempSteps; 
            return; 
        } 

        // Reallocate the SPS array
        container->sps = realloc(container->sps, container->capacity * sizeof(int32_t)); 
        if(!container->sps) { 
            debug_printf("velocity_sequence_insert(): realloc failed\n"); 
            container->sps = tempSps; 
            return; 
        } 
    }

    // Store into the dynamic array
    container->steps[container->size] = steps; 
    container->sps[container->size] = spp;
    container->size++;
}