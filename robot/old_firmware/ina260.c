/************************************************************************ 

    ina260.c

    Valiant Turtle 2 - Raspberry Pi Pico W Firmware
    Copyright (C) 2023 Simon Inns

    This file is part of Valiant Turtle 2

    This is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Email: simon.inns@gmail.com

************************************************************************/

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

#include "ina260.h"

// INA260 - Precision current and power monitor
// https://www.ti.com/lit/ds/symlink/ina260.pdf

// Initialise the INA260
void ina260Initialise(void)
{
    // Reset
    uint8_t buf[3];
    buf[0] = INA260_REG_CONFIG;
    buf[1] = 128; // MSB Set bit 15 = Reset bit
    buf[2] = 0;   // LSB
    i2c_write_blocking(i2c0, INA260_ADDR, buf, 2, false);

    if (ina260ReadManuId() != 0x5449) printf("Warning: INA260 did not respond with correct manufacturer ID!\r\n");
    if (ina260ReadDieId() != 0x2270) printf("Warning: INA260 did not respond with correct die ID!\r\n");
}

// Return the current measurement in mA
float ina260ReadCurrent(void)
{
    uint8_t buf[2];
    uint8_t reg = INA260_REG_CURRENT;
    i2c_write_blocking(i2c0, INA260_ADDR, &reg, 1, true);  // true to keep master control of bus
    i2c_read_blocking(i2c0, INA260_ADDR, buf, 2, false);  // false - finished with bus
    uint16_t value = (buf[0] << 8) | buf[1];

    return (float)value * 1.25;
}

// Return the bus voltage in mV
float ina260ReadBusVoltage(void)
{
    uint8_t buf[2];
    uint8_t reg = INA260_REG_VOLTAGE;
    i2c_write_blocking(i2c0, INA260_ADDR, &reg, 1, true);  // true to keep master control of bus
    i2c_read_blocking(i2c0, INA260_ADDR, buf, 2, false);  // false - finished with bus
    uint16_t value = (buf[0] << 8) | buf[1];

    return (float)value * 1.25;
}

// Return the power in mW
float ina260ReadPower(void)
{
    uint8_t buf[2];
    uint8_t reg = INA260_REG_POWER;
    i2c_write_blocking(i2c0, INA260_ADDR, &reg, 1, true);  // true to keep master control of bus
    i2c_read_blocking(i2c0, INA260_ADDR, buf, 2, false);  // false - finished with bus
    uint16_t value = (buf[0] << 8) | buf[1];

    return (float)value * 10.0;
}

uint16_t ina260ReadManuId(void)
{
    uint8_t buf[2];

    uint8_t reg = INA260_REG_MANU;
    i2c_write_blocking(i2c0, INA260_ADDR, &reg, 1, true);  // true to keep master control of bus
    i2c_read_blocking(i2c0, INA260_ADDR, buf, 2, false);  // false - finished with bus

    uint16_t value = (buf[0] << 8) | buf[1];

    return value;
}

uint16_t ina260ReadDieId(void)
{
    uint8_t buf[2];

    uint8_t reg = INA260_REG_DIE;
    i2c_write_blocking(i2c0, INA260_ADDR, &reg, 1, true);  // true to keep master control of bus
    i2c_read_blocking(i2c0, INA260_ADDR, buf, 2, false);  // false - finished with bus

    uint16_t value = (buf[0] << 8) | buf[1];

    return value;
}