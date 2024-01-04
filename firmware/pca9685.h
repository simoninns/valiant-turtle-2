/************************************************************************ 

    pca9685.h

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

#ifndef PCA9685_H_
#define PCA9685_H_

// PCA9685 I2C address
#define PCA9685_ADDR _u(0x40)

// hardware registers
#define PCA9685_REG_CONFIG _u(0x00)
#define PCA9685_REG_CURRENT _u(0x01)

// Prototypes
void pca9685Initialise(void);

#endif /* PCA9685_H_ */