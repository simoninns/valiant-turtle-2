/************************************************************************ 

    uart.h

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

#ifndef UART_H_
#define UART_H_

class Uart {
    public:
        Uart(uart_inst_t* _uart_id, int8_t _tx_gpio, int8_t _rx_gpio, int32_t _baud_rate);

        enum parity_t {
            PARITY_NONE,
            PARITY_EVEN,
            PARITY_ODD,
        };

        enum flow_control_t {
            FLOW_NONE,
            FLOW_SOFT,
            FLOW_HARD,
        };

        // Type for callback functions
        typedef void (*callback_t) (void);

        void set_hardware_flow_on(int8_t _rts_gpio, int8_t _cts_gpio);
        void set_hardware_flow_off(void);
        bool set_rx_callback(callback_t _rx_callback);
        uint8_t getc(void);
        void putc(uint8_t c);
        void puts(const char* s);
        bool is_readable(void);

    private:
        uart_inst_t* uart_id;
        int8_t tx_gpio;
        int8_t rx_gpio;
        int8_t rts_gpio;
        int8_t cts_gpio;
        int32_t baud_rate;
        int8_t data_bits;
        int8_t stop_bits;
        parity_t parity; 
        flow_control_t flow_control;

        callback_t rx_callback;
        bool rx_callback_set;
};

#endif /* UART_H_ */