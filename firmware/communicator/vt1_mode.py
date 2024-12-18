#************************************************************************ 
#
#   vt1_mode.py
#
#   Original Valiant Turtle Communicator emulation mode
#   Valiant Turtle 2 - Communicator firmware
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

# In legacy mode all communication is 'real-time' as the controller sends
# commands that directly pulse the stepper motors so, if the communicator
# adds delay (say from async handling) the actual robot motion will stutter.
#
# To avoid this, legacy mode works as synchronously as possible to avoid
# introducing unnecessary delay

import library.picolog as picolog
from machine import UART
from leds import Leds
from ir_uart import IrUart
from parallel_port import ParallelPort

class Vt1Mode:
    """
    Class to manage the Valiant Turtle 1 Communicator mode.

    Attributes:
        _uart (UART): UART interface for communication.
        _parallel (Parallel_port): Parallel port interface.
        _ir_uart (Ir_uart): IR UART interface.
        _leds (Leds): LED control interface.
    """

    def __init__(self, uart: UART, parallel: ParallelPort, ir_uart: IrUart, leds: Leds):
        """
        Initialize the Vt1_mode class.

        Args:
            uart (UART): The UART interface for communication.
            parallel (Parallel_port): The parallel port interface.
            ir_uart (Ir_uart): The IR UART interface.
            leds (Leds): The LED control interface.
        """
        self._uart = uart
        self._parallel = parallel
        self._ir_uart = ir_uart
        self._leds = leds

    def process(self):
        """
        Run the VT1 legacy mode process for serial and parallel to IR communication.
        """
        picolog.info("Vt1Mode::process - Running VT1 legacy mode process for serial and parallel to IR")
        self._leds.set_brightness(0, 255) # Power LED on
        self._parallel.auto_ack(False) # Turn off auto-ACK
        
        while True:
            # Send any received parallel port data via IR
            while(self._parallel.any()):
                self._leds.set_brightness(1, 255)
                ch = self._parallel.read(1)[0]
                self._ir_uart.ir_putc(ch)
                self._parallel.ack()
                #picolog.debug("Parallel Rx =", ch)
                self._leds.set_brightness(1, 0)

            # Send any received serial data via IR
            while(self._uart.any()):
                self._leds.set_brightness(1, 255)
                ch = int(self._uart.read(1)[0])
                self._ir_uart.ir_putc(ch)
                #picolog.debug("Serial Rx =", ch)
                self._leds.set_brightness(1, 0)

if __name__ == "__main__":
    from main import main
    main()