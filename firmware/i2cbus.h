/************************************************************************ 

    i2cbus.h

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

#ifndef I2CBUS_H_
#define I2CBUS_H_

#define SDA0_GPIO 8
#define SCL0_GPIO 9
#define SDA1_GPIO 10
#define SCL1_GPIO 11

// Function prototypes
void i2cInitialise(void);
bool i2cReservedAddr(uint8_t addr);
void i2cBusScan(uint16_t busNumber);

#endif /* I2CBUS_H_ */