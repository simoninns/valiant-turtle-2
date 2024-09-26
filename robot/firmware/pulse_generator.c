/************************************************************************ 

    pulse_generator.c

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

#include <stdint.h>
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/irq.h"

#include "pulse_generator.h"
#include "pulse_generator.pio.h"
#include "debug.h"

// Globals
static PIO pulse_generator_pio;
static uint pulse_generator_sm[2];
static uint pulse_generator_offset;
static int8_t pio_irq[2];

// Callback global
callback_t registered_callback_sm0;
callback_t registered_callback_sm1;
bool callback_set_sm0;
bool callback_set_sm1;

// Initialise the step generation
void pulse_generator_init()
{
    // Initialise the pulse output GPIOs
    gpio_init(PG_GPIO0);
    gpio_init(PG_GPIO1);

    // Clear the call back registration flags
    callback_set_sm0 = false;
    callback_set_sm1 = false;

    // Start the PIO running
    pulse_generator_pio_start();
}

// Claim PIO, SM and then start the PIOs
// also enables the required interrupts for CPU interaction
void pulse_generator_pio_start()
{
    pulse_generator_pio = pio0;

    // Load PIO 0 and claim SM 0 and 1
    pulse_generator_offset = pio_add_program(pulse_generator_pio, &pulse_generator_program);
    pulse_generator_sm[0] = (int8_t)pio_claim_unused_sm(pulse_generator_pio, false);
    pulse_generator_sm[1] = (int8_t)pio_claim_unused_sm(pulse_generator_pio, false);

    // Set interrupt for PIO0-SM0 - IRQ 0
    pio_irq[0] = PIO0_IRQ_0;
    pio_set_irq0_source_enabled(pulse_generator_pio, pis_interrupt0 , true); // Setting IRQ0_INTE - interrupt enable register
    irq_set_exclusive_handler(pio_irq[0], pulse_generator_interrupt_handler);  // Set the handler function in the NVIC
    irq_set_enabled(pio_irq[0], true); // Enabling the PIO0_IRQ_0

    // Set interrupt for PIO0-SM1 - IRQ 1
    pio_irq[1] = PIO0_IRQ_1;
    pio_set_irq1_source_enabled(pulse_generator_pio, pis_interrupt1 , true); // Setting IRQ0_INTE - interrupt enable register
    irq_set_exclusive_handler(pio_irq[1], pulse_generator_interrupt_handler);  // Set the handler function in the NVIC
    irq_set_enabled(pio_irq[1], true); // Enabling the PIO0_IRQ_1

    pulse_generator_program_init(pulse_generator_pio, pulse_generator_sm[0], pulse_generator_offset, PG_GPIO0);
    pulse_generator_program_init(pulse_generator_pio, pulse_generator_sm[1], pulse_generator_offset, PG_GPIO1);
}

// Stop the PIOs and free the PIOs and SMs
void pulse_generator_pio_stop()
{
    // PIO0-SM0 Disable interrupt
    pio_set_irq0_source_enabled(pulse_generator_pio, pis_interrupt0 , false);
    irq_set_enabled(pio_irq[0], false);
    irq_remove_handler(pio_irq[0], pulse_generator_interrupt_handler);

    // PIO0-SM1 Disable interrupt
    pio_set_irq1_source_enabled(pulse_generator_pio, pis_interrupt1 , false);
    irq_set_enabled(pio_irq[1], false);
    irq_remove_handler(pio_irq[1], pulse_generator_interrupt_handler);

    // Cleanup PIO
    pio_remove_program_and_unclaim_sm(&pulse_generator_program, pulse_generator_pio, pulse_generator_sm[0], pulse_generator_offset);
    pio_remove_program_and_unclaim_sm(&pulse_generator_program, pulse_generator_pio, pulse_generator_sm[1], pulse_generator_offset);
}

// Set the step generator PIO:
// pio_delay must be calculated using pulse_generator_sps_to_pio_delay()
// Steps is the required number of steps
void pulse_generator_set(int32_t sm, int32_t pio_delay, int32_t pulses)
{
    // Place the values into the TX FIFO towards the required state machine
    // Note: The FIFO is 4x32-bit
    pio_sm_put_blocking(pulse_generator_pio, pulse_generator_sm[sm], pulses);
    pio_sm_put_blocking(pulse_generator_pio, pulse_generator_sm[sm], pio_delay);
}

// Convert Pulses Per Second to required PIO clock delay
//
// The DRV8825 requires a minimum STEP pulse duration of 1.9uS
// so 1.9uS high and 1.9uS low = 3.8uS.  This means we can
// send a maximum of 1,000,000 / 3.8 = 263,157 steps/sec
//
// With a clock at 125MHz and a divider of /50 we get
// 250,000 PPS maximum (delay of 1 with a delay overhead of 8 cycles)
// 1 PPS minimum (delay of 1249996);
uint32_t pulse_generator_pps_to_pio_delay(uint32_t pps)
{
    // Range check our input
    if (pps > 250000) {
        debug_printf("step_generator_pps_to_pio_delay(): Maximum PPS is 250,000 - limiting!\n");
        pps = 250000;
    }

    float ppsf = (float)pps;
    float sys_clock_pps = 125.0 * 1000000.0; // System clock pulses per second (1000000 us per sec)
    float sys_clock_div = 50.0; // System clock divider
    float delay_loop_overhead = 8.0; // The loop overhead in PIO clock ticks

    // Calculate the PIO clock pulses per second
    float pio_clock_pps = sys_clock_pps / sys_clock_div;

    // Calculate the required delay and compensate for the loop overhead
    // Note: We divide the result by 2 because the delay is used for both
    // the high and low part of the signal (so it's counted twice)
    float required_delay =  ((pio_clock_pps / ppsf) / 2.0) - (delay_loop_overhead / 2.0);

    // Return the required delay count
    return (int32_t)required_delay;
}

// Function to allow callback registration
void pulse_generator_register_callback(uint8_t sm, callback_t _registered_callback)
{
    if (sm == 0) {
        debug_printf("pulse_generator_register_callback(): Callback registered for sm0\n");
        registered_callback_sm0 = _registered_callback;
        callback_set_sm0 = true;
    } if (sm == 1) {
        debug_printf("pulse_generator_register_callback(): Callback registered for sm1\n");
        registered_callback_sm1 = _registered_callback;
        callback_set_sm1 = true;
    } else {
        debug_printf("pulse_generator_register_callback(): SM number invalid\n");
    }
}

// Handle interrupts from the PIO (this simply calls the 
// registered callback functions for each SM)
static void pulse_generator_interrupt_handler()
{
    // Is State Machine 0 interrupting?
    if (pio_interrupt_get(pulse_generator_pio,0)) {
        // Got interrupt from PIO instance with interrupt number 0
        if (callback_set_sm0) {
            registered_callback_sm0();
        }

        // Clear the interrupt flag
        pio_interrupt_clear(pulse_generator_pio, 0);
    }

    // Is State Machine 1 interrupting?
    if (pio_interrupt_get(pulse_generator_pio,1)) {
        // Got interrupt from PIO instance with interrupt number 1
        if (callback_set_sm1) {
            registered_callback_sm1();
        }

        // Clear the interrupt flag
        pio_interrupt_clear(pulse_generator_pio, 1);
    }
}