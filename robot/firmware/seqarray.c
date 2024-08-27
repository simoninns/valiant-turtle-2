/************************************************************************ 

    seqarray.c

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
#include <stdint.h>

#include "seqarray.h"
#include "debug.h"

// Note: Originally based on an example found at ->
//       https://www.geeksforgeeks.org/dynamically-growing-array-in-c/

// Sequence array structure 
struct sequence_array { 
    size_t size; 
    size_t capacity; 
    int32_t* steps;
    int32_t* sps; 
};

// Initialise the sequence dynamic array
void seqarray_init(sequence_array_t** sequence) {
    sequence_array_t *container; 
    container = (sequence_array_t*)malloc(sizeof(sequence_array_t)); 
    if(!container) { 
        debug_printf("seqarray_init(): Memory Allocation Failed\n"); 
        exit(0); 
    } 
  
    container->size = 0; 
    container->capacity = INITIAL_SEQUENCE_SIZE; 

    // Initialise memory for steps
    container->steps = (int32_t *)malloc(INITIAL_SEQUENCE_SIZE * sizeof(int32_t));
    if (!container->steps){ 
        debug_printf("seqarray_init(): Memory Allocation Failed\n"); 
        exit(0); 
    }

    // Initialise memory for spp
    container->sps = (int32_t *)malloc(INITIAL_SEQUENCE_SIZE * sizeof(int32_t)); // 1 is the initial array size
    if (!container->sps){ 
        debug_printf("seqarray_init(): Memory Allocation Failed\n"); 
        exit(0); 
    } 
  
    *sequence = container; 
}

// Insert a step and spp value into the sequence dynamic array
void seqarray_insert(sequence_array_t* container, int32_t steps, int32_t spp) 
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
            debug_printf("seqarray_insert(): realloc failed\n"); 
            container->steps = tempSteps; 
            return; 
        } 

        // Reallocate the SPS array
        container->sps = realloc(container->sps, container->capacity * sizeof(int32_t)); 
        if(!container->sps) { 
            debug_printf("seqarray_insert(): realloc failed\n"); 
            container->sps = tempSps; 
            return; 
        } 
    }

    // Store into the dynamic array
    container->steps[container->size] = steps; 
    container->sps[container->size] = spp;
    container->size++;
}

// Get the steps from the dynamic array
int32_t seqarray_get_steps(sequence_array_t* container, int32_t index) 
{ 
    if(index >= container->size) { 
        debug_printf("seqarray_get_steps(): Index Out of Bounds\n"); 
        return -1; 
    } 
    return container->steps[index]; 
} 

// Get the SPS from the dynamic array
int32_t seqarray_get_sps(sequence_array_t* container, int32_t index) 
{ 
    if(index >= container->size) { 
        debug_printf("seqarray_get_spp(): Index Out of Bounds\n"); 
        return -1; 
    } 
    return container->sps[index]; 
}

// Output the sequence contents to stdout
void seqarray_display(sequence_array_t* container) {
    if (container->size > 0) {
        int32_t totalSteps = 0;
        int32_t maxSps = 0;

        debug_printf("seqarray_display():\n");
        debug_printf("  +--------+--------+--------+\n");
        debug_printf("  | Pos    | Steps  | SPS    |\n");
        debug_printf("  +--------+--------+--------+\n");

        for (int i = 0; i < container->size; i++) { 
            debug_printf("  | %6d | %6d | %6d |\r\n", i, container->steps[i], container->sps[i]);

            totalSteps += container->steps[i];
            if (container->sps[i] > maxSps) maxSps = container->sps[i];
        }
        debug_printf("  +--------+--------+--------+\n");

        debug_printf("\r\n");
        debug_printf("  Maximum SPS: %d\n", maxSps); 
        debug_printf("  Total steps: %d\n", totalSteps);
        debug_printf("\r\n");
    } else {
        // The sequence is empty
        debug_printf("seqarray_display(): Sequence is empty - nothing to display\n");
        debug_printf("\n");
    }
}

// Get the current size of the dynamic array
int32_t seqarray_get_size(sequence_array_t* container) 
{ 
    return container->size; 
}

// Free the dynamic array
void seqarray_free(sequence_array_t* container) { 
    if (container != NULL) {
        free(container->steps);
        free(container->sps); 
        free(container);
    }
}