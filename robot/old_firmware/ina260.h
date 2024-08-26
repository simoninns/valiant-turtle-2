/************************************************************************ 

    ina260.h

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

#ifndef INA260_H_
#define INA260_H_

// INA260 I2C address
#define INA260_ADDR _u(0x40)

// hardware registers
#define INA260_REG_CONFIG _u(0x00)

#define INA260_REG_CURRENT _u(0x01)
#define INA260_REG_VOLTAGE _u(0x02)
#define INA260_REG_POWER _u(0x03)

#define INA260_REG_MASK _u(0x06)
#define INA260_REG_ALERT _u(0x07)
#define INA260_REG_MANU _u(0xfe)
#define INA260_REG_DIE _u(0xff)

// Prototypes
void ina260Initialise(void);
float ina260ReadCurrent(void);
float ina260ReadBusVoltage(void);
float ina260ReadPower(void);
uint16_t ina260ReadManuId(void);
uint16_t ina260ReadDieId(void);

#endif /* INA260_H_ */