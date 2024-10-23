/************************************************************************ 

    i2c.h

    Valiant Turtle Communicator 2
    Copyright (C) 2024 Simon Inns

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

#ifndef I2C_H_
#define I2C_H_

class I2c {
    public:
        I2c(i2c_inst_t* _i2c_id, uint8_t _sda_gpio, uint8_t _sck_gpio);

    private:
        i2c_inst_t* i2c_id;
        uint8_t sda_gpio;
        uint8_t sck_gpio;
};

#endif /* I2C_H_ */