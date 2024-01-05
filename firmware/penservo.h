/************************************************************************ 

    penservo.h

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

#ifndef PENSERVO_H_
#define PENSERVO_H_

// Hardware mapping
// GPIO 28 (pin 34)
#define PENSERVO_GPIO 28

// Function prototypes
void penServoInitialise(void);
void penDown(void);
void penUp(void);
void penOff(void);

#endif /* PENSERVO_H_ */