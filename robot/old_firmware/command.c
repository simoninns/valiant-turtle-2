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
#include "btcomms.h"
#include "debug.h"

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

    if (strcmp(command, "MLV") == 0) {
        commandMotor(6, parameter);
        return 0;
    }

    if (strcmp(command, "MRV") == 0) {
        commandMotor(7, parameter);
        return 0;
    }

    if (strcmp(command, "MAR") == 0) {
        commandMotor(8, parameter);
        return 0;
    }

    if (strcmp(command, "MAS") == 0) {
        commandMotor(9, parameter);
        return 0;
    }

    if (strcmp(command, "MSS") == 0) {
        commandMotor(10, parameter);
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

    // Unknown command
    return 1;
}

void commandHelp(void)
{
    debugPrintf("CLI: Got command HLP\r\n");

    btPrintf("Help:\r\n");
    btPrintf("  HLP - Show this help text\r\n");
    btPrintf("\r\n");
    btPrintf("  IICx - Scan I2C bus (bus number)\r\n");
    btPrintf("  POW - Read power information from the INA260\r\n");
    btPrintf("\r\n");
    btPrintf("  PEU      - Pen servo up\r\n");
    btPrintf("  PED      - Pen servo down\r\n");
    btPrintf("  PEO      - Pen servo off\r\n");
    btPrintf("\r\n");
    btPrintf("  MON      - Drive motors enabled\r\n");
    btPrintf("  MOF      - Drive motors disabled\r\n");
    btPrintf("  MLDx     - Motor left direction (0=REV 1=FWD)\r\n");
    btPrintf("  MRDx     - Motor right direction (0=REV 1=FWD)\r\n");
    btPrintf("  MLSxxxxx - Motor left add steps (1600 steps/revolution)\r\n");
    btPrintf("  MRSxxxxx - Motor right add steps (1600 steps/revolution)\r\n");
    btPrintf("  MLVx     - Motor left speed (0=Fast 3=Slow)\r\n");
    btPrintf("  MRVx     - Motor right speed (0=Fast 3=Slow)\r\n");
    btPrintf("  MAR      - Motors all run\r\n");
    btPrintf("  MAS      - Motors all stop\r\n");
    btPrintf("  MSS      - Motors show status\r\n");
    btPrintf("\r\n");
    btPrintf("  LDRxxx   - LED Red intensity (0-255)\r\n");
    btPrintf("  LDGxxx   - LED Green intensity (0-255)\r\n");
    btPrintf("  LDBxxx   - LED Blue intensity (0-255)\r\n");
}

void commandI2cScan(uint16_t commandParameter)
{
    if (commandParameter > 1) {
        debugPrintf("CLI: Got command IIC but parameter was out of range\r\n");
        btPrintf("E04 - Parameter out of range\r\n");
        return;
    }

    debugPrintf("CLI: Got command IIC\r\n");

    // Scan the I2C bus
    i2cBusScan(commandParameter);
}

void commandPowerMonitor(void)
{
    debugPrintf("CLI: Got command POW\r\n");

    float current = ina260ReadCurrent();
    float voltage = ina260ReadBusVoltage();
    float power = ina260ReadPower();

    btPrintf("INA260 Power information:\r\nCurrent: %.2f mA\r\nBus voltage: %.2f mV\r\nPower: %.2f mW", current, voltage, power);
}

void commandPen(uint16_t commandType)
{
    switch(commandType) {
        case 0:
            penOff();
            debugPrintf("CLI: Got command PEO\r\n");
            btPrintf("R00 - Pen servo off");
            break;
        
        case 1:
            penUp();
            debugPrintf("CLI: Got command PEU\r\n");
            btPrintf("R00 - Pen servo up");
            break;

        case 2:
            penDown();
            debugPrintf("CLI: Got command PED\r\n");
            btPrintf("R00 - Pen servo down");
            break;
    }
}

void commandMotor(uint16_t commandType, uint16_t commandParameter)
{
    motor_speed_t requiredSpeed;

    switch(commandType) {
        case 0: // Motors on
            driveMotorsEnable(true);
            debugPrintf("CLI: Got command MON\r\n");
            btPrintf("R00 - Drive motors on");
            break;
        
        case 1: // Motors off
            driveMotorsEnable(false);
            debugPrintf("CLI: Got command MOF\r\n");
            btPrintf("R00 - Drive motors off");
            break;

        case 2: // Motor left set direction
            if (commandParameter == 1) {
                if (!driveMotorSetDir(MOTOR_LEFT, MOTOR_FORWARDS)) {
                    debugPrintf("CLI: Got command MLD - but motor is running\r\n");
                    btPrintf("E05 - Not allowed!");
                } else {
                    debugPrintf("CLI: Got command MLD\r\n");
                    btPrintf("R00 - Motor left set direction");
                }
            } else {
                if (!driveMotorSetDir(MOTOR_LEFT, MOTOR_BACKWARDS)) {
                    debugPrintf("CLI: Got command MLD - but motor is running\r\n");
                    btPrintf("E05 - Not allowed!");
                } else {
                    debugPrintf("CLI: Got command MLD\r\n");
                    btPrintf("R00 - Motor left set direction");
                }
            }
            break;

        case 3: // Motor right set direction
            if (commandParameter == 1) {
                if (!driveMotorSetDir(MOTOR_RIGHT, MOTOR_FORWARDS)) {
                    debugPrintf("CLI: Got command MRD - but motor is running\r\n");
                    btPrintf("E05 - Not allowed!");
                } else {
                    debugPrintf("CLI: Got command MRD\r\n");
                    btPrintf("R00 - Motor right set direction");
                }
            } else {
                if (!driveMotorSetDir(MOTOR_RIGHT, MOTOR_BACKWARDS)) {
                    debugPrintf("CLI: Got command MRD - but motor is running\r\n");
                    btPrintf("E05 - Not allowed!");
                } else {
                    debugPrintf("CLI: Got command MRD\r\n");
                    btPrintf("R00 - Motor right set direction");
                }
            }
            break;

        case 4: // Motor left step
            driveMotorSetSteps(MOTOR_LEFT, commandParameter);
            debugPrintf("CLI: Got command MLS\r\n");
            btPrintf("R00 - Motor left step");
            break;

        case 5: // Motor right step
            driveMotorSetSteps(MOTOR_RIGHT, commandParameter);
            debugPrintf("CLI: Got command MRS\r\n");
            btPrintf("R00 - Motor right step");
            break;

        case 6: // Motor left speed
            if (commandParameter > 3) {
                debugPrintf("CLI: Got command MLV but parameter was out of range\r\n");
                btPrintf("E04 - Parameter out of range\r\n");
            } else {
                switch(commandParameter) {
                    case 0: requiredSpeed = MOTOR_200;
                        break;

                    case 1: requiredSpeed = MOTOR_400;
                        break;

                    case 2: requiredSpeed = MOTOR_800;
                        break;

                    case 3: requiredSpeed = MOTOR_1600;
                        break;

                    default:
                        requiredSpeed = MOTOR_1600;
                }

                driveMotorSetMaximumSpeed(MOTOR_LEFT, requiredSpeed);
                debugPrintf("CLI: Got command MLV\r\n");
                btPrintf("R00 - Motor left speed");
            }
            break;

        case 7: // Motor right speed
            if (commandParameter > 3) {
                debugPrintf("CLI: Got command MLV but parameter was out of range\r\n");
                btPrintf("E04 - Parameter out of range\r\n");
            } else {
                switch(commandParameter) {
                    case 0: requiredSpeed = MOTOR_200;
                        break;

                    case 1: requiredSpeed = MOTOR_400;
                        break;

                    case 2: requiredSpeed = MOTOR_800;
                        break;

                    case 3: requiredSpeed = MOTOR_1600;
                        break;

                    default:
                        requiredSpeed = MOTOR_1600;
                }

                driveMotorSetMaximumSpeed(MOTOR_RIGHT, requiredSpeed);
                debugPrintf("CLI: Got command MRV\r\n");
                btPrintf("R00 - Motor right speed");
            }
            break;

        case 8: // Motors all run
            if (driveMotorsRunning(true)) {
                debugPrintf("CLI: Got command MAR\r\n");
                btPrintf("R00 - Both motors running");
            } else {
                debugPrintf("CLI: Got command MAR - but motors are not enabled!\r\n");
                btPrintf("E05 - Not allowed!");
            }
            break;

        case 9: // Motors all stop
            driveMotorsRunning(false);
            debugPrintf("CLI: Got command MAS\r\n");
            btPrintf("R00 - Both motors stopped");
            break;

        case 10: // Motors show status
            driveMotorStatus();
            debugPrintf("CLI: Got command MSS\r\n");
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
            debugPrintf("CLI: Got command LDR with intensity %d\r\n", commandParameter);
            btPrintf("R00 - LED Red intensity set to %d", commandParameter);
            break;
        
        case 1:
            ledGreenSet(commandParameter);
            debugPrintf("CLI: Got command LDG with intensity %d\r\n", commandParameter);
            btPrintf("R00 - LED Green intensity set to %d", commandParameter);
            break;

        case 2:
            ledBlueSet(commandParameter);
            debugPrintf("CLI: Got command LDB with intensity %d\r\n", commandParameter);
            btPrintf("R00 - LED Blue intensity set to %d", commandParameter);
            break;
    }
}