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
#include <stdlib.h>

// Using embedded CLI library: https://github.com/funbiscuit/embedded-cli
#define EMBEDDED_CLI_IMPL
#include "embedded_cli.h"

#include "ina260.h"
#include "penservo.h"
#include "stepconf.h"

#include "cli.h"

EmbeddedCli *cli;

// ------------------------------------------------------------------------

// This function is called for unknown commands
static void on_command(const char* name, char *tokens) {
    cli_printf("Received unknown command: %s\r\n",name);

    for (int i = 0; i < embeddedCliGetTokenCount(tokens); ++i) {
        cli_printf("Arg %d : %s\r\n", i, embeddedCliGetToken(tokens, i + 1));
    }
}

static void on_about(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    cli_printf("About:\n");
    cli_printf("  Valiant Turtle 2\n");
    cli_printf("  (c) 2024 Simon Inns - GPL Open-Source\n");
    cli_printf("\n");
}

void on_clear_cli(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    cli_printf("\33[2J\n");
}

static void on_power(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    
    float current = ina260_read_current();
    float voltage = ina260_read_bus_voltage();
    float power = ina260_read_power();

    cli_printf("INA260 Power information:\n");
    cli_printf("  Current: %.2f mA\n", current);
    cli_printf("  Bus voltage: %.2f mV\n", voltage);
    cli_printf("  Power: %.2f mW\n", power);
}

void on_pen(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    const char *arg1 = embeddedCliGetToken(args, 1);
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "up")) {
            cli_printf("Moving the pen servo to the up position\n");
            pen_up();
        } else if (!strcmp(arg1, "down")) {
            cli_printf("Moving the pen servo to the down position\n");
            pen_down();
        } else if (!strcmp(arg1, "off")) {
            cli_printf("Turning the pen servo off\n");
            pen_off();
        } else {
            // Invalid argument
            cli_printf("Pen command invalid argument - Usage: pen [up/down/off]\n");
        }
    } else {
        // Missing argument
        cli_printf("Pen command missing argument - Usage: pen [up/down/off]\n");
    }
}

void on_acccalc(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    
    // Ensure we have 5 arguments...
    if (embeddedCliGetTokenCount(args) != 5) {
        // Missing argument
        cli_printf("acccalc command missing argument(s)\n");
        cli_printf("  Usage: acccalc [required steps] [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]\n");
        return;
    }

    // Get the arguments and store as integers
    int32_t requiredSteps = atoi(embeddedCliGetToken(args, 1));
    int32_t accSpsps = atoi(embeddedCliGetToken(args, 2));
    int32_t minimumSps = atoi(embeddedCliGetToken(args, 3));
    int32_t maximumSps = atoi(embeddedCliGetToken(args, 4));
    int32_t updatesPerSecond = atoi(embeddedCliGetToken(args, 5));
}

void on_stepper_enable(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    stepconf_set_enable(true);
}

void on_stepper_disable(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    stepconf_set_enable(false);
}

void on_stepper_set_left(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 4 arguments...
    if (embeddedCliGetTokenCount(args) != 4) {
        // Missing argument
        cli_printf("stepper-set-left command missing argument(s)\n");
        cli_printf("  Usage: stepper-set-left [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]\n");
        return;
    }

    // Get the arguments and store as integers
    int32_t accSpsps = atoi(embeddedCliGetToken(args, 2));
    int32_t minimumSps = atoi(embeddedCliGetToken(args, 3));
    int32_t maximumSps = atoi(embeddedCliGetToken(args, 4));
    int32_t updatesPerSecond = atoi(embeddedCliGetToken(args, 5));

    stepconf_set_parameters(STEPPER_LEFT, accSpsps, minimumSps, maximumSps, updatesPerSecond);
}

void on_stepper_set_right(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 4 arguments...
    if (embeddedCliGetTokenCount(args) != 4) {
        // Missing argument
        cli_printf("stepper-set-right command requires 4 argument(s)\n");
        cli_printf("  Usage: stepper-set-right [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]\n");
        return;
    }

    // Get the arguments and store as integers
    int32_t accSpsps = atoi(embeddedCliGetToken(args, 1));
    int32_t minimumSps = atoi(embeddedCliGetToken(args, 2));
    int32_t maximumSps = atoi(embeddedCliGetToken(args, 3));
    int32_t updatesPerSecond = atoi(embeddedCliGetToken(args, 4));

    stepconf_set_parameters(STEPPER_RIGHT, accSpsps, minimumSps, maximumSps, updatesPerSecond);
}

void on_stepper_set_both(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 4 arguments...
    if (embeddedCliGetTokenCount(args) != 4) {
        // Missing argument
        cli_printf("stepper-set-both command requires 4 argument(s)\n");
        cli_printf("  Usage: stepper-set-both [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]\n");
        return;
    }

    // Get the arguments and store as integers
    int32_t accSpsps = atoi(embeddedCliGetToken(args, 1));
    int32_t minimumSps = atoi(embeddedCliGetToken(args, 2));
    int32_t maximumSps = atoi(embeddedCliGetToken(args, 3));
    int32_t updatesPerSecond = atoi(embeddedCliGetToken(args, 4));

    stepconf_set_parameters(STEPPER_LEFT, accSpsps, minimumSps, maximumSps, updatesPerSecond);
    stepconf_set_parameters(STEPPER_RIGHT, accSpsps, minimumSps, maximumSps, updatesPerSecond);
}

void on_stepper_show_left(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    stepconf_t stepconf = stepconf_get_parameters(STEPPER_LEFT);
    cli_printf("Left stepper parameters:\n");
    cli_printf(" Acceleration in Steps per Second per Second = %d\n", stepconf.accSpsps);
    cli_printf(" Minimum Steps per Second = %d\n", stepconf.minimumSps);
    cli_printf(" Maximum Steps per Second = %d\n", stepconf.maximumSps);
    cli_printf(" Updates per second = %d\n", stepconf.updatesPerSecond);
}

void on_stepper_show_right(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    stepconf_t stepconf = stepconf_get_parameters(STEPPER_LEFT);
    cli_printf("Right stepper parameters:\n");
    cli_printf(" Acceleration in Steps per Second per Second = %d\n", stepconf.accSpsps);
    cli_printf(" Minimum Steps per Second = %d\n", stepconf.minimumSps);
    cli_printf(" Maximum Steps per Second = %d\n", stepconf.maximumSps);
    cli_printf(" Updates per second = %d\n", stepconf.updatesPerSecond);
}

// ------------------------------------------------------------------------

// Embedded CLI library requires a write char function
static void write_char_fn(EmbeddedCli *embeddedCli, char c) {
    (void)embeddedCli;
    putchar(c);
}

void cli_printf(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    vfprintf(stdout, fmt, args);
    va_end(args);
}

// Function is called every time a CLI command is received
static void on_command_fn(EmbeddedCli *embeddedCli, CliCommand *command) {
    (void)embeddedCli;
    embeddedCliTokenizeArgs(command->args);
    on_command(command->name == NULL ? "" : command->name, command->args);
}

// Initialise the embedded CLI
void cli_initialise() {
    EmbeddedCliConfig *config = embeddedCliDefaultConfig();
    // config->cliBuffer = cliBuffer;
    // config->cliBufferSize = CLI_BUFFER_SIZE;
    // config->rxBufferSize = CLI_RX_BUFFER_SIZE;
    // config->cmdBufferSize = CLI_CMD_BUFFER_SIZE;
    // config->historyBufferSize = CLI_HISTORY_SIZE;
    config->maxBindingCount = 16;

    cli = embeddedCliNew(config);
    cli->onCommand = on_command_fn;
    cli->writeChar = write_char_fn;

    // Bind our CLI commands to functions
    CliCommandBinding about_binding = {
            "about",
            "Show information about this application",
            true,
            NULL,
            on_about
    };
    embeddedCliAddBinding(cli, about_binding);

    CliCommandBinding clear_binding = {
            "clear",
            "Clears the console",
            true,
            NULL,
            on_clear_cli
    };
    embeddedCliAddBinding(cli, clear_binding);

    CliCommandBinding power_binding = {
            "power",
            "Show power consumption information from the INA260",
            true,
            NULL,
            on_power
    };
    embeddedCliAddBinding(cli, power_binding);

    CliCommandBinding pen_binding = {
            "pen",
            "Control the pen servo\n\tpen [up/down/off]",
            true,
            NULL,
            on_pen
    };
    embeddedCliAddBinding(cli, pen_binding);

    CliCommandBinding acccalc_binding = {
            "acccalc",
            "Calculate an acceleration/deceleration sequence",
            true,
            NULL,
            on_acccalc
    };
    embeddedCliAddBinding(cli, acccalc_binding);

    CliCommandBinding stepper_enable = {
            "stepper-enable",
            "Enable the stepper motors",
            true,
            NULL,
            on_stepper_enable
    };
    embeddedCliAddBinding(cli, stepper_enable);

    CliCommandBinding stepper_disable = {
            "stepper-disable",
            "Disable the stepper motors",
            true,
            NULL,
            on_stepper_disable
    };
    embeddedCliAddBinding(cli, stepper_disable);

    CliCommandBinding stepper_set_left_binding = {
            "stepper-set-left",
            "Set the acc/dec parameters for the left stepper motor\n\tstepper-set-left [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]",
            true,
            NULL,
            on_stepper_set_left
    };
    embeddedCliAddBinding(cli, stepper_set_left_binding);

    CliCommandBinding stepper_set_right_binding = {
            "stepper-set-right",
            "Set the acc/dec parameters for the left stepper motor\n\tstepper-set-right [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]",
            true,
            NULL,
            on_stepper_set_right
    };
    embeddedCliAddBinding(cli, stepper_set_right_binding);

    CliCommandBinding stepper_show_left_binding = {
            "stepper-show-left",
            "Show the acc/dec parameters for the left stepper motor",
            true,
            NULL,
            on_stepper_show_left
    };
    embeddedCliAddBinding(cli, stepper_show_left_binding);

    CliCommandBinding stepper_show_right_binding = {
            "stepper-show-right",
            "Show the acc/dec parameters for the right stepper motor",
            true,
            NULL,
            on_stepper_show_right
    };
    embeddedCliAddBinding(cli, stepper_show_right_binding);

    CliCommandBinding stepper_set_both_binding = {
            "stepper-set-both",
            "Set the acc/dec parameters for the both stepper motors\n\tstepper-set-both [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]",
            true,
            NULL,
            on_stepper_set_both
    };
    embeddedCliAddBinding(cli, stepper_set_both_binding);

    cli_printf("CLI is running\n");
    cli_printf("Type \"help\" for a list of commands\n");
    cli_printf("Use backspace and tab to remove chars and autocomplete\n");
    cli_printf("Use up and down arrows to recall previous commands\n");
}

// Process any waiting characters into the CLI
void cli_process() {
    int c = getchar_timeout_us(0);
    if (c != PICO_ERROR_TIMEOUT) {
        embeddedCliReceiveChar(cli, c);
        embeddedCliProcess(cli);
    }
}