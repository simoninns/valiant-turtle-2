/************************************************************************ 

    cli.c

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
#include <pico/stdlib.h>
#include "pico/cyw43_arch.h"

// Using embedded CLI library: https://github.com/funbiscuit/embedded-cli
#define EMBEDDED_CLI_IMPL
#include "embedded_cli.h"

#include "ina260.h"

#include "cli.h"

EmbeddedCli *cli;

// ------------------------------------------------------------------------

// This function is called for unknown commands
static void onCommand(const char* name, char *tokens) {
    printf("Received command: %s\r\n",name);

    for (int i = 0; i < embeddedCliGetTokenCount(tokens); ++i) {
        printf("Arg %d : %s\r\n", i, embeddedCliGetToken(tokens, i + 1));
    }
}

static void onAbout(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    printf("About:\n");
    printf("  Valiant Turtle 2\n");
    printf("  (c) 2024 Simon Inns - GPL Open-Source\n");
    printf("\n");
    printf("  CLI library: https://github.com/funbiscuit/embedded-cli\n");
}

static void onPower(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    
    float current = ina260_read_current();
    float voltage = ina260_read_bus_voltage();
    float power = ina260_read_power();

    printf("INA260 Power information:\n");
    printf("  Current: %.2f mA\n", current);
    printf("  Bus voltage: %.2f mV\n", voltage);
    printf("  Power: %.2f mW\n", power);
}

// ------------------------------------------------------------------------

// Embedded CLI library requires a write char function
static void writeCharFn(EmbeddedCli *embeddedCli, char c) {
    (void)embeddedCli;
    putchar(c);
}

// Function is called everytime a CLI command is received
static void onCommandFn(EmbeddedCli *embeddedCli, CliCommand *command) {
    (void)embeddedCli;
    embeddedCliTokenizeArgs(command->args);
    onCommand(command->name == NULL ? "" : command->name, command->args);
}

// Initialise the embedded CLI
void cli_initialise() {
    cli = embeddedCliNewDefault();
    cli->onCommand = onCommandFn;
    cli->writeChar = writeCharFn;

    // Bind our CLI commands to functions
    CliCommandBinding aboutBinding = {
            "about",
            "Show information about this application",
            true,
            NULL,
            onAbout
    };
    embeddedCliAddBinding(cli, aboutBinding);

    CliCommandBinding powerBinding = {
            "power",
            "Show power consumption information from the INA260",
            true,
            NULL,
            onPower
    };
    embeddedCliAddBinding(cli, powerBinding);

    printf("Cli is running\n");
    printf("Type \"help\" for a list of commands\n");
    printf("Use backspace and tab to remove chars and autocomplete\n");
    printf("Use up and down arrows to recall previous commands\n");
}

// Process any waiting characters into the CLI
void cli_process() {
    int c = getchar_timeout_us(0);
    if (c != PICO_ERROR_TIMEOUT) {
        embeddedCliReceiveChar(cli, c);
        embeddedCliProcess(cli);
    }
}