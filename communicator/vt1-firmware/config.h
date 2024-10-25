/************************************************************************ 

    config.h

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

#ifndef CONFIG_H_
#define CONFIG_H_

// Set the current configuration format version
#define CONFIG_VERSION 1

class Config {
    public:
        // Type definition for turtle configuration
        typedef struct turtle_config_t {
            int32_t turtle_id;
            bool is_version_two;
        } turtle_config_t;

        // Type definition for overall configuration
        typedef struct config_t {
            uint16_t version_number;
            uint8_t number_of_turtles;
            turtle_config_t turtle_config[4];
        } config_t;

        Config(i2c_inst_t *_i2c, uint8_t _eeprom_address);

        config_t read_config_from_eeprom(void);
        void write_config_to_eeprom(void);
        config_t get_config(void);
        void set_config(config_t _config);
        config_t default_config(void);

    private:
        i2c_inst_t *i2c;
	    const uint8_t eeprom_address;

        config_t config;

        uint8_t read_byte(uint16_t address);
        void write_byte(uint16_t address, uint8_t data);

        void read(uint16_t address, uint8_t *data, uint16_t data_length);
        void write(uint16_t address, uint8_t *data, uint16_t data_length);
};

#endif /* CONFIG_H_ */