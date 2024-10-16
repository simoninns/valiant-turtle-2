/************************************************************************ 

    btcomms.h

    Valiant Turtle 2 Communicator - Raspberry Pi Pico W Firmware
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

#define BT_MODE_GPIO 14

// BK example defines...
#define NUM_ROWS 25
#define NUM_COLS 40

#define SPP_PROCESS_PERIOD_MS 10

// Define the required number of virtual serial port connections
#define SPP_PORTS 1

// Class Of Device
// Service Class: Networking
// Major Device Class: Toy
// Minor Device Class: Robot
#define BT_CLASS_OF_DEVICE 0x020804

// Interval between scanning for SPP servers (in seconds)
#define SCAN_INQUIRY_INTERVAL 5

// State enum
typedef enum {
    // SPP
    BTCOMMS_OFF,
    BTCOMMS_DISCONNECTED,
    BTCOMMS_COD_SCANNING,
    BTCOMMS_COD_SCAN_COMPLETE,
    BTCOMMS_SEND_SDP_QUERY,
    BTCOMMS_SDP_QUERY_SENT,
    BTCOMMS_CONNECTED,
    DONE
} btcomms_state_t;

struct btstack_timer_source;

// Prototypes
void btcomms_initialise(void);

static void btcomms_start_scan(void);
static void btcomms_stop_scan(void);

static void btcomms_handle_query_rfcomm_event(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size);
static void btcomms_handle_start_sdp_client_query(void * context);
static void btcomms_packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size);

static void btcomms_one_shot_timer_setup(void);
static void btcomms_process_handler(struct btstack_timer_source *ts);

bool btcomms_is_channel_open(int8_t channel);

int btcomms_getchar(int8_t channel);
int btcomms_putchar(int8_t channel, char c);

#endif /* BTCOMMS_H_ */