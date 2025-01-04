#************************************************************************ 
#
#   configuration.py
#
#   System configuration class with serialization
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

import picolog
import ustruct
from micropython import const

class Configuration:
    CONFIGURATION_VERSION = const(0x03)

    def __init__(self):
        self._configuration_version = 0
        self._linear_target_speed_umps = 0
        self._linear_acceleration_umpss = 0
        self._rotational_target_speed_umps = 0
        self._rotational_acceleration_umpss = 0
        self._wheel_calibration_um = 0
        self._axel_calibration_um = 0
        self._turtle_id = 0

        # Set default configuration
        self.default()

        # ustruct format
        # See: https://docs.micropython.org/en/latest/library/struct.html
        # 8 x int32_t (4 bytes) = 32 bytes
        self.format = 'qqqqqqqq'

    def pack(self) -> bytes:
        buffer = ustruct.pack(self.format,
            int(Configuration.CONFIGURATION_VERSION),
            int(self._linear_target_speed_umps),
            int(self._linear_acceleration_umpss),
            int(self._rotational_target_speed_umps),
            int(self._rotational_acceleration_umpss),
            int(self._wheel_calibration_um),
            int(self._axel_calibration_um),
            int(self._turtle_id),
            )
        return buffer
    
    # Unpack configuration data. Returns:
    # True = EEPROM was valid
    # False = EEPROM was invalid (uses default configuration instead)
    def unpack(self, buffer: bytes) -> bool:
        result = ustruct.unpack(self.format, buffer)

        # Place the resulting tuple into the configuration parameters
        self._configuration_version = result[0]
        self._linear_target_speed_umps = result[1]
        self._linear_acceleration_umpss = result[2]
        self._rotational_target_speed_umps = result[3]
        self._rotational_acceleration_umpss = result[4]
        self._wheel_calibration_um = result[5]
        self._axel_calibration_um = result[6]
        self._turtle_id = result[7]

        # Check configuration is valid
        if self._configuration_version != Configuration.CONFIGURATION_VERSION:
            picolog.info("Configuration::unpack - Configuration invalid... Using default")
            self.default()
            return False

        picolog.info("Configuration::unpack - Configuration valid")
        return True
    
    def default(self):
        self._configuration_version = Configuration.CONFIGURATION_VERSION

        # Linear velocity
        self._linear_target_speed_umps = 200000 # um per second
        self._linear_acceleration_umpss = 4000 # um per second per second

        # Rotational velocity
        self._rotational_target_speed_umps = 100000 # um per second
        self._rotational_acceleration_umpss = 4000 # um per second per second

        # Wheel and axel calibration
        self._wheel_calibration_um = 0 # micrometers
        self._axel_calibration_um = 0 # micrometers

        # Turtle ID
        self._turtle_id = 0

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
    def linear_target_speed_umps(self) -> int:
        return self._linear_target_speed_umps

    @linear_target_speed_umps.setter
    def linear_target_speed_umps(self, value: int):
        if 0 <= value <= 2147483647:
            self._linear_target_speed_umps = value
        else:
            raise ValueError("linear_target_speed_umps must be an integer between 0 and 2,147,483,647")

    @property
    def linear_acceleration_umpss(self) -> int:
        return self._linear_acceleration_umpss

    @linear_acceleration_umpss.setter
    def linear_acceleration_umpss(self, value: int):
        if 0 <= value <= 2147483647:
            self._linear_acceleration_umpss = value
        else:
            raise ValueError("linear_acceleration_umpss must be an integer between 0 and 2,147,483,647")

    @property
    def rotational_target_speed_umps(self) -> int:
        return self._rotational_target_speed_umps

    @rotational_target_speed_umps.setter
    def rotational_target_speed_umps(self, value: int):
        if 0 <= value <= 2147483647:
            self._rotational_target_speed_umps = value
        else:
            raise ValueError("rotational_target_speed_umps must be an integer between 0 and 2,147,483,647")

    @property
    def rotational_acceleration_umpss(self) -> int:
        return self._rotational_acceleration_umpss

    @rotational_acceleration_umpss.setter
    def rotational_acceleration_umpss(self, value: int):
        if 1 <= value <= 2147483647:
            self._rotational_acceleration_umpss = value
        else:
            raise ValueError("rotational_acceleration_umpss must be an integer between 1 and 2,147,483,647")

    @property
    def wheel_calibration_um(self) -> int:
        return self._wheel_calibration_um

    @wheel_calibration_um.setter
    def wheel_calibration_um(self, value: int):
        if -2147483647 <= value <= 2147483647:
            self._wheel_calibration_um = value
        else:
            raise ValueError("wheel_calibration_um must be an integer between -2,147,483,647 and 2,147,483,647")

    @property
    def axel_calibration_um(self) -> int:
        return self._axel_calibration_um

    @axel_calibration_um.setter
    def axel_calibration_um(self, value: int):
        if -2147483647 <= value <= 2147483647:
            self._axel_calibration_um = value
        else:
            raise ValueError("axel_calibration_um must be an integer between -2,147,483,647 and 2,147,483,647")

    @property
    def turtle_id(self) -> int:
        return self._turtle_id

    @turtle_id.setter
    def turtle_id(self, value: int):
        if 0 <= value <= 7:
            self._turtle_id = value
        else:
            raise ValueError("turtle_id must be an integer between 0 and 7")

if __name__ == "__main__":
    from main import main
    main()