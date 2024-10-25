/************************************************************************ 

    config.c

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

#include <cstdio>
#include <iostream>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

#include "config.h"
#include "i2c.h"
#include "logging.h"

// Initialise the configuration
Config::Config(i2c_inst_t *_i2c, uint8_t _eeprom_address) : i2c(_i2c), eeprom_address(_eeprom_address) {
    int32_t temp = static_cast<int32_t>(eeprom_address);
    log(log_debug) << "Config::Config(): EEPROM with I2C address 0x" << std::hex << temp << " initialised";

    config = read_config_from_eeprom();
}

Config::config_t Config::read_config_from_eeprom() {
    unsigned char* ptr = (unsigned char*)&config;
    read(0, ptr, sizeof(config));

    if (config.version_number != CONFIG_VERSION)
        log(log_warning) << "Config::read_config_from_eeprom(): Configuration version mismatch - defaulting configuration";
        config = default_config();

    return config;
}

void Config::write_config_to_eeprom() {
    log(log_debug) << "Config::Config(): Writing configuration to EEPROM with address " << eeprom_address;
    unsigned char* ptr = (unsigned char*)&config;
    write(0, ptr, sizeof(config));
}

Config::config_t Config::get_config() {
    return config;
}

void Config::set_config(Config::config_t _config) {
    config = _config;
}

Config::config_t Config::default_config() {
    config_t local_config;
    local_config.version_number = CONFIG_VERSION;
    local_config.number_of_turtles = 1;
    local_config.turtle_config[0].turtle_id = 0;
    local_config.turtle_config[0].is_version_two = true;

    return local_config;
}

// Private methods ----------------------------------------------------------------------------------------------------

// Read a byte from the 24LC16 I2C EEPROM
uint8_t Config::read_byte(uint16_t address) {
    // Ensure the address is not out of bounds
    if ((address) > (256*8)) {
        log(log_error) <<  "Config::read_byte(): Requested address is out of bounds!";
        return 0;
    }

    // Determine the device address (including the block) and intra-block address
    uint8_t device_address = eeprom_address | (address >> 8);
    uint8_t block_address = (address & 0xFF);

    // Perform the read by sending the block, block address and then reading
    // one byte from the device
    uint8_t data;
    i2c_write_blocking(i2c0, device_address, &block_address, 1, true); 
    i2c_read_blocking(i2c0, device_address, &data, 1, false);

    return data;
}

// Write a byte to the 24LC16 I2C EEPROM
void Config::write_byte(uint16_t address, uint8_t data) {
    // Ensure the address is not out of bounds
    if ((address) > (256*8)) {
        log(log_error) <<  "Config::write_byte(): Requested address is out of bounds!";
        return;
    }

    // Determine the device address (including the block) and intra-block address
    uint8_t device_address = eeprom_address | (address >> 8);
    uint8_t block_address = (address & 0xFF);

    uint8_t command[2];
    command[0] = block_address;
    command[1] = data;

    i2c_write_blocking(i2c0, device_address, command, 2, false);
    sleep_us(11000);
}

// Read one or more bytes from the 24LC16 I2C EEPROM
void Config::read(uint16_t address, uint8_t *data, uint16_t data_length) {
        // Ensure the address is not out of bounds
    if ((address+data_length) > (256*8)) {
        log(log_error) <<  "Config::read(): Requested address is out of bounds!";
        return;
    }

    // Determine the device address (including the block) and intra-block address
    uint8_t device_address = eeprom_address | (address >> 8);
    uint8_t block_address = (address & 0xFF);

    // Write the required starting address
    i2c_write_blocking(i2c0, device_address, &block_address, 1, true); 

    // Now read the required data (the whole EEPROM can be read in one command)
    i2c_read_blocking(i2c0, device_address, data, (size_t)data_length, false);
}

// Write one or more bytes to the 24LC16 I2C EEPROM
void Config::write(uint16_t address, uint8_t *data, uint16_t data_length) {
    // Ensure the address is not out of bounds
    if ((address+data_length) > (256*8)) {
        log(log_error) <<  "Config::write(): Requested address is out of bounds!";
        return;
    }

    // Note: The page size of 16 bytes is the maximum we can write in one command...
    int32_t remaining_data = data_length;
    int32_t data_pointer = 0;

    while(remaining_data > 0) {
        // Determine the start address for this page write
        uint8_t device_address = eeprom_address | ((address+data_pointer) >> 8);
        uint8_t block_address = ((address+data_pointer) & 0xFF);

        // Initialise an array to store the start address and a page of data
        uint8_t page[16+1];
        int32_t write_length = 16;

        // If we have less that 16 bytes of remaining data, lower the write length
        if (remaining_data < 16) write_length = remaining_data;

        // If we would cross a block boundary, lower the write length to avoid
        if ((block_address+write_length) > 255) write_length -= (block_address+write_length) - 256;

        // Copy the start address and the data into the page
        page[0] = block_address;
        for (int32_t i=0; i < write_length; i++) {
            page[i+1] = data[data_pointer];
            data_pointer++;
        }

        // Perform a page write
        i2c_write_blocking(i2c0, device_address, page, write_length+1, false);
        sleep_us(11000);

        // Continue if required
        remaining_data -= write_length;
    }
}