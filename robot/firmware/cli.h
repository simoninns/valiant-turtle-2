/************************************************************************ 

    cli.h

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

#ifndef CLI_H_
#define CLI_H_

// Enumerations
typedef enum {
    CLI_START,
    CLI_PROMPT,
	CLI_COLLECT,
    CLI_INTERPRET,
	CLI_ERROR,
    CLI_PENCTRL,
    CLI_MOTORCTRL
} cli_state_t;

typedef enum {
    ERR_CMD_NONE,
    ERR_CMD_SHORT,
    ERR_CMD_UNKNOWN,
    ERR_CMD_PARAMISSING
} cli_error_t;

// Prototypes
void cliResetCommandBuffers(void);
void cliInitialise(void);
void cliProcess(void);

// States
cli_state_t cliState_Start(void);
cli_state_t cliState_Prompt(void);
cli_state_t cliState_Collect(void);
cli_state_t cliState_Interpret(void);
cli_state_t cliState_Error(void);

// Utilities
void convUppercase(char *temp);

#endif /* CLI_H_ */