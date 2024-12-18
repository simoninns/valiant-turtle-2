#************************************************************************ 
#
#   options.py
#
#   Option headers
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

import library.picolog as picolog
from machine import Pin

class Options:
    def __init__(self, option0_gpio: int, option1_gpio: int, option2_gpio: int):
        # Setup option headers as inputs with pull-up
        self._option0 = Pin(option0_gpio, Pin.IN, Pin.PULL_UP)
        self._option1 = Pin(option1_gpio, Pin.IN, Pin.PULL_UP)
        self._option2 = Pin(option2_gpio, Pin.IN, Pin.PULL_UP)

        # Option headers are only read at startup
        self._option0_value = self._option0.value()
        self._option1_value = self._option1.value()
        self._option2_value = self._option2.value()
    
    def show_options(self):
        picolog.info(f"Options::show_options - Jumpers = Option0: {self.option0}, Option1: {self.option1}, Option2: {self.option2}")

    @property
    def option0(self):
        if self._option0_value == 0:
            return True
        return False
    
    @property
    def option1(self):
        if self._option1_value == 0:
            return True
        return False
    
    @property
    def option2(self):
        if self._option2_value == 0:
            return True
        return False
    
if __name__ == "__main__":
    from main import main
    main()