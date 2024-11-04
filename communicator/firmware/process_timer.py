#************************************************************************ 
#
#   process_timer.py
#
#   Centralised process timer for repetitive tasks
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

from log import log_debug, log_info, log_warn
from machine import Timer

class Process_timer:
    def __init__(self):
        self.period_ms = 10
        self.callbacks = list()

        # Set the one-shot timer
        self.timer = Timer(period=self.period_ms, mode=Timer.ONE_SHOT, callback=self.__timer_callback)
        log_debug("Process_timer::__init__ - Process timer initialised with", self.period_ms,"ms period")

    # Method to register callbacks (to be called when one-shot fires)
    def register_callback(self, callback_function):
        self.callbacks.append(callback_function)
        log_debug("Process_timer::register_callback - Callback registered")

    def __timer_callback(self, t):
        # Call all registered callbacks
        for callback in self.callbacks:
            callback()

        # Set the one-shot timer up again
        self.timer.init(period=self.period_ms, mode=Timer.ONE_SHOT, callback=self.__timer_callback)