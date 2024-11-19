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

import logging
from machine import Pin

class Drv8825:
    """
    A class to represent and control a DRV8825 stepper motor driver.
    Attributes
    ----------
    enable : Pin
        GPIO pin to enable or disable the driver.
    m0 : Pin
        GPIO pin for microstepping mode control.
    m1 : Pin
        GPIO pin for microstepping mode control.
    m2 : Pin
        GPIO pin for microstepping mode control.
    Methods
    -------
    set_steps_per_revolution(steps_per_revolution: int):
        Sets the microstepping mode based on the number of steps per revolution.
    set_enable(is_enabled: bool):
        Enables or disables the DRV8825 driver.
    """

    def __init__(self, enable_pin, m0_pin, m1_pin, m2_pin):
        """
        Initialize the DRV8825 stepper motor driver with the given GPIO pins.
        Args:
            enable_pin (int): The GPIO pin number connected to the enable pin of the DRV8825.
            m0_pin (int): The GPIO pin number connected to the M0 pin of the DRV8825.
            m1_pin (int): The GPIO pin number connected to the M1 pin of the DRV8825.
            m2_pin (int): The GPIO pin number connected to the M2 pin of the DRV8825.
        """

        # Configure the GPIOs
        self.enable = Pin(enable_pin, Pin.OUT)
        self.m0 = Pin(m0_pin, Pin.OUT)
        self.m1 = Pin(m1_pin, Pin.OUT)
        self.m2 = Pin(m2_pin, Pin.OUT)

        self.enable.value(0)
        self.m0.value(0)
        self.m1.value(0)
        self.m2.value(0)

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
            self.m0.value(0)
            self.m1.value(0)
            self.m2.value(0)
            logging.debug("Drv8825::set_steps_per_revolution - Full step mode set (200 steps/rev)")
        elif steps_per_revolution == 400: # Half step
            self.m0.value(1)
            self.m1.value(0)
            self.m2.value(0)
            logging.debug("Drv8825::set_steps_per_revolution - Half step mode set (400 steps/rev)")
        elif steps_per_revolution == 800: # 1/4 step
            self.m0.value(0)
            self.m1.value(1)
            self.m2.value(0)
            logging.debug("Drv8825::set_steps_per_revolution - 1/4 step mode set (800 steps/rev)")
        elif steps_per_revolution == 1600: # 1/8 step
            self.m0.value(1)
            self.m1.value(1)
            self.m2.value(0)
            logging.debug("Drv8825::set_steps_per_revolution - 1/8 step mode set (1600 steps/rev)")
        elif steps_per_revolution == 3200: # 1/16 step
            self.m0.value(0)
            self.m1.value(0)
            self.m2.value(1)
            logging.debug("Drv8825::set_steps_per_revolution - 1/16 step mode set (3200 steps/rev)")
        elif steps_per_revolution == 6400: # 1/32 step
            self.m0.value(1)
            self.m1.value(0)
            self.m2.value(1)
            logging.debug("Drv8825::set_steps_per_revolution - 1/32 step mode set (6400 steps/rev)")
        else:
            raise RuntimeError("Drv8825::set_steps_per_revolution - ERROR - Steps per revolution must be 200, 400, 800, 1600, 3200 or 6400")
        
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
            self.enable.value(1)
            logging.debug("Drv8825::set_enable - DRV8825 Enabled")
        else: 
            self.enable.value(0)
            logging.debug("Drv8825::set_enable - DRV8825 Disabled")

if __name__ == "__main__":
    from main import main
    main()