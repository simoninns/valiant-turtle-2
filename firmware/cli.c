/************************************************************************ 

    cli.c

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

#include <stdio.h>
#include <pico/stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#include "cli.h"
#include "command.h"

// State Globals
cli_state_t cliState;

// CLI Buffer
char cliBuffer[10];
uint16_t cliBufferPointer;
uint16_t cliError;

void cliResetCommandBuffers(void)
{
    cliBufferPointer = 0;
    cliError = ERR_CMD_NONE;
}

void cliInitialise(void)
{
    cliState = CLI_START;
    cliResetCommandBuffers();
}

void cliProcess(void)
{
    switch(cliState) {
        case CLI_START:
            cliState = cliState_Start();
            break;

        case CLI_PROMPT:
            cliState = cliState_Prompt();
            break;

        case CLI_COLLECT:
            cliState = cliState_Collect();
            break; 

        case CLI_INTERPRET:
            cliState = cliState_Interpret();
            break; 

        case CLI_ERROR:
            cliState = cliState_Error();
            break; 
    }
}

cli_state_t cliState_Start(void)
{
    // Show a banner on the CLI
    printf("\r\nValiant Turtle 2\r\n");
    printf("Copyright (C)2023 Simon Inns\r\n");
    printf("Use HLP to show available commands\r\n");

    return CLI_PROMPT;
}

cli_state_t cliState_Prompt(void)
{
    // Show the prompt
    printf("\r\nVT2> ");
    return CLI_COLLECT;
}

cli_state_t cliState_Collect(void)
{
    // Collect any input waiting
    const int cint = getchar_timeout_us(0);

    // Was anything received?
    if ((cint < 0) || (cint > 254)) {
      // didn't get anything
      return CLI_COLLECT;
    }

    // Was the character a <CR>?
    if (cint == 13) {
        // Has the buffer got contents?
        if (cliBufferPointer > 0) {
            printf("\r\n");
            return CLI_INTERPRET;
        } else {
            return CLI_PROMPT;
        }
    }

    // Was the character a <BS>?
    if (cint == 8) {
        // Backspace
        if (cliBufferPointer > 0) {
            putchar(8);
            putchar(32);
            putchar(8);
            cliBufferPointer--;
        }
        return CLI_COLLECT;
    }

    // Buffer overflow?
    if (cliBufferPointer == 8) {
        // Ignore further input until it's a <CR> or <BS>
        return CLI_COLLECT;
    }

    // Not a <CR>, so add the character to our buffer
    cliBuffer[cliBufferPointer] = cint;
    cliBufferPointer++;

    // Display the received character
    putchar((char)cint);

    // All good, keep collecting
    return CLI_COLLECT;
}

cli_state_t cliState_Interpret(void)
{
    // Note: All commands are cccppppp where ccc is the command and ppppp is a numerical parameter

    // Check minimum length
    if (cliBufferPointer < 3) {
        cliError = ERR_CMD_SHORT;
        return CLI_ERROR;
    }

    // Get the command (3 characters)
    char command[4];
    char parameter[6];
    uint16_t pointer = 0;

    for (pointer = 0; pointer < 3; pointer++) {
        command[pointer] = cliBuffer[pointer];
    }
    command[pointer] = '\0'; // Terminate

    // Get the parameter (5 characters)
    for (pointer = 0; pointer < cliBufferPointer-3; pointer++) {
        parameter[pointer] = cliBuffer[pointer+3];
    }
    parameter[pointer] = '\0'; // Terminate

    // Convert command to uppercase
    convUppercase(command);

    // Convert parameter to integer
    uint16_t nparam = atoi(parameter);

    // Process the command
    if (commandProcess(command, nparam) != 0) {
        cliError = ERR_CMD_UNKNOWN;
        return CLI_ERROR;
    }

    // Empty the buffer and return to the prompting state
    cliResetCommandBuffers();
    return CLI_PROMPT;
}

cli_state_t cliState_Error(void)
{
    switch(cliError) {
        case ERR_CMD_NONE:
            printf("E00 - OK\r\n");
            break;

        case ERR_CMD_SHORT:
            printf("E01 - Command too short\r\n");
            break;

        case ERR_CMD_UNKNOWN:
            printf("E02 - Unknown command\r\n");
            break;

        case ERR_CMD_PARAMISSING:
            printf("E03 - Parameter missing\r\n");
            break;
    }

    // Empty the buffer and return to the prompting state
    cliResetCommandBuffers();
    return CLI_PROMPT;
}

// Convert a string to uppercase
void convUppercase(char *temp)
{
    char * name;
    name = strtok(temp,":");

    // Convert to upper case
    char *s = name;
    while (*s) {
        *s = toupper((unsigned char) *s);
        s++;
    }
}