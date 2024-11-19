#************************************************************************ 
#
#   robot_comms.py
#
#   Classes for robot communications
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

class Battery:
    def __init__(self, voltage_mV: float = 0, current_mA: float = 0, power_mW: float = 0):
        """Class to store battery status information"""
        self._voltage_mV = voltage_mV
        self._current_mA = current_mA
        self._power_mW = power_mW

    @property
    def voltage_mV(self):
        """Get the battery voltage in mV"""
        return  self._voltage_mV
    
    @property
    def voltage_mV_fstring(self) -> str:
        """Get the battery voltage as a formatted string"""
        return "{:.2f} mV".format(self._voltage_mV)
    
    @property
    def current_mA(self):
        """Get the battery current in mA"""
        return  self._current_mA
    
    @property
    def current__mA_fstring(self) -> str:
        """Get the battery current as a formatted string"""
        return "{:.2f} mA".format(self._current_mA)
    
    @property
    def power_mW(self):
        """Get the battery power in mW"""
        return  self._power_mW
    
    @property
    def power__mW_fstring(self) -> str:
        """Get the battery power as a formatted string"""
        return "{:.2f} mW".format(self._power_mW)

    @voltage_mV.setter
    def voltage_mV(self, value):
        """Set the battery voltage in mV"""
        self._voltage_mV = value

    @current_mA.setter
    def current_mA(self, value):
        """Set the battery current in mA"""
        self._current_mA = value

    @power_mW.setter
    def voltage_mV(self, value):
        """Set the battery power in mW"""
        self._power_mW = value

    @property
    def status(self):
        """Get the battery status as a tuple containing voltage, current and power (mV, mA, mW)"""
        return (self._voltage_mV, self._current_mA, self._power_mW)

    @status.setter
    def status(self, values):
        """Set the battery status as a tuple containing voltage, current and power (mV, mA, mW)"""
        self._voltage_mV, self._current_mA, self._power_mW = values

if __name__ == "__main__":
    from main import main
    main()