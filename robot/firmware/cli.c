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

void on_stepper(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 arguments...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("stepper command missing argument(s)\n");
        cli_printf("  Usage: stepper [enable/disable]\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "enable")) {
            stepconf_set_enable(true);
            cli_printf("Stepper motors enabled\n");
        } else if (!strcmp(arg1, "disable")) {
            stepconf_set_enable(false);
            cli_printf("Stepper motors disabled\n");
        } else {
            // Invalid argument
            cli_printf("stepper command invalid argument - You must specify enable or disable\n");
        }
    }
}

void on_stepper_set(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 5 arguments...
    if (embeddedCliGetTokenCount(args) != 5) {
        // Missing argument
        cli_printf("stepper-set command missing argument(s)\n");
        cli_printf("  Usage: stepper-set [left/right/both] [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    int32_t which_stepper = 0;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            which_stepper = 0;
        } else if (!strcmp(arg1, "right")) {
            which_stepper = 1;
        } else if (!strcmp(arg1, "both")) {
            which_stepper = 2;
        } else {
            // Invalid argument
            cli_printf("stepper-set command invalid argument - You must specify left, right or both\n");
            return;
        }
    }

    // Get the arguments and store as integers
    int32_t accSpsps = atoi(embeddedCliGetToken(args, 2));
    int32_t minimumSps = atoi(embeddedCliGetToken(args, 3));
    int32_t maximumSps = atoi(embeddedCliGetToken(args, 4));
    int32_t updatesPerSecond = atoi(embeddedCliGetToken(args, 5));

    if (which_stepper == 0) {
        stepconf_set_parameters(STEPPER_LEFT, accSpsps, minimumSps, maximumSps, updatesPerSecond);
        cli_printf("Stepper left parameters set\n");
    } else if (which_stepper == 1) {
        stepconf_set_parameters(STEPPER_RIGHT, accSpsps, minimumSps, maximumSps, updatesPerSecond);
        cli_printf("Stepper right parameters set\n");
    } else {
        stepconf_set_parameters(STEPPER_LEFT, accSpsps, minimumSps, maximumSps, updatesPerSecond);
        stepconf_set_parameters(STEPPER_RIGHT, accSpsps, minimumSps, maximumSps, updatesPerSecond);
        cli_printf("Stepper left and right parameters set\n");
    }
}

void on_stepper_show(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 argument...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("stepper-show command missing argument(s)\n");
        cli_printf("  Usage: stepper-show [left/right/both]\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    stepconf_t stepconf;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            stepconf = stepconf_get_parameters(STEPPER_LEFT);
            cli_printf("Left stepper parameters:\n");
            cli_printf("  Acceleration in Steps per Second per Second = %d\n", stepconf.accSpsps);
            cli_printf("  Minimum Steps per Second = %d\n", stepconf.minimumSps);
            cli_printf("  Maximum Steps per Second = %d\n", stepconf.maximumSps);
            cli_printf("  Updates per second = %d\n", stepconf.updatesPerSecond);
        } else if (!strcmp(arg1, "right")) {
            stepconf = stepconf_get_parameters(STEPPER_RIGHT);
            cli_printf("Right stepper parameters:\n");
            cli_printf("  Acceleration in Steps per Second per Second = %d\n", stepconf.accSpsps);
            cli_printf("  Minimum Steps per Second = %d\n", stepconf.minimumSps);
            cli_printf("  Maximum Steps per Second = %d\n", stepconf.maximumSps);
            cli_printf("  Updates per second = %d\n", stepconf.updatesPerSecond);
        } else if (!strcmp(arg1, "both")) {
            stepconf = stepconf_get_parameters(STEPPER_LEFT);
            cli_printf("Left stepper parameters:\n");
            cli_printf("  Acceleration in Steps per Second per Second = %d\n", stepconf.accSpsps);
            cli_printf("  Minimum Steps per Second = %d\n", stepconf.minimumSps);
            cli_printf("  Maximum Steps per Second = %d\n", stepconf.maximumSps);
            cli_printf("  Updates per second = %d\n", stepconf.updatesPerSecond);
            stepconf = stepconf_get_parameters(STEPPER_RIGHT);
            cli_printf("Right stepper parameters:\n");
            cli_printf("  Acceleration in Steps per Second per Second = %d\n", stepconf.accSpsps);
            cli_printf("  Minimum Steps per Second = %d\n", stepconf.minimumSps);
            cli_printf("  Maximum Steps per Second = %d\n", stepconf.maximumSps);
            cli_printf("  Updates per second = %d\n", stepconf.updatesPerSecond);
        } else {
            // Invalid argument
            cli_printf("stepper-set command invalid argument - You must specify left, right or both\n");
            return;
        }
    }
}

void on_stepper_dryrun(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 2 arguments...
    if (embeddedCliGetTokenCount(args) != 2) {
        // Missing argument
        cli_printf("stepper-dryrun command missing argument(s)\n");
        cli_printf("  Usage: stepper-dryrun [left/right] [required number of steps]\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    int32_t which_stepper = 0;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            which_stepper = 0;
        } else if (!strcmp(arg1, "right")) {
            which_stepper = 1;
        } else {
            // Invalid argument
            cli_printf("stepper-dryrun command invalid argument - You must specify left or right\n");
            return;
        }
    }

    // Get the arguments and store as integers
    int32_t requiredSteps = atoi(embeddedCliGetToken(args, 2));
    if (requiredSteps < 1) {
        // Invalid argument
        cli_printf("stepper-dryrun command invalid argument - You must specify 1 or more steps\n");
        return;
    }

    if (which_stepper == 0) {
        stepconf_dryrun(STEPPER_LEFT, requiredSteps);
    } else if (which_stepper == 1) {
        stepconf_dryrun(STEPPER_RIGHT, requiredSteps);
    }
}

void on_stepper_run(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    const char *arg1 = embeddedCliGetToken(args, 1);
    int32_t which_stepper = 0;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            which_stepper = 0;
        } else if (!strcmp(arg1, "right")) {
            which_stepper = 1;
        } else if (!strcmp(arg1, "both")) {
            which_stepper = 2;
        } else {
            // Invalid argument
            cli_printf("stepper-run command invalid argument - You must specify left, right or both\n");
            return;
        }
    }

    if (which_stepper == 0 || which_stepper == 1) {
        // Ensure we have 2 arguments...
        if (embeddedCliGetTokenCount(args) != 2) {
            // Missing argument
            cli_printf("stepper-run command missing argument(s)\n");
            cli_printf("  Usage: stepper-run [left/right/both] [required number of steps]([required number of steps])\n");
            return;
        }
    } else {
        // Ensure we have 3 arguments...
        if (embeddedCliGetTokenCount(args) != 3) {
            // Missing argument
            cli_printf("stepper-run command missing argument(s)\n");
            cli_printf("  Usage: stepper-run [left/right/both] [required number of steps]([required number of steps])\n");
            return;
        }
    }

    // Get the arguments and store as integers
    int32_t requiredSteps1 = atoi(embeddedCliGetToken(args, 2));
    if (requiredSteps1 < 1) {
        // Invalid argument
        cli_printf("stepper-run command invalid argument - You must specify 1 or more steps\n");
        return;
    }

    int32_t requiredSteps2;
    if (which_stepper == 2) {
        requiredSteps2 = atoi(embeddedCliGetToken(args, 3));
        if (requiredSteps2 < 1) {
            // Invalid argument
            cli_printf("stepper-run command invalid argument - You must specify 1 or more steps\n");
            return;
        }
    }

    if (which_stepper == 0) {
        cli_printf("Running left stepper for %d steps\n", requiredSteps1);
        stepconf_run(STEPPER_LEFT, requiredSteps1);
    } else if (which_stepper == 1) {
        cli_printf("Running right stepper for %d steps\n", requiredSteps1);
        stepconf_run(STEPPER_RIGHT, requiredSteps1);
    } else if (which_stepper == 2) {
        cli_printf("Running left stepper for %d steps\n", requiredSteps1);
        cli_printf("Running right stepper for %d steps\n", requiredSteps2);
        stepconf_run(STEPPER_LEFT, requiredSteps1);
        stepconf_run(STEPPER_RIGHT, requiredSteps2);
    }
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

    CliCommandBinding stepper = {
            "stepper",
            "Enable or disable the stepper motors\n\tstepper [enable/disable]",
            true,
            NULL,
            on_stepper
    };
    embeddedCliAddBinding(cli, stepper);

    CliCommandBinding stepper_set_binding = {
            "stepper-set",
            "Set the acc/dec parameters for the stepper motors\n\tstepper-set [left/right/both] [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]",
            true,
            NULL,
            on_stepper_set
    };
    embeddedCliAddBinding(cli, stepper_set_binding);

    CliCommandBinding stepper_show_binding = {
            "stepper-show",
            "Show the acc/dec parameters for the stepper motors\n\tstepper-show [left/right/both]",
            true,
            NULL,
            on_stepper_show
    };
    embeddedCliAddBinding(cli, stepper_show_binding);

    CliCommandBinding stepper_dryrun_binding = {
            "stepper-dryrun",
            "Dry run the stepper (shows the calculated sequence)\n\tstepper-dryrun [left/right] [required number of steps]",
            true,
            NULL,
            on_stepper_dryrun
    };
    embeddedCliAddBinding(cli, stepper_dryrun_binding);

    CliCommandBinding stepper_run_binding = {
            "stepper-run",
            "Run the stepper\n\tstepper-run [left/right/both] [required number of steps]([required number of steps])",
            true,
            NULL,
            on_stepper_run
    };
    embeddedCliAddBinding(cli, stepper_run_binding);

    cli_printf("\n\nCLI is running\n");
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