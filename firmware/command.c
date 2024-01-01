/************************************************************************ 

    command.c

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

#include "command.h"
#include "penservo.h"
#include "drivemotors.h"

uint16_t commandProcess(char *command, uint16_t parameter)
{
    // Help
    if (strcmp(command, "HLP") == 0) {
        commandHelp();
        return 0;
    }

    // Pen servo commands
    if (strcmp(command, "PEO") == 0) {
        commandPen(0);
        return 0;
    }

    if (strcmp(command, "PEU") == 0) {
        commandPen(1);
        return 0;
    }

    if (strcmp(command, "PED") == 0) {
        commandPen(2);
        return 0;
    }

    if (strcmp(command, "MON") == 0) {
        commandMotor(0, parameter);
        return 0;
    }

    if (strcmp(command, "MOF") == 0) {
        commandMotor(1, parameter);
        return 0;
    }

    if (strcmp(command, "MLD") == 0) {
        commandMotor(2, parameter);
        return 0;
    }

    if (strcmp(command, "MRD") == 0) {
        commandMotor(3, parameter);
        return 0;
    }

    if (strcmp(command, "MLS") == 0) {
        commandMotor(4, parameter);
        return 0;
    }

    if (strcmp(command, "MRS") == 0) {
        commandMotor(5, parameter);
        return 0;
    }

    // Drive motor commands

    // Unknown command
    return 1;
}

void commandHelp(void)
{
    printf("Help:\r\n");
        printf("  HLP - Show this help text\r\n");
        printf("\r\n");
        printf("  PEU      - Pen servo up\r\n");
        printf("  PED      - Pen servo down\r\n");
        printf("  PEO      - Pen servo off\r\n");
        printf("\r\n");
        printf("  MON      - Drive motors on\r\n");
        printf("  MOF      - Drive motors off\r\n");
        printf("  MLDx     - Motor left direction (0=REV 1=FWD)\r\n");
        printf("  MRDx     - Motor right direction (0=REV 1=FWD)\r\n");
        printf("  MLSxxxxx - Motor left step (number of steps)\r\n");
        printf("  MRSxxxxx - Motor right step (number of steps)\r\n");
        printf("\r\n");
        printf("  LDRxx    - LED Red intensity (0-15)\r\n");
        printf("  LDGxx    - LED Green intensity (0-15)\r\n");
        printf("  LDBxx    - LED Blue intensity (0-15)\r\n");
}

void commandPen(uint16_t commandType)
{
    switch(commandType) {
        case 0:
            penOff();
            printf("R00 - Pen servo off");
            break;
        
        case 1:
            penUp();
            printf("R00 - Pen servo up");
            break;

        case 2:
            penDown();
            printf("R00 - Pen servo down");
            break;
    }
}

void commandMotor(uint16_t commandType, uint16_t commandParameter)
{
    switch(commandType) {
        case 0: // Motors on
            driveMotorsEnable(true);
            printf("R00 - Drive motors on");
            break;
        
        case 1: // Motors off
            driveMotorsEnable(false);
            printf("R00 - Drive motors off");
            break;

        case 2: // Motor left set direction
            if (commandParameter == 1) driveMotorLeftDir(true);
            else driveMotorLeftDir(false);
            printf("R00 - Motor left set direction");
            break;

        case 3: // Motor right set direction
            if (commandParameter == 1) driveMotorRightDir(true);
            else driveMotorRightDir(false);
            printf("R00 - Motor right set direction");
            break;

        case 4: // Motor left step
            driveMotorLeftStep(commandParameter);
            printf("R00 - Motor left step");
            break;

        case 5: // Motor right step
            driveMotorRightStep(commandParameter);
            printf("R00 - Motor right step");
            break;
    }
}