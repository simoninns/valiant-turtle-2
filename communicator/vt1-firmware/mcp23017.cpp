/************************************************************************ 

    mcp23017.cpp

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

#include "mcp23017.h"
#include "i2c.h"
#include "logging.h"

Mcp23017::Mcp23017(i2c_inst_t *_i2c, uint8_t _address) : i2c(_i2c), address(_address) {
    // Default our local flag representations
    gpio_direction_flags = 0x0000;
    gpio_pullup_flags = 0x0000;
    gpio_input_flags = 0x0000;
    gpio_output_flags = 0x0000;

    interrupt_enable_flags = 0x0000;
    interrupt_default_values = 0x0000;
    interrupt_type = 0x0000;

    // Default the callback flag
    interrupt_callback_set = false;

    // Configure IO Control
    configuration(true, false);

	// Set all pins to output, turn off, turn off all pulls, default interrupts to off
	for (int gp = 0; gp < 16; gp++) {
		mgpio_disable_pulls(gp);
		mgpio_set_dir(gp, false);
		mgpio_put(gp, false);
        interrupt_enable(gp, false);
	}

    int32_t temp = static_cast<int32_t>(address);
    log(log_debug) << "Mcp23017::Mcp23017(): MCP23017 with I2C address 0x" << std::hex << temp << " initialised";
}

// Public configuration methods ---------------------------------------------------------------------------------------

// Set the mirroring and polarity configuration flags
//
// Note: If mirroring is true any GPIO interrupt will set both INTA and INTB
// otherwise INTA is set for an interrupt on GPIOA and INTB for GPIOB
void Mcp23017::configuration(bool mirroring, bool int_polarity) {
	uint8_t io_control_flags = 0x00;
    io_control_flags = set_bit(io_control_flags, MCP23017_IOCON_BANK_BIT, false);
	io_control_flags = set_bit(io_control_flags, MCP23017_IOCON_MIRROR_BIT, mirroring); // INT pins are internally connected
	io_control_flags = set_bit(io_control_flags, MCP23017_IOCON_SEQOP_BIT, false);
	io_control_flags = set_bit(io_control_flags, MCP23017_IOCON_DISSLW_BIT, false);
	io_control_flags = set_bit(io_control_flags, MCP23017_IOCON_HAEN_BIT, false);
	io_control_flags = set_bit(io_control_flags, MCP23017_IOCON_ODR_BIT, false);
	io_control_flags = set_bit(io_control_flags, MCP23017_IOCON_INTPOL_BIT, int_polarity); // INT active-low
    write_register(MCP23017_IOCONA, io_control_flags);
	write_register(MCP23017_IOCONB, io_control_flags);
}

// Public interrupt methods -------------------------------------------------------------------------------------------

// Method to enable and disable interrupts
void Mcp23017::interrupt_enable(int32_t gpio, bool is_set)  {
    if (gpio > 15) gpio = 15;
    interrupt_enable_flags = set_bit(interrupt_enable_flags, gpio, is_set);
    write_dual_registers(MCP23017_GPINTENA, interrupt_enable_flags); // Also writes GPINTENB
}

// Method to set default gpio value (false = 0, true = 1) for interrupt comparison
void Mcp23017::interrupt_set_default_value(int32_t gpio, bool default_value)  {
    if (gpio > 15) gpio = 15;
    interrupt_default_values = set_bit(interrupt_default_values, gpio, default_value);
    write_dual_registers(MCP23017_DEFVALA, interrupt_default_values); // Also writes DEFVALB
}

// Method to configure the interrupt type (false = compare to previous state, true = compare to default value in DEFVAL)
void Mcp23017::interrupt_set_type(int32_t gpio, bool is_default_compared) {
    if (gpio > 15) gpio = 15;
    interrupt_type = set_bit(interrupt_type, gpio, is_default_compared);
    write_dual_registers(MCP23017_INTCONA, interrupt_type); // Also writes INTCONB
}

// Method to get the pin values at the time the last interrupt occurred. Note: this has to be
// read all at once as the read clears the values
//
// From the data-sheet:
// The INTCAP register captures the GPIO port value at the time the interrupt occurred. The register is
// read-only and is updated only when an interrupt occurs. The register remains unchanged until the
// interrupt is cleared via a read of INTCAP or GPIO
//
// Note: Reading this register also clears the INTA or INTB pin of the MCP23017
uint16_t Mcp23017::interrupt_get_values() {
    return read_dual_registers(MCP23017_INTCAPA); // Also reads INTCAPB
}

// Method to get the last gpio that caused an interrupt
//
// From the data-sheet:
// The INTF register reflects the interrupt condition on the port pins of any pin that is enabled for interrupts via the
// GPINTEN register. A set bit indicates that the associated pin caused the interrupt.
// This register is read-only. Writes to this register will be ignored
int32_t Mcp23017::interrupt_get_last_gpio() {
    int32_t int_flag;

	int_flag = read_dual_registers(MCP23017_INTFA); // Also reads INTFB

    // Scan for an interrupt and return the GPIO (pin) number
    for (int pin = 0; pin < 16; pin++) {
        if (is_bit_set(int_flag, pin)) {
            return pin;
        }
    }

    return -1;
}

// Register an interrupt callback
bool Mcp23017::set_interrupt_callback(callback_t _interrupt_callback) {
    // Save the callback procedure
    interrupt_callback = _interrupt_callback;

    // Configure the interrupt GPIO pin (GPIO 10)
    // NOTE: HARDCODED ONLY FOR DEV - FIX THIS!
    gpio_init(MCP23017_INT_GPIO);
    gpio_set_dir(MCP23017_INT_GPIO, GPIO_IN);
    gpio_pull_up(MCP23017_INT_GPIO);

    // Falling edge only IRQ on GPIO
    gpio_set_irq_enabled(MCP23017_INT_GPIO, GPIO_IRQ_EDGE_FALL, true);
	irq_set_exclusive_handler(IO_IRQ_BANK0, interrupt_callback);
	irq_set_priority(IO_IRQ_BANK0, 0);
	irq_set_enabled(IO_IRQ_BANK0, true); 

    // Flag that a callback is set
    interrupt_callback_set = true;

    log(log_debug) << "Mcp23017::set_interrupt_callback(): Interrupt Callback registered";

    return true;
}

// Public GPIO methods ------------------------------------------------------------------------------------------------
void Mcp23017::mgpio_set_dir(int32_t gpio, bool is_input) {
    if (gpio > 15) gpio = 15;
    gpio_direction_flags = set_bit(gpio_direction_flags, gpio, is_input);
    write_dual_registers(MCP23017_IODIRA, gpio_direction_flags); // Also writes IODIRB
}

void Mcp23017::mgpio_pull_up(int32_t gpio) {
    if (gpio > 15) gpio = 15;
    gpio_pullup_flags = set_bit(gpio_pullup_flags, gpio, true);
    write_dual_registers(MCP23017_GPPUA, gpio_pullup_flags); // Also writes GPPUB
}

void Mcp23017::mgpio_disable_pulls(int32_t gpio) {
    if (gpio > 15) gpio = 15;
    gpio_pullup_flags = set_bit(gpio_pullup_flags, gpio, false);
    write_dual_registers(MCP23017_GPPUA, gpio_pullup_flags); // Also writes GPPUB
}

bool Mcp23017::mgpio_get(int32_t gpio) {
    if (gpio > 15) gpio = 15;
    gpio_input_flags = read_dual_registers(MCP23017_GPIOA); // Also reads GPIOB
    return is_bit_set(gpio_input_flags, gpio);
}

void Mcp23017::mgpio_put(int32_t gpio, bool value) {
    if (gpio > 15) gpio = 15;
    gpio_output_flags = set_bit(gpio_output_flags, gpio, value);
    write_dual_registers(MCP23017_GPIOA, gpio_output_flags); // Also writes GPIOB
}

void Mcp23017::mgpio_put_all(uint16_t value) {
    gpio_output_flags = value;
    write_dual_registers(MCP23017_GPIOA, gpio_output_flags); // Also writes GPIOB
}

uint16_t Mcp23017::mgpio_get_all(void) {
    gpio_input_flags = read_dual_registers(MCP23017_GPIOA); // Also reads GPIOB
    return gpio_input_flags;
}

// Private methods ----------------------------------------------------------------------------------------------------
int32_t Mcp23017::write_register(uint8_t reg, uint8_t value) const {
	uint8_t command[] = { reg, value };
	i2c_write_blocking(i2c, address, command, 2, false);
	return 0;
}

uint8_t Mcp23017::read_register(uint8_t reg) const {
	uint8_t buffer = 0;
	i2c_write_blocking(i2c, address,  &reg, 1, true);
	i2c_read_blocking(i2c, address, &buffer, 1, false);

	return buffer;
}

// Write both A and B registers
int32_t Mcp23017::write_dual_registers(uint8_t reg, uint16_t value) const {
	uint8_t command[] = {
			reg,
			static_cast<uint8_t>(value & 0xff),
			static_cast<uint8_t>((value>>8) & 0xff)
	};
	i2c_write_blocking(i2c, address, command, 3, false);

	return 0;
}

// Read both A and B registers
uint16_t Mcp23017::read_dual_registers(uint8_t reg) const {
	uint8_t buffer[2];
	i2c_write_blocking(i2c, address,  &reg, 1, true);
	i2c_read_blocking(i2c, address, buffer, 2, false);

	return static_cast<uint16_t>((buffer[1]<<8) + buffer[0]);
}