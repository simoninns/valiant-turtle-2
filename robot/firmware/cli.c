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
#include "btcomms.h"
#include "fifo.h"
#include "metricmotion.h"

#include "cli.h"

EmbeddedCli *cli;

// ------------------------------------------------------------------------

// This function is called for unknown commands
static void on_command(const char* name, char *tokens) {
    btcomms_printf("Received unknown command: %s\r\n",name);

    for (int i = 0; i < embeddedCliGetTokenCount(tokens); ++i) {
        btcomms_printf("Arg %d : %s\r\n", i, embeddedCliGetToken(tokens, i + 1));
    }
}

static void on_about(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    btcomms_printf("About:\r\n");
    btcomms_printf("  Valiant Turtle 2\r\n");
    btcomms_printf("  (c) 2024 Simon Inns - GPL Open-Source\r\n");
    btcomms_printf("\r\n");
}

void on_clear_cli(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    btcomms_printf("\33[2J\r\n");
}

static void on_power(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    
    float current = ina260_read_current();
    float voltage = ina260_read_bus_voltage();
    float power = ina260_read_power();

    btcomms_printf("INA260 Power information:\r\n");
    btcomms_printf("  Current: %.2f mA\r\n", current);
    btcomms_printf("  Bus voltage: %.2f mV\r\n", voltage);
    btcomms_printf("  Power: %.2f mW\r\n", power);
}

void on_pen(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    const char *arg1 = embeddedCliGetToken(args, 1);
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "up")) {
            btcomms_printf("Moving the pen servo to the up position\r\n");
            pen_up();
        } else if (!strcmp(arg1, "down")) {
            btcomms_printf("Moving the pen servo to the down position\r\n");
            pen_down();
        } else if (!strcmp(arg1, "off")) {
            btcomms_printf("Turning the pen servo off\r\n");
            pen_off();
        } else {
            // Invalid argument
            btcomms_printf("Pen command invalid argument - Usage: pen [up/down/off]\r\n");
        }
    } else {
        // Missing argument
        btcomms_printf("Pen command missing argument - Usage: pen [up/down/off]\r\n");
    }
}

void on_stepper_enable(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    stepconf_set_enable(true);
    btcomms_printf("Stepper motors enabled\r\n");
}

void on_stepper_disable(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    stepconf_set_enable(false);
    btcomms_printf("Stepper motors disabled\r\n");
}

void on_stepper_set(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 4 arguments...
    if (embeddedCliGetTokenCount(args) != 4) {
        // Missing argument
        btcomms_printf("stepper-set command missing argument(s)\r\n");
        btcomms_printf("  Usage: stepper-set [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]\r\n");
        return;
    }

    // Get the arguments and store as integers
    int32_t accSpsps = atoi(embeddedCliGetToken(args, 1));
    int32_t minimumSps = atoi(embeddedCliGetToken(args, 2));
    int32_t maximumSps = atoi(embeddedCliGetToken(args, 3));
    int32_t updatesPerSecond = atoi(embeddedCliGetToken(args, 4));

    stepconf_set_parameters(accSpsps, minimumSps, maximumSps, updatesPerSecond);
    btcomms_printf("Stepper parameters set\r\n");
}

void on_stepper_show(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    stepconf_t stepconf;

    stepconf = stepconf_get_parameters();
    btcomms_printf("Stepper parameters:\r\n");
    btcomms_printf("  Acceleration in Steps per Second per Second = %d\r\n", stepconf.accSpsps);
    btcomms_printf("  Minimum Steps per Second = %d\r\n", stepconf.minimumSps);
    btcomms_printf("  Maximum Steps per Second = %d\r\n", stepconf.maximumSps);
    btcomms_printf("  Updates per second = %d\r\n", stepconf.updatesPerSecond);
}

void on_stepper_dryrun(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 arguments...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        btcomms_printf("stepper-dryrun command missing argument(s)\r\n");
        btcomms_printf("  Usage: stepper-dryrun [required number of steps]\r\n");
        return;
    }

    // Get the arguments and store as integers
    int32_t requiredSteps = atoi(embeddedCliGetToken(args, 1));
    if (requiredSteps < 1) {
        // Invalid argument
        btcomms_printf("stepper-dryrun command invalid argument - You must specify 1 or more steps\r\n");
        return;
    }

    stepconf_dryrun(requiredSteps);
}

void on_stepper_run(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 argument...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        btcomms_printf("stepper-run command missing argument(s)\r\n");
        btcomms_printf("  Usage: stepper-run [required number of steps]\r\n");
        return;
    }

    // Get the arguments and store as integers
    int32_t requiredSteps = atoi(embeddedCliGetToken(args, 1));
    if (requiredSteps < 1) {
        // Invalid argument
        btcomms_printf("stepper-run command invalid argument - You must specify 1 or more steps\r\n");
        return;
    }

    btcomms_printf("Running stepper for %d steps\r\n", requiredSteps);
    stepconf_run(requiredSteps);
}

// Metric motion commands
void on_forwards(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 arguments...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        btcomms_printf("forward command missing argument\r\n");
        btcomms_printf("  Usage: forwards [number of millimeters]\r\n");
        return;
    }

    int32_t millimeters = atoi(embeddedCliGetToken(args, 1));
    if (millimeters < 1) {
        // Invalid argument
        btcomms_printf("forwards command invalid argument - You must specify 1 or more millimeters\r\n");
        return;
    }

    // Perform command
    btcomms_printf("Moving forwards %d millimeters\r\n", millimeters);
    metricmotion_forwards(millimeters);
}

void on_backwards(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 arguments...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        btcomms_printf("backward command missing argument\r\n");
        btcomms_printf("  Usage: backwards [number of millimeters]\r\n");
        return;
    }

    int32_t millimeters = atoi(embeddedCliGetToken(args, 1));
    if (millimeters < 1) {
        // Invalid argument
        btcomms_printf("backwards command invalid argument - You must specify 1 or more millimeters\r\n");
        return;
    }

    // Perform command
    btcomms_printf("Moving backwards %d millimeters\r\n", millimeters);
    metricmotion_backwards(millimeters);
}

void on_left(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 arguments...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        btcomms_printf("left command missing argument\r\n");
        btcomms_printf("  Usage: left [number of degrees]\r\n");
        return;
    }

    int32_t degrees = atoi(embeddedCliGetToken(args, 1));
    if (degrees < 1) {
        // Invalid argument
        btcomms_printf("left command invalid argument - You must specify 1 or more degrees\r\n");
        return;
    }

    // Perform command
    btcomms_printf("Turning left %d degrees\r\n", degrees);
    metricmotion_left(degrees);
}

void on_right(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 arguments...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        btcomms_printf("right command missing argument\r\n");
        btcomms_printf("  Usage: right [number of degrees]\r\n");
        return;
    }

    int32_t degrees = atoi(embeddedCliGetToken(args, 1));
    if (degrees < 1) {
        // Invalid argument
        btcomms_printf("right command invalid argument - You must specify 1 or more degrees\r\n");
        return;
    }

    // Perform command
    btcomms_printf("Turning right %d degrees\r\n", degrees);
    metricmotion_right(degrees);
}

// ------------------------------------------------------------------------

// Embedded CLI library requires a write char function
static void write_char_fn(EmbeddedCli *embeddedCli, char c) {
    (void)embeddedCli;
    //putchar(c);
    fifo_out_write(c);
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
    // config->rxBufferSize = 64;
    // config->cmdBufferSize = 64;
    // config->historyBufferSize = 128;
    // config->cliBuffer = NULL;
    // config->cliBufferSize = 0;
    // config->maxBindingCount = 8;
    // config->enableAutoComplete = true;
    config->maxBindingCount = 16;
    config->invitation = "VT2> ";

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
            "Control the pen servo\r\n\tpen [up/down/off]",
            true,
            NULL,
            on_pen
    };
    embeddedCliAddBinding(cli, pen_binding);

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

    CliCommandBinding stepper_set_binding = {
            "stepper-set",
            "Set the acc/dec parameters for the stepper motors\r\n\tstepper-set [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]",
            true,
            NULL,
            on_stepper_set
    };
    embeddedCliAddBinding(cli, stepper_set_binding);

    CliCommandBinding stepper_show_binding = {
            "stepper-show",
            "Show the acc/dec parameters for the stepper motors\r\n\tstepper-show",
            true,
            NULL,
            on_stepper_show
    };
    embeddedCliAddBinding(cli, stepper_show_binding);

    CliCommandBinding stepper_dryrun_binding = {
            "stepper-dryrun",
            "Dry run the stepper (shows the calculated sequence)\r\n\tstepper-dryrun [required number of steps]",
            true,
            NULL,
            on_stepper_dryrun
    };
    embeddedCliAddBinding(cli, stepper_dryrun_binding);

    CliCommandBinding stepper_run_binding = {
            "stepper-run",
            "Run the stepper\r\n\tstepper-run [required number of steps]([required number of steps])",
            true,
            NULL,
            on_stepper_run
    };
    embeddedCliAddBinding(cli, stepper_run_binding);

    // Metric motion commands
    CliCommandBinding forwards_binding = {
            "forwards",
            "Move forwards the specified number of millimeters\r\n\tforwards [number of millimeters]",
            true,
            NULL,
            on_forwards
    };
    embeddedCliAddBinding(cli, forwards_binding);

    CliCommandBinding backwards_binding = {
            "backwards",
            "Move backwards the specified number of millimeters\r\n\tbackwards [number of millimeters]",
            true,
            NULL,
            on_backwards
    };
    embeddedCliAddBinding(cli, backwards_binding);

    CliCommandBinding left_binding = {
            "left",
            "Turn left the specified number of degrees\r\n\tleft [number of degrees]",
            true,
            NULL,
            on_left
    };
    embeddedCliAddBinding(cli, left_binding);

    CliCommandBinding right_binding = {
            "right",
            "Turn right the specified number of degrees\r\n\tright [number of degrees]",
            true,
            NULL,
            on_right
    };
    embeddedCliAddBinding(cli, right_binding);

    // Show initial CLI instructions to user
    btcomms_printf("\r\n\r\nWelcome to the Valiant Turtle 2 CLI\r\n");
    btcomms_printf("  Type \"help\" for a list of commands\r\n");
    btcomms_printf("  Use <Backspace> to remove characters and <TAB> to autocomplete a command\r\n");
    btcomms_printf("  Use the up and down arrow keys to recall and scroll through previous commands\r\n");
    btcomms_printf("\r\n");
}

// Process any waiting characters into the CLI
void cli_process() {
    //int c = getchar_timeout_us(0);
    int c = fifo_in_read(); // Get input from BT
    if (c != PICO_ERROR_TIMEOUT) {
        embeddedCliReceiveChar(cli, c);
        embeddedCliProcess(cli);
    }
}