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

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

#include "i2cbus.h"
#include "btcomms.h"

// Initialise the I2C buses
void i2cInitialise(void)
{
    // Initialise I2C interface 0
    i2c_init(i2c0, 100 * 1000);
    gpio_set_function(SDA0_GPIO, GPIO_FUNC_I2C);
    gpio_set_function(SCL0_GPIO, GPIO_FUNC_I2C);
    gpio_pull_up(SDA0_GPIO);
    gpio_pull_up(SCL0_GPIO);

    // Initialise I2C interface 1
    i2c_init(i2c1, 100 * 1000);
    gpio_set_function(SDA1_GPIO, GPIO_FUNC_I2C);
    gpio_set_function(SCL1_GPIO, GPIO_FUNC_I2C);
    gpio_pull_up(SDA1_GPIO);
    gpio_pull_up(SCL1_GPIO);
}

// I2C reserves some addresses for special purposes. We exclude these from the scan.
// These are any addresses of the form 000 0xxx or 111 1xxx
bool i2cReservedAddr(uint8_t addr)
{
    return (addr & 0x78) == 0 || (addr & 0x78) == 0x78;
}

// Scan the I2C bus
void i2cBusScan(uint16_t busNumber)
{
    // Range check
    if (busNumber > 1) busNumber = 1;

    // Show header
    btPrintf("\r\nI2C Bus Scan of bus %d\r\n\r\n", busNumber);
    btPrintf("     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\r\n");

    for (int16_t addr = 0; addr < (1 << 7); ++addr) {
        if (addr % 16 == 0) {
            btPrintf("0x%02x ", addr);
        }

        // Perform a 1-byte dummy read from the probe address. If a slave
        // acknowledges this address, the function returns the number of bytes
        // transferred. If the address byte is ignored, the function returns
        // -1.

        // Skip over any reserved addresses.
        int16_t ret;
        uint8_t rxdata;
        if (i2cReservedAddr(addr)) ret = -1;
        else {
            if (busNumber == 0) ret = i2c_read_blocking(i2c0, addr, &rxdata, 1, false);
            else ret = i2c_read_blocking(i2c1, addr, &rxdata, 1, false);
        }

        btPrintf(ret < 0 ? "." : "@");
        btPrintf(addr % 16 == 15 ? "\r\n" : "  ");
    }
    btPrintf("\r\nScan complete\r\n");
}