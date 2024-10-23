/************************************************************************ 

    led.h

    Valiant Turtle Communicator 2
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

#ifndef LED_H_
#define LED_H_

class Led {
    public:
        Led(uint8_t _led_gpio);
        void set_state(bool _led_state);

    private:
        uint8_t led_gpio;
        bool led_state;
};

#endif /* LED_H_ */