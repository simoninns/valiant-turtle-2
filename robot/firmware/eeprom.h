/************************************************************************ 

    eeprom.h

    Valiant Turtle 2 - Raspberry Pi Pico W Firmware
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

// 24LC16 - 16Kbit EEPROM
// 8 blocks of 256 bits
// 256 * 8 = 2048 bits/block
// 2048 * 8 = 16384 bits

// Address is 1010bbbr
// bbb = block address 000 -> 111
// R = R/!W (1=Read, 0=Write)
//
// So write to block 2 would be:
//   10100100 = 0xA4

#define EEPROM_ADDR 0x50

void eeprom_initialise(void);
uint8_t eeprom_read_byte(uint16_t address);
void eeprom_write_byte(uint16_t address, uint8_t data);

void eeprom_read(uint16_t address, uint8_t *data, uint16_t data_length);
void eeprom_write(uint16_t address, uint8_t *data, uint16_t data_length);

#endif /* EEPROM_H_ */