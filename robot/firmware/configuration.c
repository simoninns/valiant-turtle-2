/************************************************************************ 

    configuration.c

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

#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"

// Local headers
#include "eeprom.h"
#include "configuration.h"
#include "cli.h"
#include "debug.h"

configuration_t current_configuration;

void configuration_initialise()
{
    // Initialise the EEPROM
    eeprom_initialise();

    // Read the current configuration from EEPROM
    debug_printf("configuration_initialise(): Retrieving current configuration from EEPROM\n");
    current_configuration = configuration_retrieve();
    debug_printf("configuration_initialise(): Turtle ID is %d\r\n", current_configuration.turtle_id);
}

// This returns a configuration object with default parameters
configuration_t configuration_get_default()
{
    configuration_t configuration;

    // Default version number
    configuration.version_number = CONFIG_VERSION;

    // Default metric configuration
    configuration.metric_config.axel_distance_mm = 230.0;
    configuration.metric_config.wheel_diameter_mm = 54.0;
    configuration.metric_config.steps_per_revolution = 800;

    // Default left stepper configuration
    configuration.stepper_left.accSpsps = 2;
    configuration.stepper_left.minimumSps = 2;
    configuration.stepper_left.maximumSps = 800;
    configuration.stepper_left.updatesPerSecond = 8;

    // Default right stepper configuration
    configuration.stepper_right.accSpsps = 2;
    configuration.stepper_right.minimumSps = 2;
    configuration.stepper_right.maximumSps = 800;
    configuration.stepper_right.updatesPerSecond = 8;

    // Default turtle ID
    configuration.turtle_id = 0;

    return configuration;
}

// Get the current configuration
configuration_t configuration_get()
{
    return current_configuration;
}

// Set the current configuration
void configuration_set(configuration_t configuration)
{
    current_configuration = configuration;
    debug_printf("configuration_set(): Configuration updated\n");
}

// Store the passed configuration to EEPROM
void configuration_store(configuration_t configuration)
{
    unsigned char* ptr = (unsigned char*)&configuration;
    eeprom_write(0, ptr, sizeof(configuration));
    debug_printf("configuration_store(): Configuration written to EEPROM in %d bytes\n", sizeof(configuration));
}

// Retrieve the configuration from EEPROM
configuration_t configuration_retrieve()
{
    configuration_t configuration;

    unsigned char* ptr = (unsigned char*)&configuration;
    eeprom_read(0, ptr, sizeof(configuration));

    // Check configuration is valid
    if (configuration.version_number != CONFIG_VERSION) {
        debug_printf("configuration_retrieve(): Configuration version mismatch - reverting to defaults!\n");
        configuration = configuration_get_default();

        // Store the configuration defaults to EEPROM
        configuration_store(configuration);
        debug_printf("configuration_retrieve(): Default configuration written to EEPROM\n");
    } else {
        debug_printf("configuration_retrieve(): Configuration read from EEPROM in %d bytes\n", sizeof(configuration));
    }

    return configuration;
}