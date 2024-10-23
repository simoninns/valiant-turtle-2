/************************************************************************ 

    parallel.h

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

#ifndef PARALLEL_H_
#define PARALLEL_H_

#include "mcp23017.h"

// MCP27013 pin mapping GPA0 - GPB7 = 0 to 15
#define PARALLEL_UN0 0
#define PARALLEL_UN1 1
#define PARALLEL_NACK 2
#define PARALLEL_BUSY 3
#define PARALLEL_NDATASTROBE 4
#define PARALLEL_5 5
#define PARALLEL_6 6
#define PARALLEL_7 7
#define PARALLEL_DAT0 8
#define PARALLEL_DAT1 9
#define PARALLEL_DAT2 10
#define PARALLEL_DAT3 11
#define PARALLEL_DAT4 12
#define PARALLEL_DAT5 13
#define PARALLEL_DAT6 14
#define PARALLEL_DAT7 15

class Parallel {
    public:
        Parallel(void);

        // Type for callback functions
        typedef void (*callback_t) (void);

        uint8_t get_data(void);
        bool set_rx_callback(callback_t _rx_callback);
        void ack(void);

    private:
        Mcp23017* mcp23017;

        callback_t rx_callback;
        bool rx_callback_set;
};

#endif /* PARALLEL_H_ */