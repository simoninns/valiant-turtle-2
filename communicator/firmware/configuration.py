#************************************************************************ 
#
#   configuration.py
#
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

class Configuration:
    def __init__(self):
        # Default configuration
        self._configuration_version = 1
        self._is_legacy_mode = True
        self._serial_speed = 4800
        self._serial_rtscts = False

    # Getters and setters for configuration parameters

    # Note: configuration version is read only
    @property
    def configuration_version(self) -> int:
        return self._configuration_version

    @property
    def is_legacy_mode(self) -> bool:
        return self._is_legacy_mode
    
    @is_legacy_mode.setter
    def is_legacy_mode(self, value: bool):
        self._is_legacy_mode = value
    
    @property
    def serial_speed(self) -> int:
        return self._serial_speed
    
    @serial_speed.setter
    def serial_speed(self, value: int):
        self._serial_speed = value
    
    @property
    def serial_rtscts(self) -> bool:
        return self._serial_rtscts
    
    @serial_rtscts.setter
    def serial_rtscts(self, value: bool):
        self._serial_rtscts = value