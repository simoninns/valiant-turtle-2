#************************************************************************ 
#
#   pulse_generator.py
#
#   Stepper motor control (via DRV8825)
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

from machine import Pin
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def pulse_generator():
    wrap_target()
    pull(block)             # Pull (with blocking) FIFO into OSR (first, number of steps)
    mov(x, osr)             # Store the OSR in X

    pull(block)             # Pull (with blocking) FIFO into OSR (second, number of delay cycles)
    mov(y, osr)             # Store the OSR in Y

    irq(rel(0))             # Signal parameters read to CPU (IRQ relative to SM number)

    label("step")
    jmp(not_x, "finished")  # If X == 0 then jump to "finished"
    set(pins, 1)            # Turn pin on

    label("ondelay")
    jmp(y_dec, "ondelay")
    mov(y, osr)             # Restore the Y register (number of delay cycles)

    set(pins, 0)            # Turn pin off

    label("offdelay")
    jmp(y_dec,"offdelay")
    mov(y, osr)             # Restore the Y register (number of delay cycles)

    jmp(x_dec,"step")       # X-- then jump to "step"

    label("finished")
    set(pins, 0)            # Ensure output pin is 0 (not really needed)
    wrap()

class Pulse_generator:
    def __init__(self, state_machine, pin):
        self._sm = rp2.StateMachine(state_machine, pulse_generator, freq=2500000, set_base=Pin(pin))
        self._sm.active(1)

        # I need to add in the IRQ stuff here

        # // Set interrupt for PIO0-SM0 - IRQ 0
        # pio_irq[0] = PIO0_IRQ_0;
        # pio_set_irq0_source_enabled(pulse_generator_pio, pis_interrupt0 , true); // Setting IRQ0_INTE - interrupt enable register
        # irq_set_exclusive_handler(pio_irq[0], pulse_generator_interrupt_handler);  // Set the handler function in the NVIC
        # irq_set_enabled(pio_irq[0], true); // Enabling the PIO0_IRQ_0

        # pulse_generator_program_init(pulse_generator_pio, pulse_generator_sm[0], pulse_generator_offset, PG_GPIO0);

    # Set the pulse generator (and start it running)
    # PPS = Pulses Per Second, pulses = number of pulses to generate
    def set(self, pps, pulses: int):
        pio_delay = self.__pps_to_pio_delay(pps)

        # Place the values into the TX FIFO towards the required state machine
        # Note: The FIFO is 4x32-bit
        #log_debug("Pulse_generator::set: Pulses =", pulses, ", PIO delay =", pio_delay)
        self._sm.put(pulses)
        self._sm.put(pio_delay)

    # Convert pulses per second to the required PIO delay
    def __pps_to_pio_delay(self, pps) -> int:
        # Range check our input
        if pps > 250000:
            log_debug("Pulse_generator::__pps_to_pio_delay: Maximum PPS is 250,000 - limiting!")
            pps = 250000
        
        # The loop overhead in PIO clock ticks
        # Note: This is dependent on the PIO code and will change if the ASM code changes
        delay_loop_overhead = 8.0

        # PIO clock speed in hertz
        pio_clock_pps = 2500000

        # Calculate the required delay and compensate for the loop overhead
        # Note: We divide the result by 2 because the delay is used for both
        # the high and low part of the signal (so it's counted twice)
        required_delay = ((pio_clock_pps / float(pps)) / 2.0) - (delay_loop_overhead / 2.0)

        return int(required_delay)