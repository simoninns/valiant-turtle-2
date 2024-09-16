/************************************************************************ 

    btcomms.h

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

#ifndef BTCOMMS_H_
#define BTCOMMS_H_

#define BTCLIPROCESS_PERIOD_MS 10

#define SPP_CLI_SERVER_CHANNEL 1
#define SPP_DEBUG_SERVER_CHANNEL 2

// Enumerations
typedef enum {
    BTCOMMS_OFF,
    BTCOMMS_DISCONNECTED,
    BTCOMMS_CONNECTED,
    BTCOMMS_PAIRING
} btComms_state_t;

struct btstack_timer_source;

static void btcomms_spp_service_setup(void);
static void btcomms_packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size);

static void btcomms_one_shot_timer_setup(void);
static void btcomms_cli_process_handler(struct btstack_timer_source *ts);

void btcomms_initialise(void);
void btcomms_process(void);
void btcomms_printf(const char *fmt, ...);

#endif /* BTCOMMS_H_ */