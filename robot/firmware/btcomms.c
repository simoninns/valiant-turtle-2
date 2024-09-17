/************************************************************************ 

    btcomms.c

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

#include <stdio.h>
#include <pico/stdlib.h>
#include "pico/cyw43_arch.h"
#include "pico/cyw43_arch.h"
#include "pico/btstack_cyw43.h"
#include "btstack.h"

#include <inttypes.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "btcomms.h"
#include "fifo.h"
#include "cli.h"
#include "debug.h"

// Globals
static btstack_timer_source_t btcomms_cli_process_timer;
static btstack_packet_callback_registration_t hci_event_callback_registration;

static uint8_t spp_service_buffer[2][150];

btComms_state_t current_bt_state[3];
static bool channel_open[3];
static uint16_t rfcomm_channel_id[3];

char *lineBuffer;

// Initialise the Bluetooth stack and functionality
void btcomms_initialise(void)
{
    debug_printf("btcomms_initialise(): Initialising Bluetooth\n");
    // Set initial state
    channel_open[SPP_CLI_SERVER_CHANNEL] = false;
    channel_open[SPP_DEBUG_SERVER_CHANNEL] = false;
    current_bt_state[SPP_CLI_SERVER_CHANNEL] = BTCOMMS_OFF;
    current_bt_state[SPP_DEBUG_SERVER_CHANNEL] = BTCOMMS_OFF;

    // Set up the FIFO buffers for incoming and outgoing characters
    fifo_initialise();

    btcomms_one_shot_timer_setup();
    btcomms_spp_service_setup();

    gap_discoverable_control(1);
    gap_ssp_set_io_capability(SSP_IO_CAPABILITY_DISPLAY_YES_NO);

    // Use the following to include the HW Address in the device name
    gap_set_local_name("Valiant Turtle 2 00:00:00:00:00:00");

    // Power on the Bluetooth device
    hci_power_control(HCI_POWER_ON);
    current_bt_state[SPP_CLI_SERVER_CHANNEL] = BTCOMMS_DISCONNECTED;
    current_bt_state[SPP_DEBUG_SERVER_CHANNEL] = BTCOMMS_DISCONNECTED;

    debug_printf("btcomms_initialise(): Bluetooth is powered on\n");

    // Malloc some memory for the shared lineBuffer
    lineBuffer = malloc(sizeof(char*) * LINE_BUFFER_SIZE);

    if (!lineBuffer) {
        debug_printf("btcomms_initialise(): Line buffer memory allocation failed\n"); 
        exit(0); 
    }
}

// Set up Serial Port Profile (SPP)
static void btcomms_spp_service_setup(void)
{
    debug_printf("btcomms_spp_service_setup(): Setting up Bluetooth SPP services\n");

    // register for HCI events
    hci_event_callback_registration.callback = &btcomms_packet_handler;
    hci_add_event_handler(&hci_event_callback_registration);

    l2cap_init();
    rfcomm_init();
    rfcomm_register_service(btcomms_packet_handler, SPP_CLI_SERVER_CHANNEL, 0xffff);  // Reserve channel 1, mtu limited by l2cap
    rfcomm_register_service(btcomms_packet_handler, SPP_DEBUG_SERVER_CHANNEL, 0xffff);  // Reserve channel 2, mtu limited by l2cap

    // Initialise SDP
    sdp_init();

    // Set up SPP Channel 1 for Valiant Turtle CLI
    memset(spp_service_buffer[0], 0, sizeof(spp_service_buffer[0]));
    spp_create_sdp_record(spp_service_buffer[0], sdp_create_service_record_handle(), 1, "Valiant Turtle CLI");
    btstack_assert(de_get_len(spp_service_buffer[0]) <= sizeof(spp_service_buffer[0]));
    sdp_register_service(spp_service_buffer[0]);

    // Set up SPP Channel 2 for Valiant Turtle Debug
    memset(spp_service_buffer[1], 0, sizeof(spp_service_buffer[1]));
    spp_create_sdp_record(spp_service_buffer[1], sdp_create_service_record_handle(), 2, "Valiant Turtle Debug");
    btstack_assert(de_get_len(spp_service_buffer[1]) <= sizeof(spp_service_buffer[1]));
    sdp_register_service(spp_service_buffer[1]);
}

// Bluetooth packet handler
static void btcomms_packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
    bd_addr_t event_addr;
    uint8_t rfcomm_server_channel;
    uint16_t mtu;
    uint16_t requesting_cid;

    switch (packet_type) {
        case HCI_EVENT_PACKET:
            switch (hci_event_packet_get_type(packet)) {
                case RFCOMM_EVENT_INCOMING_CONNECTION:
                    rfcomm_event_incoming_connection_get_bd_addr(packet, event_addr);
                    rfcomm_server_channel = rfcomm_event_incoming_connection_get_server_channel(packet);
                    rfcomm_channel_id[rfcomm_server_channel] = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);
                    debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_INCOMING_CONNECTION event on server channel %u with CID %u\n", rfcomm_server_channel, rfcomm_channel_id[rfcomm_server_channel]);
                    
                    rfcomm_accept_connection(rfcomm_channel_id[rfcomm_server_channel]);
                    debug_printf("btcomms_packet_handler():   Connection request accepted from client %s\n", bd_addr_to_str(event_addr));
                    break;
               
                case RFCOMM_EVENT_CHANNEL_OPENED:
                    if (rfcomm_event_channel_opened_get_status(packet)) {
                        debug_printf("btcomms_packet_handler(): RFCOMM channel open FAILED, status 0x%02x\n", rfcomm_event_channel_opened_get_status(packet));
                    } else {
                        rfcomm_server_channel = rfcomm_event_channel_opened_get_server_channel(packet);
                        rfcomm_channel_id[rfcomm_server_channel] = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_CHANNEL_OPENED event on server channel %u with CID %u\n", rfcomm_server_channel, rfcomm_channel_id[rfcomm_server_channel]);

                        mtu = rfcomm_event_channel_opened_get_max_frame_size(packet);
                        debug_printf("btcomms_packet_handler():   RFCOMM channel open succeeded - max frame size %u\n", mtu);
                        current_bt_state[rfcomm_server_channel] = BTCOMMS_CONNECTED;
                        channel_open[rfcomm_server_channel] = true;
                    }
                    break;

                case RFCOMM_EVENT_CAN_SEND_NOW:
                    requesting_cid = rfcomm_event_can_send_now_get_rfcomm_cid(packet);

                    // Check if requesting CID belongs to server channel 1 (CLI)
                    if (requesting_cid == rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL]) {
                        // Output the contents of the CLI output buffer
                        int16_t pos = 0;
                        bool finished = false;
                        while (!finished) {
                            lineBuffer[pos] = fifo_out_read(CLI_BUFFER);
                            if (lineBuffer[pos] == 0) finished = true;
                            if (pos == 128-2) {
                                lineBuffer[pos+1] = 0;
                                finished = true;
                            }
                            pos++;
                        }

                        if (pos != 0) {
                            rfcomm_send(rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL], (uint8_t*) lineBuffer, (uint16_t) pos);
                        }
                    } else if (requesting_cid == rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL]) {
                        // Output the contents of the Debug output buffer
                        int16_t pos = 0;
                        bool finished = false;
                        while (!finished) {
                            lineBuffer[pos] = fifo_out_read(DEBUG_BUFFER);
                            if (lineBuffer[pos] == 0) finished = true;
                            if (pos == 128-2) {
                                lineBuffer[pos+1] = 0;
                                finished = true;
                            }
                            pos++;
                        }

                        if (pos != 0) {
                            rfcomm_send(rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL], (uint8_t*) lineBuffer, (uint16_t) pos);
                        }
                    }
                    break;

                case RFCOMM_EVENT_CHANNEL_CLOSED:
                    requesting_cid = rfcomm_event_channel_closed_get_rfcomm_cid(packet);
                    debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_CHANNEL_CLOSED event with CID %u\n", requesting_cid);

                    // Check if requesting CID belongs to the CLI channel
                    if (requesting_cid == rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL]) {
                        current_bt_state[SPP_CLI_SERVER_CHANNEL] = BTCOMMS_DISCONNECTED;
                        channel_open[SPP_CLI_SERVER_CHANNEL] = false;
                        debug_printf("btcomms_packet_handler():   RFCOMM CLI channel is closed\n");
                    } else if (requesting_cid == rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL]) {
                        current_bt_state[SPP_DEBUG_SERVER_CHANNEL] = BTCOMMS_DISCONNECTED;
                        channel_open[SPP_DEBUG_SERVER_CHANNEL] = false;
                        debug_printf("btcomms_packet_handler():   RFCOMM Debug channel is closed\n");
                    } else {
                        debug_printf("btcomms_packet_handler():   Got a channel closed event for an unknown channel!\n");
                    }
                    break;
                
                default:
                    break;
            }
            break;

        case RFCOMM_DATA_PACKET:
            if (channel == rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL]) {
                // Place the incoming characters into our input buffer
                for (int i=0; i<size; i++) fifo_in_write(CLI_BUFFER, (char)packet[i]);
            } else if (channel == rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL]) {
                // Place the incoming characters into our input buffer
                for (int i=0; i<size; i++) fifo_in_write(DEBUG_BUFFER, (char)packet[i]);
            } else {
                debug_printf("btcomms_packet_handler(): Received RFCOMM_DATA_PACKET event with CID %u - Ignoring\n", channel);
            }
            break;

        default:
            break;
    }
}

static void btcomms_one_shot_timer_setup(void)
{
    // Initialise the CLI
    cli_initialise();

    // Set one-shot timer
    btcomms_cli_process_timer.process = &btcomms_cli_process_handler;
    btstack_run_loop_set_timer(&btcomms_cli_process_timer, BTCLIPROCESS_PERIOD_MS);
    btstack_run_loop_add_timer(&btcomms_cli_process_timer);
}

// Handler for the Bluetooth CLI Process timer
static void btcomms_cli_process_handler(struct btstack_timer_source *ts)
{
    // Ensure the RFCOMM channel for the CLI is valid (open and connected)
    if (channel_open[SPP_CLI_SERVER_CHANNEL]) {
        // Process the CLI
        cli_process();

        // Check the CLI output buffer
        if (!fifo_is_out_empty(CLI_BUFFER)) {
            // Ask for a send event on the CLI channel
            rfcomm_request_can_send_now_event(rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL]);
        }
    }

    // Ensure the RFCOMM channel for the Debug is valid (open and connected)
    if (channel_open[SPP_DEBUG_SERVER_CHANNEL]) {
        // Check the DEBUG output buffer
        if (!fifo_is_out_empty(DEBUG_BUFFER)) {
            // Ask for a send event on the DEBUG channel
            rfcomm_request_can_send_now_event(rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL]);
        }
    }

    // Set up the next timer shot
    btstack_run_loop_set_timer(ts, BTCLIPROCESS_PERIOD_MS);
    btstack_run_loop_add_timer(ts);
} 

// A printf like function but outputs via BT SPP for CLI
void btcomms_printf_cli(const char *fmt, ...)
{
    if (channel_open[SPP_CLI_SERVER_CHANNEL]) {
        va_list args;
        va_start(args, fmt);
        vsprintf(lineBuffer, fmt, args);
        va_end(args);

        // Copy the output string to the output buffer
        for (uint16_t i = 0; i < strlen(lineBuffer); i++) fifo_out_write(CLI_BUFFER, lineBuffer[i]);
    }
}

// A printf like function but outputs via BT SPP for debug
void btcomms_printf_debug(const char *fmt, ...)
{
    if (channel_open[SPP_DEBUG_SERVER_CHANNEL]) {
        va_list args;
        va_start(args, fmt);
        vsprintf(lineBuffer, fmt, args);
        va_end(args);

        if (strlen(lineBuffer) >= LINE_BUFFER_SIZE) {
            debug_printf("btcomms_printf_debug(): Possible line buffer overrun\n"); 
        }

        // Copy the output string to the output buffer
        for (uint16_t i = 0; i < strlen(lineBuffer); i++) fifo_out_write(DEBUG_BUFFER, lineBuffer[i]);
    }
}