/************************************************************************ 

    command.h

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

#ifndef COMMAND_H_
#define COMMAND_H_

uint16_t commandProcess(char *command, uint16_t parameter);

void commandHelp(void);
void commandI2cScan(uint16_t commandParameter);
void commandPowerMonitor(void);
void commandPen(uint16_t commandType);
void commandMotor(uint16_t commandType, uint16_t commandParameter);
void commandLed(uint16_t ledNumber, uint16_t commandParameter);
void commandButton(void);

#endif /* COMMAND_H_ */