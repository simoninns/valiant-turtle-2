/************************************************************************ 

    mcp23017.h

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

#ifndef MCP23017_H_
#define MCP23017_H_

#define MCP23017_IODIRA     0x00 // Direction of data I/O port A (bits set as: 1 = input, 0 = output)
#define MCP23017_IODIRB     0x01 // Direction of data I/O port B (bits set as: 1 = input, 0 = output)
#define MCP23017_IPOLA      0x02 // Input polarity register A
#define MCP23017_IPOLB      0x03 // Input polarity register B
#define MCP23017_GPINTENA   0x04 // Interrupt on change A
#define MCP23017_GPINTENB   0x05 // Interrupt on change B
#define MCP23017_DEFVALA    0x06 // Default value register A
#define MCP23017_DEFVALB    0x07 // Default value register B
#define MCP23017_INTCONA    0x08 // Interrupt on change control register A
#define MCP23017_INTCONB    0x09 // Interrupt on change control register B
#define MCP23017_IOCONA     0x0A // IO Control register A
#define MCP23017_IOCONB     0x0B // IO Control register B
#define MCP23017_GPPUA      0x0C // Pull-up set internal pull up for input pins on A
#define MCP23017_GPPUB      0x0D // Pull-up set internal pull up for input pins on B
#define MCP23017_INTFA      0x0E // Interrupt Flag A
#define MCP23017_INTFB      0x0F // Interrupt Flag B
#define MCP23017_INTCAPA    0x10 // Interrupt Capture A
#define MCP23017_INTCAPB    0x11 // Interrupt Capture B
#define MCP23017_GPIOA      0x12 // Port Register A - write modifies latch
#define MCP23017_GPIOB      0x13 // Port Register B - write modifies latch

// I/O configuration (IOCONA/IOCONB) register bits
#define MCP23017_IOCON_BANK_BIT     7
#define MCP23017_IOCON_MIRROR_BIT   6
#define MCP23017_IOCON_SEQOP_BIT    5
#define MCP23017_IOCON_DISSLW_BIT   4
#define MCP23017_IOCON_HAEN_BIT     3
#define MCP23017_IOCON_ODR_BIT      2
#define MCP23017_IOCON_INTPOL_BIT   1

// Define the Pico GPIO that the INTerrupt line is connected to
#define MCP23017_INT_GPIO 10

inline uint16_t set_bit(uint16_t value, int32_t bit, bool set) {
	if (bit >= 0 && bit <= 15) {
		if (set) {
			value |= (1 << bit);
		} else {
			value &= ~(1 << bit);
		}
	}

    return value;
}

inline bool is_bit_set(uint16_t value, int32_t bit) {
	if (bit >= 0 && bit <= 15) {
		return (bool) (0x1 & (value >> bit));
	}
	return false;
}

class Mcp23017 {
    public:
        Mcp23017(i2c_inst_t *_i2c, uint8_t _address);

        // Type for callback functions
        typedef void (*callback_t) (void);

        void configuration(bool mirroring, bool int_polarity);

        void interrupt_enable(int32_t gpio, bool is_interrupting);
        void interrupt_set_default_value(int32_t gpio, bool default_value);
        void interrupt_set_type(int32_t gpio, bool is_default_compared);
        uint16_t interrupt_get_values();
        int32_t interrupt_get_last_gpio();

        bool set_interrupt_callback(callback_t _interrupt_callback);

        void mgpio_set_dir(int32_t gpio, bool is_input);
        void mgpio_pull_up(int32_t gpio);
        void mgpio_disable_pulls(int32_t gpio);
        bool mgpio_get(int32_t gpio);
        void mgpio_put(int32_t gpio, bool value);
        void mgpio_put_all(uint16_t value);
        uint16_t mgpio_get_all(void);

    private:
        i2c_inst_t *i2c;
	    const uint8_t address;

        uint16_t gpio_direction_flags;
        uint16_t gpio_pullup_flags;
        uint16_t gpio_input_flags;
        uint16_t gpio_output_flags;

        uint16_t interrupt_enable_flags;
        uint16_t interrupt_default_values;
        uint16_t interrupt_type;

        callback_t interrupt_callback;
        bool interrupt_callback_set;

        int32_t write_register(uint8_t reg, uint8_t value) const;
        uint8_t read_register(uint8_t reg) const;
        int32_t write_dual_registers(uint8_t reg, uint16_t value) const;
        uint16_t read_dual_registers(uint8_t reg) const;
};

#endif /* MCP23017_H_ */