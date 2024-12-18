#************************************************************************ 
#
#   drv8825.py
#
#   DRV8825 shared stepper controls
#   Valiant Turtle 2 - Robot firmware
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

class Drv8825:
    def __init__(self, enable_pin: Pin, m0_pin: Pin, m1_pin :Pin, m2_pin: Pin):
        """Initializes the DRV8825 driver.
        Parameters:
        enable_pin (Pin): The GPIO pin to enable or disable the driver.
        m0_pin (Pin): The GPIO pin for microstepping mode 0 control.
        m1_pin (Pin): The GPIO pin for microstepping mode 1 control.
        m2_pin (Pin): The GPIO pin for microstepping mode 2 control.
        """

        # Configure the GPIOs
        self._enable_pin = enable_pin
        self._m0_pin = m0_pin
        self._m1_pin = m1_pin
        self._m2_pin = m2_pin

        self._enable_pin.value(0)
        self._m0_pin.value(0)
        self._m1_pin.value(0)
        self._m2_pin.value(0)
        self._steps_per_revolution = 800

        self._is_enabled = False

    @property
    def is_enabled(self):
        return self._is_enabled

    # Set the DRV8825s microstepping mode
    def set_steps_per_revolution(self, steps_per_revolution: int):
        """
        Set the step mode for the DRV8825 stepper motor driver based on the number of steps per revolution.
        Parameters:
        steps_per_revolution (int): The number of steps per revolution. Valid values are:
            - 200 for Full step
            - 400 for Half step
            - 800 for 1/4 step
            - 1600 for 1/8 step
            - 3200 for 1/16 step
            - 6400 for 1/32 step
        Raises:
        RuntimeError: If the steps_per_revolution is not one of the valid values.
        """

        if steps_per_revolution == 200: # Full step
            self._m0_pin.value(0)
            self._m1_pin.value(0)
            self._m2_pin.value(0)
            self._steps_per_revolution = 200
            picolog.debug("Drv8825::set_steps_per_revolution - Full step mode set (200 steps/rev)")
        elif steps_per_revolution == 400: # Half step
            self._m0_pin.value(1)
            self._m1_pin.value(0)
            self._m2_pin.value(0)
            self._steps_per_revolution = 400
            picolog.debug("Drv8825::set_steps_per_revolution - Half step mode set (400 steps/rev)")
        elif steps_per_revolution == 800: # 1/4 step
            self._m0_pin.value(0)
            self._m1_pin.value(1)
            self._m2_pin.value(0)
            self._steps_per_revolution = 800
            picolog.debug("Drv8825::set_steps_per_revolution - 1/4 step mode set (800 steps/rev)")
        elif steps_per_revolution == 1600: # 1/8 step
            self._m0_pin.value(1)
            self._m1_pin.value(1)
            self._m2_pin.value(0)
            self._steps_per_revolution = 1600
            picolog.debug("Drv8825::set_steps_per_revolution - 1/8 step mode set (1600 steps/rev)")
        elif steps_per_revolution == 3200: # 1/16 step
            self._m0_pin.value(0)
            self._m1_pin.value(0)
            self._m2_pin.value(1)
            self._steps_per_revolution = 3200
            picolog.debug("Drv8825::set_steps_per_revolution - 1/16 step mode set (3200 steps/rev)")
        elif steps_per_revolution == 6400: # 1/32 step
            self._m0_pin.value(1)
            self._m1_pin.value(0)
            self._m2_pin.value(1)
            self._steps_per_revolution = 6400
            picolog.debug("Drv8825::set_steps_per_revolution - 1/32 step mode set (6400 steps/rev)")
        else:
            raise RuntimeError("Drv8825::set_steps_per_revolution - ERROR - Steps per revolution must be 200, 400, 800, 1600, 3200 or 6400")
    
    @property
    def steps_per_revolution(self):
        """Return the number of steps per revolution."""
        return self._steps_per_revolution

    # Enable or disable the DRV8825s
    def set_enable(self, is_enabled: bool):
        """
        Enables or disables the DRV8825 driver.
        Args:
            is_enabled (bool): If True, enables the driver. If False, disables the driver.
        Returns:
            None
        """

        if (is_enabled): 
            self._enable_pin.value(1)
            self._is_enabled = True
            picolog.debug("Drv8825::set_enable - DRV8825 Enabled")
        else: 
            self._enable_pin.value(0)
            self._is_enabled = False
            picolog.debug("Drv8825::set_enable - DRV8825 Disabled")

if __name__ == "__main__":
    from main import main
    main()