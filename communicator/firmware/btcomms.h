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

// Class Of Device
// Service Class: Networking
// Major Device Class: Toy
// Minor Device Class: Robot
#define BT_CLASS_OF_DEVICE 0x020804

#define TEST_MODE_SEND      1
#define TEST_MODE_RECEIVE   2
#define TEST_MODE_DUPLEX    3

// configure test mode: send only, receive only, full duplex
#define TEST_MODE TEST_MODE_SEND

// Interval between scanning for SPP servers (in seconds)
#define SCAN_INQUIRY_INTERVAL 5

// Throughput tracking report interval
#define REPORT_INTERVAL_MS 3000

typedef enum {
    // SPP
    W4_PEER_COD,
    W4_SCAN_COMPLETE,
    W4_SDP_RESULT,
    W2_SEND_SDP_QUERY,
    W4_RFCOMM_CHANNEL,
    SENDING,
    DONE
} state_t;

void btcomms_initialise(void);

static void btcomms_start_scan(void);
static void btcomms_stop_scan(void);

static void btcomms_test_reset(void);
static void btcomms_test_track_transferred(int bytes_sent);

static void btcomms_spp_create_test_data(void);
static void btcomms_spp_send_packet(void);

static void btcomms_handle_query_rfcomm_event(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size);
static void btcomms_handle_start_sdp_client_query(void * context);
static void btcomms_packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size);

#endif /* BTCOMMS_H_ */