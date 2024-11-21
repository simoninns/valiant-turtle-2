#************************************************************************ 
#
#   configuration.py
#
#   System configuration class with serialization
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

import logging
import ustruct

_CONFIGURATION_version = const(0x02)

class Configuration:
    """
    Class to manage the system configuration with serialization.

    Attributes:
        _configuration_version (int): Version of the configuration.
        _is_legacy_mode (bool): Indicates if the system is in legacy mode.
        _serial_speed (int): Serial communication speed.
        _serial_rtscts (bool): Indicates if RTS/CTS flow control is enabled.
        format (str): ustruct format string for packing/unpacking configuration data.
    """

    def __init__(self):
        """
        Initialize the Configuration class and set default configuration.
        """
        # Set default configuration
        self.default()

        # ustruct format
        # See: https://docs.micropython.org/en/latest/library/struct.html
        self.format = 'iiii' # Format: i = 4 byte int

    def pack(self) -> bytes:
        """
        Pack the configuration data into a bytes object.

        Returns:
            bytes: The packed configuration data.
        """
        buffer = ustruct.pack(self.format,
            self._configuration_version,
            int(self._is_legacy_mode),
            self._serial_speed,
            int(self._serial_rtscts)
            )
        return buffer

    def default(self):
        """
        Set the default configuration values.
        """
        self._configuration_version = _CONFIGURATION_version
        self._is_legacy_mode = False
        self._serial_speed = 9600
        self._serial_rtscts = False

    def unpack(self, buffer: bytes):
        """
        Unpack the configuration data from a bytes object.

        Args:
            buffer (bytes): The packed configuration data.
        """
        (self._configuration_version,
         self._is_legacy_mode,
         self._serial_speed,
         self._serial_rtscts) = ustruct.unpack(self.format, buffer)
        self._is_legacy_mode = bool(self._is_legacy_mode)
        self._serial_rtscts = bool(self._serial_rtscts)

    # Return the size (in bytes) of the packed configuration
    @property
    def pack_size(self) -> int:
        return ustruct.calcsize(self.format)

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

if __name__ == "__main__":
    from main import main
    main()