/************************************************************************ 

    eeprom.h

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

#ifndef EEPROM_H_
#define EEPROM_H_

class Eeprom {
    public:
        Eeprom(i2c_inst_t *_i2c, uint8_t _eeprom_address);

        uint8_t read_byte(uint16_t address);
        void write_byte(uint16_t address, uint8_t data);

        void read(uint16_t address, uint8_t *data, uint16_t data_length);
        void write(uint16_t address, uint8_t *data, uint16_t data_length);

    private:
        i2c_inst_t *i2c;
	    const uint8_t eeprom_address;
};

#endif /* EEPROM_H_ */