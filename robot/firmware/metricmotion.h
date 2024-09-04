/************************************************************************ 

    metricmotion.h

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

#ifndef METRICMOTION_H_
#define METRICMOTION_H_

#define WHEEL_DIAMETER_MM 55.0
#define AXEL_WIDTH 230.0
#define STEPS_PER_REV 800.0

void metricmotion_forwards(int32_t millimeters);
void metricmotion_backwards(int32_t millimeters);
void metricmotion_left(int32_t degrees);
void metricmotion_right(int32_t degrees);

int32_t metricmotion_mm_to_steps(int32_t millimeters);
int32_t metricmotion_deg_to_steps(int32_t degrees);

#endif /* METRICMOTION_H_ */