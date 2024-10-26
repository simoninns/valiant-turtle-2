#************************************************************************ 
#
#   ina260.py
#
#   INA260 I2C Power Monitor Communication
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

from machine import I2C

# INA260 Registers
_INA260_REG_CONFIG = const(0x00)
_INA260_REG_CURRENT = const(0x01)
_INA260_REG_VOLTAGE = const(0x02)
_INA260_REG_POWER = const(0x03)
_INA260_REG_MASK = const(0x06)
_INA260_REG_ALERT = const(0x07)
_INA260_REG_MANU = const(0xFE)
_INA260_REG_DIE = const(0xFF)

# Expected manufacturer ID and die ID values
_TEXAS_INSTRUMENTS_ID = const(0x5449)
_INA260_ID = const(0x2270)

class Ina260:
    def __init__(self, i2c_bus: I2C, address: int = 0x40):
        self.i2c = i2c_bus
        self.address = address

        # Reg: Config - 16 bit - Set bit 15 = reset
        buffer = bytearray([_INA260_REG_CONFIG, 128, 0])
        self.i2c.writeto(self.address, buffer, True)

        # Verify we are communicating with a valid device
        if (self.manu_id != _TEXAS_INSTRUMENTS_ID):
            raise RuntimeError("INA260::__init__ - INA260 Manufacturer's ID is incorrect - check IC")
        if (self.die_id != _INA260_ID):
            raise RuntimeError("INA260::__init__ - Die ID is incorrect - check IC")

    # Read the current (between V+ and V-) in mA
    @property
    def current(self) -> float:
        buffer = bytearray([_INA260_REG_CURRENT])
        self.i2c.writeto(self.address, buffer, False)
        response = int.from_bytes(self.i2c.readfrom(self.address, 2, True), "big")
        return float(response) * 1.25

    # Read the bus voltage in V
    @property
    def bus_voltage(self) -> float:
        buffer = bytearray([_INA260_REG_VOLTAGE])
        self.i2c.writeto(self.address, buffer, False)
        response = int.from_bytes(self.i2c.readfrom(self.address, 2, True), "big")
        return float(response) * 1.25

    # Read the power being delivered to the load in mW
    @property
    def power(self) -> float:
        buffer = bytearray([_INA260_REG_POWER])
        self.i2c.writeto(self.address, buffer, False)
        response = int.from_bytes(self.i2c.readfrom(self.address, 2, True), "big")
        return float(response) * 10.0

    # Read the manufacturer's ID
    @property
    def manu_id(self) -> int:
        buffer = bytearray([_INA260_REG_MANU])
        self.i2c.writeto(self.address, buffer, False)
        response = int.from_bytes(self.i2c.readfrom(self.address, 2, True), "big")
        return response

    # Read the die ID
    @property
    def die_id(self) -> int:
        buffer = bytearray([_INA260_REG_DIE])
        self.i2c.writeto(self.address, buffer, False)
        response = int.from_bytes(self.i2c.readfrom(self.address, 2, True), "big")
        return response