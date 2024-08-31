/************************************************************************ 

    stepper.c

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
#include "hardware/pio.h"
#include "hardware/irq.h"

#include "stepper.h"
#include "stepper.pio.h"
#include "seqarray.h"

// Expected system clock speed is 125 MHz
// This module should probably check the clock speed at
// run-time... TODO

// Globals
static PIO pio[3];
static uint sm[3];
static uint offset[3];
static int8_t pio_irq[3];

int32_t left_sequence_pointer;
int32_t right_sequence_pointer;
sequence_array_t* left_local_container;
sequence_array_t* right_local_container;
bool sm_left_busy;
bool sm_right_busy;

// Initialise the stepper motor control
void stepper_init()
{
    // Initialise the drive motor control GPIOs
    gpio_init(SM_ENABLE_GPIO);
    gpio_init(SM_LSTEP_GPIO);
    gpio_init(SM_RSTEP_GPIO);
    gpio_init(SM_LDIR_GPIO);
    gpio_init(SM_RDIR_GPIO);
    gpio_init(SM_LM0_GPIO);
    gpio_init(SM_LM1_GPIO);
    gpio_init(SM_RM0_GPIO);
    gpio_init(SM_RM1_GPIO);

    // Set the drive motor control GPIO directions
    gpio_set_dir(SM_ENABLE_GPIO, GPIO_OUT);
    gpio_set_dir(SM_LSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(SM_RSTEP_GPIO, GPIO_OUT);
    gpio_set_dir(SM_LDIR_GPIO, GPIO_OUT);
    gpio_set_dir(SM_RDIR_GPIO, GPIO_OUT);
    gpio_set_dir(SM_LM0_GPIO, GPIO_OUT);
    gpio_set_dir(SM_LM1_GPIO, GPIO_OUT);
    gpio_set_dir(SM_RM0_GPIO, GPIO_OUT);
    gpio_set_dir(SM_RM1_GPIO, GPIO_OUT);

    // Initialise microstep mode (800 steps/revolution)
    stepper_set_microstep_mode(SM_LEFT, SM_MODE_800);
    stepper_set_microstep_mode(SM_RIGHT, SM_MODE_800);

    // Set the stepper direction to forwards
    stepper_set_direction(SM_LEFT, SM_FORWARDS);
    stepper_set_direction(SM_RIGHT, SM_FORWARDS);

    // Disable the steppers
    stepper_enable(false);

    // Flag the stepper motors as idle
    sm_left_busy = false;
    sm_right_busy = false;

    // Start the PIOs running
    stepper_pio_start();
}

// Set the stepper directions
// Note: The steppers are mounted opposite each other, so 'direction' is different for either stepper
void stepper_set_direction(sm_side_t side, sm_direction_t direction)
{
    if (side == SM_LEFT) {
        if (direction == SM_FORWARDS) {
            gpio_put(SM_LDIR_GPIO, 1);
            printf("stepper_set_direction(): Left motor direction forwards\r\n");
        }
        else {
            gpio_put(SM_LDIR_GPIO, 0);
            printf("stepper_set_direction(): Left motor direction reverse\r\n");
        }
    }
    
    if (side == SM_RIGHT) {
        if (direction == SM_FORWARDS) {
            gpio_put(SM_RDIR_GPIO, 0);
            printf("stepper_set_direction(): Right motor direction forwards\r\n");
        } else {
            gpio_put(SM_RDIR_GPIO, 1);
            printf("stepper_set_direction(): Right motor direction reverse\r\n");
        }
    }
}

// Sets the enable/disable flag on the DRV8825
void stepper_enable(bool state)
{
    if (state) {
        gpio_put(SM_ENABLE_GPIO, 1);
        printf("steppers_enable(): Stepper motors enabled\r\n");
    } else {
        gpio_put(SM_ENABLE_GPIO, 0);
        printf("steppers_enable(): Stepper motors disabled\r\n");
    }
}

// DRV8825 Microstepping control table
//
// M0 M1 M2 - Resolution
//  0  0  0   Full step  (200 steps/rev)
//  1  0  0   Half step  (400 steps/rev)
//  0  1  0   1/4 step   (800 steps/rev)
//  1  1  0   1/8 step   (1600 steps/rev)
//  0  0  1   1/16 step  (3200 steps/rev) Not supported
//  1  0  1   1/32 step  (6400 steps/rev) Not supported
//  0  1  1   1/32 step  N/A
//  1  1  1   1/32 step  N/A
void stepper_set_microstep_mode(sm_side_t sm_side, sm_microstep_mode_t microstep_mode)
{
    if (sm_side == SM_LEFT) {
        // Left motor
        switch(microstep_mode) {
            case SM_MODE_200:
                gpio_put(SM_LM0_GPIO, 0);
                gpio_put(SM_LM1_GPIO, 0);
                printf("stepper_set_microstep_mode(): Set left microstep to 200 steps/revolution\r\n");
                break;

            case SM_MODE_400:
                gpio_put(SM_LM0_GPIO, 1);
                gpio_put(SM_LM1_GPIO, 0);
                printf("stepper_set_microstep_mode(): Set left microstep to 400 steps/revolution\r\n");
                break;

            case SM_MODE_800:
                gpio_put(SM_LM0_GPIO, 0);
                gpio_put(SM_LM1_GPIO, 1);
                printf("stepper_set_microstep_mode(): Set left microstep to 800 steps/revolution\r\n");
                break;

            case SM_MODE_1600:
                gpio_put(SM_LM0_GPIO, 1);
                gpio_put(SM_LM1_GPIO, 1);
                printf("stepper_set_microstep_mode(): Set left microstep to 1600 steps/revolution\r\n");
                break;
        }
    } else {
        // Right motor
        switch(microstep_mode) {
            case SM_MODE_200:
                gpio_put(SM_RM0_GPIO, 0);
                gpio_put(SM_RM1_GPIO, 0);
                printf("stepper_set_microstep_mode(): Set right microstep to 200 steps/revolution\r\n");
                break;

            case SM_MODE_400:
                gpio_put(SM_RM0_GPIO, 1);
                gpio_put(SM_RM1_GPIO, 0);
                printf("stepper_set_microstep_mode(): Set right microstep to 400 steps/revolution\r\n");
                break;

            case SM_MODE_800:
                gpio_put(SM_RM0_GPIO, 0);
                gpio_put(SM_RM1_GPIO, 1);
                printf("stepper_set_microstep_mode(): Set right microstep to 800 steps/revolution\r\n");
                break;

            case SM_MODE_1600:
                gpio_put(SM_RM0_GPIO, 1);
                gpio_put(SM_RM1_GPIO, 1);
                printf("stepper_set_microstep_mode(): Set right microstep to 1600 steps/revolution\r\n");
                break;
        }
    }
}

// Check if the stepper motor is busy
bool stepper_is_busy(sm_side_t sm_side) {
    if (sm_side == SM_LEFT) return sm_left_busy;
    return sm_right_busy;
}

// Claim PIO, SM and then start the PIOs
// also enables the required interrupts for CPU interaction
void stepper_pio_start() {
    pio[0] = pio0;
    pio[1] = pio1;

    // Load PIO 0 - Left stepper motor
    offset[0] = pio_add_program(pio[0], &stepper_program);
    sm[0] = (int8_t)pio_claim_unused_sm(pio[0], false);

    pio_irq[0] = PIO0_IRQ_0;
    pio_set_irq0_source_enabled(pio[0], pis_interrupt0 , true); // Setting IRQ0_INTE - interrupt enable register
    irq_set_exclusive_handler(pio_irq[0], pio_irq_func);  // Set the handler in the NVIC
    irq_set_enabled(pio_irq[0], true); // Enabling the PIO0_IRQ_0

    stepper_program_init(pio[0], sm[0], offset[0], SM_LSTEP_GPIO);

    // Load PIO 1 - Right stepper motor
    offset[1] = pio_add_program(pio[1], &stepper_program);
    sm[1] = (int8_t)pio_claim_unused_sm(pio[1], false);

    pio_irq[1] = PIO1_IRQ_0;
    pio_set_irq0_source_enabled(pio[1], pis_interrupt0 , true); // Setting IRQ0_INTE - interrupt enable register
    irq_set_exclusive_handler(pio_irq[1], pio_irq_func);  // Set the handler in the NVIC
    irq_set_enabled(pio_irq[1], true); // Enabling the PIO1_IRQ_0

    stepper_program_init(pio[1], sm[1], offset[1], SM_RSTEP_GPIO);
}

// Stop the PIOs and free the PIOs and SMs
void stepper_pio_stop() {
    // PIO0
    // Disable interrupts
    pio_set_irq0_source_enabled(pio[0], pis_interrupt0 , false);
    irq_set_enabled(pio_irq[0], false);
    irq_remove_handler(pio_irq[0], pio_irq_func);

    // Cleanup PIO
    pio_remove_program_and_unclaim_sm(&stepper_program, pio[0], sm[0], offset[0]);

    // PIO1
    // Disable interrupts
    pio_set_irq0_source_enabled(pio[1], pis_interrupt0 , false);
    irq_set_enabled(pio_irq[1], false);
    irq_remove_handler(pio_irq[1], pio_irq_func);

    // Cleanup PIO
    pio_remove_program_and_unclaim_sm(&stepper_program, pio[1], sm[1], offset[1]);
}

bool stepper_set(sm_side_t sm_side, sequence_array_t* container)
{
    if (sm_side == SM_LEFT) {
        // Check that the stepper is not busy
        if (sm_left_busy) {
            printf("stepper_set(): Left stepper is busy, cannot set new sequence!");
            return false;
        }

        printf("stepper_set(): Starting new sequence - Left stepper Busy\n");

        left_sequence_pointer = 0;
        left_local_container = container; // Make a local copy so the interrupt handler can reference the sequence container

        // Flag the stepper as busy
        sm_left_busy = true;

        int32_t steps = seqarray_get_steps(left_local_container, left_sequence_pointer);
        int32_t sps = seqarray_get_sps(left_local_container, left_sequence_pointer);

        // Calculate the required delay
        uint32_t delay = stepper_sps_to_delay(sps);

        // Place the values into the TX FIFO
        // Note: The FIFO is 4x32-bit
        pio_sm_put_blocking(pio[0], sm[0], steps);
        pio_sm_put_blocking(pio[0], sm[0], delay);
        left_sequence_pointer++;
    }

    if (sm_side == SM_RIGHT) {
        // Check that the stepper is not busy
        if (sm_right_busy) {
            printf("stepper_set(): Right stepper is busy, cannot set new sequence!");
            return false;
        }

        printf("stepper_set(): Starting new sequence - Right stepper Busy\n");

        right_sequence_pointer = 0;
        right_local_container = container; // Make a local copy so the interrupt handler can reference the sequence container

        // Flag the stepper as busy
        sm_right_busy = true;

        int32_t steps = seqarray_get_steps(right_local_container, right_sequence_pointer);
        int32_t sps = seqarray_get_sps(right_local_container, right_sequence_pointer);

        // Calculate the required delay
        uint32_t delay = stepper_sps_to_delay(sps);

        // Place the values into the TX FIFO
        // Note: The FIFO is 4x32-bit
        pio_sm_put_blocking(pio[1], sm[1], steps);
        pio_sm_put_blocking(pio[1], sm[1], delay);
        right_sequence_pointer++;
    }

    return true;
}

// Convert Steps Per Second to required PIO clock delay
// The DRV8825 requires a minimum STEP pulse duration of 1.9uS
// so 1.9uS high and 1.9uS low = 3.8uS.  This means we can
// send a maximum of 1,000,000 / 3.8 = 263157 steps/sec
int32_t stepper_sps_to_delay(int32_t sps) {
    float spsf = (float)sps;
    float sys_clock_pps = 125.0 * 1000000.0; // System clock pulses per second (1000000 us per sec)
    float sys_clock_div = 50.0; // System clock divider
    float delay_loop_overhead = 8.0; // The loop overhead in PIO clock ticks

    // Calculate the PIO clock pulse per minute
    float pio_clock_pps = sys_clock_pps / sys_clock_div;

    // Calculate the required delay and compensate for the loop overhead
    // Note: We divide the result by 2 because the delay is used for both
    // the high and low part of the signal (so it's counted twice)
    float required_delay =  (pio_clock_pps / spsf) / 2.0;
    required_delay = required_delay - (delay_loop_overhead / 2.0);

    //printf("Requested SPS = %f - required PIO delay = %f\n", spsf, required_delay);

    return (int32_t)required_delay; // Range check this? 0-4,294,967,295
}

// IRQ called when the pio fifo is not empty, i.e. there are some characters on the uart
// This needs to run as quickly as possible or else you will lose characters (in particular don't printf!)
static void pio_irq_func() {
    if (pio_interrupt_get(pio[0],0)) {
        // Do we have left motor sequence data waiting to send?
        if (left_sequence_pointer < seqarray_get_size(left_local_container)) {
            // Get the steps and SPP (and convert SPP into the PIO delay needed)
            int32_t steps = seqarray_get_steps(left_local_container, left_sequence_pointer);
            uint32_t delay = stepper_sps_to_delay(seqarray_get_sps(left_local_container, left_sequence_pointer));

            // Place the values into the PIO TX FIFO
            pio_sm_put_blocking(pio[0], sm[0], steps);
            pio_sm_put_blocking(pio[0], sm[0], delay);
            
            left_sequence_pointer++;
        } else {
            printf("pio_irq_func(): Left stepper - no more sequence data\n");
            sm_left_busy = false;
        }

        // Clear the interrupt flag
        pio_interrupt_clear(pio[0], 0);
    }

    if (pio_interrupt_get(pio[1],0)) {
        // Do we have right motor sequence data waiting to send?
        if (right_sequence_pointer < seqarray_get_size(right_local_container)) {
            // Get the steps and SPP (and convert SPP into the PIO delay needed)
            int32_t steps = seqarray_get_steps(right_local_container, right_sequence_pointer);
            uint32_t delay = stepper_sps_to_delay(seqarray_get_sps(right_local_container, right_sequence_pointer));

            // Place the values into the PIO TX FIFO
            pio_sm_put_blocking(pio[1], sm[1], steps);
            pio_sm_put_blocking(pio[1], sm[1], delay);
            
            right_sequence_pointer++;
        } else {
            printf("pio_irq_func(): Right stepper - no more sequence data\n");
            sm_right_busy = false;
        }

        // Clear the interrupt flag
        pio_interrupt_clear(pio[1], 0);
    }  
}