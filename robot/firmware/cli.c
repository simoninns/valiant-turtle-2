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
#include <stdlib.h>
#include <pico/stdlib.h>
#include "pico/cyw43_arch.h"

// Using embedded CLI library: https://github.com/funbiscuit/embedded-cli
#define EMBEDDED_CLI_IMPL
#include "embedded_cli.h"

#include "ina260.h"
#include "penservo.h"
#include "stepper.h"
#include "velocity.h"
#include "metric.h"
#include "btcomms.h"

#include "cli.h"

// Globals
EmbeddedCli *cli;
bool bluetooth_open;

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
    cli_printf("About:\r\n");
    cli_printf("  Valiant Turtle 2\r\n");
    cli_printf("  (c) 2024 Simon Inns - GPL Open-Source\r\n");
    cli_printf("\r\n");
}

void on_clear_cli(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    cli_printf("\33[2J\r\n");
}

static void on_power(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    
    float current = ina260_read_current();
    float voltage = ina260_read_bus_voltage();
    float power = ina260_read_power();

    cli_printf("INA260 Power information:\r\n");
    cli_printf("  Current: %.2f mA\r\n", current);
    cli_printf("  Bus voltage: %.2f mV\r\n", voltage);
    cli_printf("  Power: %.2f mW\r\n", power);
}

void on_pen(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    const char *arg1 = embeddedCliGetToken(args, 1);
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "up")) {
            cli_printf("Moving the pen servo to the up position\r\n");
            pen_up();
        } else if (!strcmp(arg1, "down")) {
            cli_printf("Moving the pen servo to the down position\r\n");
            pen_down();
        } else if (!strcmp(arg1, "off")) {
            cli_printf("Turning the pen servo off\r\n");
            pen_off();
        } else {
            // Invalid argument
            cli_printf("Pen command invalid argument - Usage: pen [up/down/off]\r\n");
        }
    } else {
        // Missing argument
        cli_printf("Pen command missing argument - Usage: pen [up/down/off]\r\n");
    }
}

void on_stepper_enable(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    stepper_enable(true);
    cli_printf("Stepper motors enabled\r\n");
}

void on_stepper_disable(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    stepper_enable(false);
    cli_printf("Stepper motors disabled\r\n");
}

void on_stepper_velocity(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 5 arguments...
    if (embeddedCliGetTokenCount(args) != 5) {
        // Missing argument
        cli_printf("stepper-velocity command missing argument(s)\r\n");
        cli_printf("  Usage: stepper-velocity [left/right/both] [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]\r\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    stepper_side_t stepper_choice = STEPPER_LEFT;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            stepper_choice = STEPPER_LEFT;
        } else if (!strcmp(arg1, "right")) {
            stepper_choice = STEPPER_RIGHT;
        } else if (!strcmp(arg1, "both")) {
            stepper_choice = STEPPER_BOTH;
        } else {
            // Invalid argument
            cli_printf("stepper-velocity command invalid argument - You must specify left, right or both\n");
            return;
        }
    }

    // Get the rest of the arguments and store as integers
    int32_t accSpsps = atoi(embeddedCliGetToken(args, 2));
    int32_t minimumSps = atoi(embeddedCliGetToken(args, 3));
    int32_t maximumSps = atoi(embeddedCliGetToken(args, 4));
    int32_t updatesPerSecond = atoi(embeddedCliGetToken(args, 5));

    stepper_set_velocity(STEPPER_BOTH, accSpsps, minimumSps, maximumSps, updatesPerSecond);
    cli_printf("Stepper velocity set\r\n");
}

void on_stepper_show(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    
    // Ensure we have 1 argument...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("stepper-show command missing argument(s)\r\n");
        cli_printf("  Usage: stepper-show [left/right/both]\r\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    stepper_side_t stepper_choice = STEPPER_LEFT;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            stepper_choice = STEPPER_LEFT;
        } else if (!strcmp(arg1, "right")) {
            stepper_choice = STEPPER_RIGHT;
        } else if (!strcmp(arg1, "both")) {
            stepper_choice = STEPPER_BOTH;
        } else {
            // Invalid argument
            cli_printf("stepper-show command invalid argument - You must specify left, right or both\n");
            return;
        }
    }

    if (stepper_choice == STEPPER_LEFT || stepper_choice == STEPPER_BOTH) {
        stepper_config_t stepper_config;
        stepper_config = stepper_get_configuration(STEPPER_LEFT);
        cli_printf("Left Stepper parameters:\r\n");
        cli_printf("  Acceleration in Steps per Second per Second = %d\r\n", stepper_config.velocity.accSpsps);
        cli_printf("  Minimum Steps per Second = %d\r\n", stepper_config.velocity.minimumSps);
        cli_printf("  Maximum Steps per Second = %d\r\n", stepper_config.velocity.maximumSps);
        cli_printf("  Updates per second = %d\r\n", stepper_config.velocity.updatesPerSecond);

        if (stepper_config.direction == STEPPER_FORWARDS) {
            cli_printf("  Stepper direction = forwards\r\n");
        } else {
            cli_printf("  Stepper direction = backwards\r\n");
        }

        if (stepper_config.isEnabled) {
            cli_printf("  Stepper enabled = true\r\n");
        } else {
            cli_printf("  Stepper enabled = false\r\n");
        }

        if (stepper_config.isBusy) {
            cli_printf("  Stepper busy = true\r\n");
        } else {
            cli_printf("  Stepper busy = false\r\n");
        }
        
        cli_printf("  Steps remaining = %d\r\n", stepper_config.steps_remaining);
    }

    if (stepper_choice == STEPPER_RIGHT || stepper_choice == STEPPER_BOTH) {
        stepper_config_t stepper_config;
        stepper_config = stepper_get_configuration(STEPPER_RIGHT);
        cli_printf("Right Stepper parameters:\r\n");
        cli_printf("  Acceleration in Steps per Second per Second = %d\r\n", stepper_config.velocity.accSpsps);
        cli_printf("  Minimum Steps per Second = %d\r\n", stepper_config.velocity.minimumSps);
        cli_printf("  Maximum Steps per Second = %d\r\n", stepper_config.velocity.maximumSps);
        cli_printf("  Updates per second = %d\r\n", stepper_config.velocity.updatesPerSecond);

        if (stepper_config.direction == STEPPER_FORWARDS) {
            cli_printf("  Stepper direction = forwards\r\n");
        } else {
            cli_printf("  Stepper direction = backwards\r\n");
        }

        if (stepper_config.isEnabled) {
            cli_printf("  Stepper enabled = true\r\n");
        } else {
            cli_printf("  Stepper enabled = false\r\n");
        }

        if (stepper_config.isBusy) {
            cli_printf("  Stepper busy = true\r\n");
        } else {
            cli_printf("  Stepper busy = false\r\n");
        }
        
        cli_printf("  Steps remaining = %d\r\n", stepper_config.steps_remaining);
    }
}

void on_stepper_steps(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 5 arguments...
    if (embeddedCliGetTokenCount(args) != 2) {
        // Missing argument
        cli_printf("stepper-steps command missing argument(s)\r\n");
        cli_printf("  Usage: stepper-steps [left/right/both] [number of steps]\r\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    stepper_side_t stepper_choice = STEPPER_LEFT;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            stepper_choice = STEPPER_LEFT;
        } else if (!strcmp(arg1, "right")) {
            stepper_choice = STEPPER_RIGHT;
        } else if (!strcmp(arg1, "both")) {
            stepper_choice = STEPPER_BOTH;
        } else {
            // Invalid argument
            cli_printf("stepper-steps command invalid argument - You must specify left, right or both\n");
            return;
        }
    }

    // Check that steppers aren't busy
    if (stepper_isBusy(stepper_choice)) {
        cli_printf("stepper-steps command cannot be used when stepper is busy! - Ignoring\n");
        return;
    }

    // Get the rest of the arguments and store as integers
    int32_t steps = atoi(embeddedCliGetToken(args, 2));

    if (stepper_choice == STEPPER_LEFT || stepper_choice == STEPPER_BOTH) {
        stepper_set_steps(STEPPER_LEFT, steps);
        cli_printf("Stepper left steps set\r\n");
    }

    if (stepper_choice == STEPPER_RIGHT || stepper_choice == STEPPER_BOTH) {
        stepper_set_steps(STEPPER_RIGHT, steps);
        cli_printf("Stepper right steps set\r\n");
    }
}

void on_stepper_dryrun(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 arguments...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("stepper-dryrun command missing argument(s)\r\n");
        cli_printf("  Usage: stepper-dryrun [left/right/both]\r\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    stepper_side_t stepper_choice = STEPPER_LEFT;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            stepper_choice = STEPPER_LEFT;
        } else if (!strcmp(arg1, "right")) {
            stepper_choice = STEPPER_RIGHT;
        } else if (!strcmp(arg1, "both")) {
            stepper_choice = STEPPER_BOTH;
        } else {
            // Invalid argument
            cli_printf("stepper-dryrun command invalid argument - You must specify left, right or both\n");
            return;
        }
    }

    if (stepper_choice == STEPPER_LEFT || stepper_choice == STEPPER_BOTH) {
        if (stepper_get_steps(STEPPER_LEFT) != 0) {
            stepper_dryrun(STEPPER_LEFT);

            velocity_sequence_t* sequence = stepper_get_configuration(STEPPER_LEFT).velocity_sequence;
            if (velocity_get_size(sequence) > 0) {
                int32_t totalSteps = 0;
                int32_t maxSps = 0;

                cli_printf("Left stepper velocity sequence:\r\n");
                cli_printf("  +----------+--------+--------+\r\n");
                cli_printf("  | Interval | Steps  | SPS    |\r\n");
                cli_printf("  +----------+--------+--------+\r\n");

                for (int i = 0; i < velocity_get_size(sequence); i++) { 
                    cli_printf("  | %6d   | %6d | %6d |\r\n", i, velocity_get_steps(sequence, i), velocity_get_sps(sequence, i));

                    totalSteps += velocity_get_steps(sequence, i);
                    if (velocity_get_sps(sequence, i) > maxSps) maxSps = velocity_get_sps(sequence, i);
                }
                cli_printf("  +----------+--------+--------+\r\n");

                cli_printf("\r\n");
                cli_printf("  Maximum achieved SPS: %d\r\n", maxSps); 
                cli_printf("  Total steps: %d\r\n", totalSteps);
                cli_printf("\r\n");
            } else {
                // The sequence is empty
                cli_printf("stepper-dryrun - Left sequence is empty - nothing to display\r\n");
            }

            // Free the sequence
            stepper_dryrun_free(STEPPER_LEFT);
        } else {
            // No steps
            cli_printf("stepper-dryrun - The number of left steps required is 0 - nothing to display\r\n");
        }
    }

    if (stepper_choice == STEPPER_RIGHT || stepper_choice == STEPPER_BOTH) {
        if (stepper_get_steps(STEPPER_RIGHT) != 0) {
            stepper_dryrun(STEPPER_RIGHT);

            velocity_sequence_t* sequence = stepper_get_configuration(STEPPER_RIGHT).velocity_sequence;
            if (velocity_get_size(sequence) > 0) {
                int32_t totalSteps = 0;
                int32_t maxSps = 0;

                cli_printf("Right stepper velocity sequence:\r\n");
                cli_printf("  +----------+--------+--------+\r\n");
                cli_printf("  | Interval | Steps  | SPS    |\r\n");
                cli_printf("  +----------+--------+--------+\r\n");

                for (int i = 0; i < velocity_get_size(sequence); i++) { 
                    cli_printf("  | %6d   | %6d | %6d |\r\n", i, velocity_get_steps(sequence, i), velocity_get_sps(sequence, i));

                    totalSteps += velocity_get_steps(sequence, i);
                    if (velocity_get_sps(sequence, i) > maxSps) maxSps = velocity_get_sps(sequence, i);
                }
                cli_printf("  +----------+--------+--------+\r\n");

                cli_printf("\r\n");
                cli_printf("  Maximum achieved SPS: %d\r\n", maxSps); 
                cli_printf("  Total steps: %d\r\n", totalSteps);
                cli_printf("\r\n");
            } else {
                // The sequence is empty
                cli_printf("stepper-dryrun - Right sequence is empty - nothing to display\r\n");
            }

            // Free the sequence
            stepper_dryrun_free(STEPPER_RIGHT);
        } else {
            // No steps
            cli_printf("stepper-dryrun - The number of right steps required is 0 - nothing to display\r\n");
        }
    }
}

void on_stepper_run(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 arguments...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("stepper-run command missing argument(s)\r\n");
        cli_printf("  Usage: stepper-run [left/right/both]\r\n");
        return;
    }

    const char *arg1 = embeddedCliGetToken(args, 1);
    stepper_side_t stepper_choice = STEPPER_LEFT;
    if (arg1 != NULL) {
        // Argument received
        if (!strcmp(arg1, "left")) {
            stepper_choice = STEPPER_LEFT;
        } else if (!strcmp(arg1, "right")) {
            stepper_choice = STEPPER_RIGHT;
        } else if (!strcmp(arg1, "both")) {
            stepper_choice = STEPPER_BOTH;
        } else {
            // Invalid argument
            cli_printf("stepper-run command invalid argument - You must specify left, right or both\n");
            return;
        }
    }

    // Check that steppers aren't busy
    if (stepper_isBusy(stepper_choice)) {
        cli_printf("stepper-run command cannot be used when stepper is busy! - Ignoring\n");
        return;
    }

    if (stepper_choice == STEPPER_LEFT || stepper_choice == STEPPER_BOTH) {
        if (stepper_get_steps(STEPPER_LEFT) != 0) {
            stepper_run(STEPPER_LEFT);
        } else {
            // No steps
            cli_printf("stepper-run - The number of left steps required is 0 - nothing to do\r\n");
        }
    }

    if (stepper_choice == STEPPER_RIGHT || stepper_choice == STEPPER_BOTH) {
        if (stepper_get_steps(STEPPER_RIGHT) != 0) {
            stepper_run(STEPPER_RIGHT);
        } else {
            // No steps
            cli_printf("stepper-run - The number of right steps required is 0 - nothing to do\r\n");
        }
    }
}

// Metric commands
void on_metric_show(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;
    metric_config_t metric_config = metric_get_config();

    cli_printf("Metric configuration:\r\n");
    cli_printf("  Wheel diameter = %.2fmm\r\n", metric_config.wheel_diameter_mm);
    cli_printf("  Axel distance = %.2fmm\r\n", metric_config.axel_distance_mm);
}

void on_metric_set(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 2 arguments...
    if (embeddedCliGetTokenCount(args) != 2) {
        // Missing argument
        cli_printf("metric-set command missing argument(s)\r\n");
        cli_printf("  Usage: metric-set [wheel diameter in mm] [axel distance in mm]\r\n");
        return;
    }

    // Get the current configuration
    metric_config_t metric_config = metric_get_config();

    // Get the rest of the arguments and store as floats
    metric_config.wheel_diameter_mm = atof(embeddedCliGetToken(args, 1));
    metric_config.axel_distance_mm = atof(embeddedCliGetToken(args, 2));

    metric_set_config(metric_config);
}

void on_metric_forwards(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 argument...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("metric-forwards command missing argument(s)\r\n");
        cli_printf("  Usage: metric-forwards [distance in mm]\r\n");
        return;
    }

    // Check that steppers aren't busy
    if (stepper_isBusy(STEPPER_BOTH)) {
        cli_printf("metric-forwards command cannot be used when steppers are busy! - Ignoring\n");
        return;
    }

    // get the argument and store as float
    float distance_mm = atof(embeddedCliGetToken(args, 1));

    // Get the metric conversion result
    metric_result_t metric_result = metric_forwards(distance_mm);

    // Configure the steppers
    stepper_set_direction(STEPPER_LEFT, metric_result.left_direction);
    stepper_set_steps(STEPPER_LEFT, metric_result.left_steps);
    stepper_set_direction(STEPPER_RIGHT, metric_result.right_direction);
    stepper_set_steps(STEPPER_RIGHT, metric_result.right_steps);

    cli_printf("Steppers configured to move forward %.2f millimeters using %d steps\r\n", distance_mm, metric_result.left_steps);
}

void on_metric_backwards(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 argument...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("metric-backwards command missing argument(s)\r\n");
        cli_printf("  Usage: metric-backwards [distance in mm]\r\n");
        return;
    }

    // Check that steppers aren't busy
    if (stepper_isBusy(STEPPER_BOTH)) {
        cli_printf("metric-backwards command cannot be used when steppers are busy! - Ignoring\n");
        return;
    }

    // get the argument and store as float
    float distance_mm = atof(embeddedCliGetToken(args, 1));

    // Get the metric conversion result
    metric_result_t metric_result = metric_backwards(distance_mm);

    // Configure the steppers
    stepper_set_direction(STEPPER_LEFT, metric_result.left_direction);
    stepper_set_steps(STEPPER_LEFT, metric_result.left_steps);
    stepper_set_direction(STEPPER_RIGHT, metric_result.right_direction);
    stepper_set_steps(STEPPER_RIGHT, metric_result.right_steps);

    cli_printf("Steppers configured to move backward %.2f millimeters using %d steps\r\n", distance_mm, metric_result.left_steps);
}

void on_metric_left(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 argument...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("metric-left command missing argument(s)\r\n");
        cli_printf("  Usage: metric-left [degrees]\r\n");
        return;
    }

    // Check that steppers aren't busy
    if (stepper_isBusy(STEPPER_BOTH)) {
        cli_printf("metric-left command cannot be used when steppers are busy! - Ignoring\n");
        return;
    }

    // get the argument and store as float
    float degrees = atof(embeddedCliGetToken(args, 1));

    // Get the metric conversion result
    metric_result_t metric_result = metric_left(degrees);

    // Configure the steppers
    stepper_set_direction(STEPPER_LEFT, metric_result.left_direction);
    stepper_set_steps(STEPPER_LEFT, metric_result.left_steps);
    stepper_set_direction(STEPPER_RIGHT, metric_result.right_direction);
    stepper_set_steps(STEPPER_RIGHT, metric_result.right_steps);

    cli_printf("Steppers configured to rotate left %.2f degrees using %d steps\r\n", degrees, metric_result.left_steps);
}

void on_metric_right(EmbeddedCli *cli, char *args, void *context) {
    (void)cli;

    // Ensure we have 1 argument...
    if (embeddedCliGetTokenCount(args) != 1) {
        // Missing argument
        cli_printf("metric-right command missing argument(s)\r\n");
        cli_printf("  Usage: metric-right [degrees]\r\n");
        return;
    }

    // Check that steppers aren't busy
    if (stepper_isBusy(STEPPER_BOTH)) {
        cli_printf("metric-right command cannot be used when steppers are busy! - Ignoring\n");
        return;
    }

    // get the argument and store as float
    float degrees = atof(embeddedCliGetToken(args, 1));

    // Get the metric conversion result
    metric_result_t metric_result = metric_right(degrees);

    // Configure the steppers
    stepper_set_direction(STEPPER_LEFT, metric_result.left_direction);
    stepper_set_steps(STEPPER_LEFT, metric_result.left_steps);
    stepper_set_direction(STEPPER_RIGHT, metric_result.right_direction);
    stepper_set_steps(STEPPER_RIGHT, metric_result.right_steps);

    cli_printf("Steppers configured to rotate left %.2f degrees using %d steps\r\n", degrees, metric_result.left_steps);
}

// ------------------------------------------------------------------------

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
    config->maxBindingCount = 24;
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

    CliCommandBinding stepper_velocity_binding = {
            "stepper-velocity",
            "Set the velocity parameters for the stepper motors\r\n\tstepper-velocity [left/right/both] [acceleration SPSPS] [minimum SPS] [maximum SPS] [updates per second]",
            true,
            NULL,
            on_stepper_velocity
    };
    embeddedCliAddBinding(cli, stepper_velocity_binding);

    CliCommandBinding stepper_steps_binding = {
        "stepper-steps",
        "Set the required number of steps for the stepper motors\r\n\tstepper-steps [left/right/both] [steps]",
        true,
        NULL,
        on_stepper_steps
    };
    embeddedCliAddBinding(cli, stepper_steps_binding);

    CliCommandBinding stepper_show_binding = {
            "stepper-show",
            "Show the configuration parameters for the stepper motors\r\n\tstepper-show [left/right/both]",
            true,
            NULL,
            on_stepper_show
    };
    embeddedCliAddBinding(cli, stepper_show_binding);

    CliCommandBinding stepper_dryrun_binding = {
            "stepper-dryrun",
            "Dry run the stepper (shows the calculated velocity sequence)\r\n\tstepper-dryrun [left/right/both]",
            true,
            NULL,
            on_stepper_dryrun
    };
    embeddedCliAddBinding(cli, stepper_dryrun_binding);

    CliCommandBinding stepper_run_binding = {
            "stepper-run",
            "Run the stepper\r\n\tstepper-run [left/right/both])",
            true,
            NULL,
            on_stepper_run
    };
    embeddedCliAddBinding(cli, stepper_run_binding);

    // Metric commands
    CliCommandBinding metric_show_binding = {
            "metric-show",
            "Show the current metric to steps configuration",
            true,
            NULL,
            on_metric_show
    };
    embeddedCliAddBinding(cli, metric_show_binding);

    CliCommandBinding metric_set_binding = {
            "metric-set",
            "Set the current metric to steps configuration\r\n\tmetric-set [wheel diameter in mm] [axel distance in mm]",
            true,
            NULL,
            on_metric_set
    };
    embeddedCliAddBinding(cli, metric_set_binding);

    CliCommandBinding metric_forwards_binding = {
            "metric-forwards",
            "Configure the steppers ready to move the robot forwards a specified number of millimeters\r\n\tmetric-forwards [distance in mm]",
            true,
            NULL,
            on_metric_forwards
    };
    embeddedCliAddBinding(cli, metric_forwards_binding);

    CliCommandBinding metric_backwards_binding = {
            "metric-backwards",
            "Configure the steppers ready to move the robot backwards a specified number of millimeters\r\n\tmetric-backwards [distance in mm]",
            true,
            NULL,
            on_metric_backwards
    };
    embeddedCliAddBinding(cli, metric_backwards_binding);

    CliCommandBinding metric_left_binding = {
            "metric-left",
            "Configure the steppers ready to rotate the robot left a specified number of degrees\r\n\tmetric-left [degrees]",
            true,
            NULL,
            on_metric_left
    };
    embeddedCliAddBinding(cli, metric_left_binding);

    CliCommandBinding metric_right_binding = {
            "metric-right",
            "Configure the steppers ready to rotate the robot right a specified number of degrees\r\n\tmetric-right [degrees]",
            true,
            NULL,
            on_metric_right
    };
    embeddedCliAddBinding(cli, metric_right_binding);

    // Show initial CLI instructions to user
    bluetooth_open = false;
    cli_initial_prompt();

    // Flush the input buffer
    while(getchar_timeout_us(0) != PICO_ERROR_TIMEOUT);

    // Initial process call before triggering on keypresses
    embeddedCliProcess(cli);
}

// Show an initial prompt to the user
void cli_initial_prompt()
{
    cli_printf("\r\n\r\nWelcome to the Valiant Turtle 2 CLI\r\n");
    cli_printf("  Type \"help\" for a list of commands\r\n");
    cli_printf("  Use <Backspace> to remove characters and <TAB> to autocomplete a command\r\n");
    cli_printf("  Use the up and down arrow keys to recall and scroll through previous commands\r\n");
    cli_printf("\r\n");
    cli_printf("VT2> ");
}

// Embedded CLI library requires a write char function
static void write_char_fn(EmbeddedCli *embeddedCli, char c) {
    (void)embeddedCli;

    if (!btcomms_is_channel_open(0)) putchar(c);
    else btcomms_putchar(0, c);
}

// CLI printf function
int cli_printf(const char *fmt, ...) {
    va_list args;
    int ret = 0;

    if (!btcomms_is_channel_open(0)) {
        // The BT SPP channel is closed, so we send cli to stdout
        va_start(args, fmt);
        ret = vfprintf(stdout, fmt, args);
        va_end(args);
    } else {
        // The BT SPP channel is open, so we send debug to channel 1
        va_start(args, fmt);
        char stringBuffer[256];
        ret = vsprintf(stringBuffer, fmt, args);
        va_end(args);

        for (int i=0; i < strlen(stringBuffer); i++) {
            if (stringBuffer[i] == '\n') btcomms_putchar(1, '\r');
            btcomms_putchar(0, stringBuffer[i]);
        }
    }    

    return ret;
}

// Process any waiting characters into the CLI
void cli_process() {
    int c = PICO_ERROR_TIMEOUT;

    // This is the ensure the user sees the initial prompt when
    // connecting via bluetooth SPP
    if (btcomms_is_channel_open(0) && bluetooth_open == false) {
        cli_initial_prompt();
        bluetooth_open = true;
    }

    // If the Bluetooth SPP channel is closed, use stdin
    if (!btcomms_is_channel_open(0)) {
        c = getchar_timeout_us(0);
        bluetooth_open = false;
    } else {
        c = btcomms_getchar(0);
    }

    if (c != PICO_ERROR_TIMEOUT) {
        embeddedCliReceiveChar(cli, c);
        embeddedCliProcess(cli);
    }
}