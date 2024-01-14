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
#include "i2cbus.h"
#include "ina260.h"
#include "leds.h"
#include "display.h"
#include "buttons.h"

uint16_t commandProcess(char *command, uint16_t parameter)
{
    // Help
    if (strcmp(command, "HLP") == 0) {
        commandHelp();
        return 0;
    }

    if (strcmp(command, "IIC") == 0) {
        commandI2cScan(parameter);
        return 0;
    }

    if (strcmp(command, "POW") == 0) {
        commandPowerMonitor();
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

    // LED Commands
    if (strcmp(command, "LDR") == 0) {
        commandLed(0, parameter);
        return 0;
    }

    if (strcmp(command, "LDG") == 0) {
        commandLed(1, parameter);
        return 0;
    }

    if (strcmp(command, "LDB") == 0) {
        commandLed(2, parameter);
        return 0;
    }

    if (strcmp(command, "BUT") == 0) {
        commandButton();
        return 0;
    }

    // Unknown command
    return 1;
}

void commandHelp(void)
{
//    printf("Help:\r\n");
//     printf("  HLP - Show this help text\r\n");
//     printf("\r\n");
//     printf("  IICx - Scan I2C bus (bus number)\r\n");
//     printf("  POW - Read power information from the INA260\r\n");
//     printf("\r\n");
//     printf("  PEU      - Pen servo up\r\n");
//     printf("  PED      - Pen servo down\r\n");
//     printf("  PEO      - Pen servo off\r\n");
//     printf("\r\n");
//     printf("  MON      - Drive motors on\r\n");
//     printf("  MOF      - Drive motors off\r\n");
//     printf("  MLDx     - Motor left direction (0=REV 1=FWD)\r\n");
//     printf("  MRDx     - Motor right direction (0=REV 1=FWD)\r\n");
//     printf("  MLSxxxxx - Motor left step (number of steps)\r\n");
//     printf("  MRSxxxxx - Motor right step (number of steps)\r\n");
//     printf("\r\n");
//     printf("  LDRxxx   - LED Red intensity (0-255)\r\n");
//     printf("  LDGxxx   - LED Green intensity (0-255)\r\n");
//     printf("  LDBxxx   - LED Blue intensity (0-255)\r\n");
//     printf("\r\n");
//     printf("  BUT      - Show button states\r\n");

    // snprintf(lineBuffer, sizeof(lineBuffer), "Output from the HLP command goes here...\r\n");
    // btSendLineBuffer();
}

void commandI2cScan(uint16_t commandParameter)
{
    if (commandParameter > 1) {
        printf("E04 - Parameter out of range\r\n");
        return;
    }

    // Scan the I2C bus
    i2cBusScan(commandParameter);
}

void commandPowerMonitor(void)
{
    printf("INA260 Power information:\r\n");
    printf("      Current: %.2f mA\r\n", ina260ReadCurrent());
    printf("  Bus voltage: %.2f mV\r\n", ina260ReadBusVoltage());
    printf("        Power: %.2f mW\r\n", ina260ReadPower());

    displayPowerInformation(ina260ReadCurrent(), ina260ReadBusVoltage(), ina260ReadPower());
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

void commandLed(uint16_t ledNumber, uint16_t commandParameter)
{
    // Range check the requested brightness
    if (commandParameter < 0) commandParameter = 0;
    if (commandParameter > 255) commandParameter = 255;

    switch(ledNumber) {
        case 0:
            ledRedSet(commandParameter);
            printf("R00 - LED Red intensity set to %d", commandParameter);
            break;
        
        case 1:
            ledGreenSet(commandParameter);
            printf("R00 - LED Green intensity set to %d", commandParameter);
            break;

        case 2:
            ledBlueSet(commandParameter);
            printf("R00 - LED Blue intensity set to %d", commandParameter);
            break;
    }
}

void commandButton(void)
{
    bool button0;
    bool button1;

    button0 = buttonsGetState(0);
    button1 = buttonsGetState(1);

    if (button0) printf("Button 0: ON\r\n");
    else printf("Button 0: OFF\r\n");
    if (button1) printf("Button 1: ON\r\n");
    else printf("Button 1: OFF\r\n");
}