/************************************************************************ 

    cli.h

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

#ifndef CLI_H_
#define CLI_H_

#include "embedded_cli.h"

static void on_command(const char* name, char *tokens);

static void on_about(EmbeddedCli *cli, char *args, void *context);
static void on_clear_cli(EmbeddedCli *cli, char *args, void *context);
static void on_power(EmbeddedCli *cli, char *args, void *context);
static void on_pen(EmbeddedCli *cli, char *args, void *context);
static void on_acccalc(EmbeddedCli *cli, char *args, void *context);
void on_stepper_enable(EmbeddedCli *cli, char *args, void *context);
void on_stepper_disable(EmbeddedCli *cli, char *args, void *context);
void on_stepper_set_left(EmbeddedCli *cli, char *args, void *context);
void on_stepper_set_right(EmbeddedCli *cli, char *args, void *context);
void on_stepper_set_both(EmbeddedCli *cli, char *args, void *context);
void on_stepper_show_left(EmbeddedCli *cli, char *args, void *context);
void on_stepper_show_right(EmbeddedCli *cli, char *args, void *context);

static void write_char_fn(EmbeddedCli *embeddedCli, char c);
void cli_printf(const char *fmt, ...);
static void on_command_fn(EmbeddedCli *embeddedCli, CliCommand *command);
void cli_initialise();
void cli_process();

#endif /* CLI_H_ */