
#include <cstdio>
#include <iostream>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

#include "eeprom.h"
#include "i2c.h"

// Initialise the EEPROM
Eeprom::Eeprom(i2c_inst_t *_i2c, uint8_t _eeprom_address) : i2c(_i2c), eeprom_address(_eeprom_address) {
    // Nothing to do here
}

// Read a byte from the 24LC16 I2C EEPROM
uint8_t Eeprom::read_byte(uint16_t address) {
    // Ensure the address is not out of bounds
    if ((address) > (256*8)) {
        std::cerr << "Eeprom::read_byte(): Requested address is out of bounds!" << std::endl;
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
void Eeprom::write_byte(uint16_t address, uint8_t data) {
    // Ensure the address is not out of bounds
    if ((address) > (256*8)) {
        std::cerr << "Eeprom::write_byte(): Requested address is out of bounds!" << std::endl;
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
void Eeprom::read(uint16_t address, uint8_t *data, uint16_t data_length) {
        // Ensure the address is not out of bounds
    if ((address+data_length) > (256*8)) {
        std::cerr << "Eeprom::read(): Requested address is out of bounds!" << std::endl;
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
void Eeprom::write(uint16_t address, uint8_t *data, uint16_t data_length) {
    // Ensure the address is not out of bounds
    if ((address+data_length) > (256*8)) {
        std::cerr << "Eeprom::write(): Requested address is out of bounds!" << std::endl;
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