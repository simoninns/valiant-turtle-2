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

btComms_state_t current_bt_state[2];
static bool channel_open[2];
static uint16_t rfcomm_channel_id[2];

char *sendBuffer[2];

// Initialise the Bluetooth stack and functionality
void btcomms_initialise(void)
{
    debug_printf("btcomms_initialise(): Initialising Bluetooth\n");
    // Set initial state
    channel_open[SPP_CLI_SERVER_CHANNEL-1] = false;
    channel_open[SPP_DEBUG_SERVER_CHANNEL-1] = false;
    current_bt_state[SPP_CLI_SERVER_CHANNEL-1] = BTCOMMS_OFF;
    current_bt_state[SPP_DEBUG_SERVER_CHANNEL-1] = BTCOMMS_OFF;

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
    current_bt_state[SPP_CLI_SERVER_CHANNEL-1] = BTCOMMS_DISCONNECTED;
    current_bt_state[SPP_DEBUG_SERVER_CHANNEL-1] = BTCOMMS_DISCONNECTED;

    debug_printf("btcomms_initialise(): Bluetooth is powered on\n");
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
    memset(spp_service_buffer[SPP_CLI_SERVER_CHANNEL-1], 0, sizeof(spp_service_buffer[SPP_CLI_SERVER_CHANNEL-1]));
    spp_create_sdp_record(spp_service_buffer[SPP_CLI_SERVER_CHANNEL-1], sdp_create_service_record_handle(), SPP_CLI_SERVER_CHANNEL, "Valiant Turtle CLI");
    btstack_assert(de_get_len(spp_service_buffer[SPP_CLI_SERVER_CHANNEL-1]) <= sizeof(spp_service_buffer[SPP_CLI_SERVER_CHANNEL-1]));
    sdp_register_service(spp_service_buffer[SPP_CLI_SERVER_CHANNEL-1]);

    // Set up SPP Channel 2 for Valiant Turtle Debug
    memset(spp_service_buffer[SPP_DEBUG_SERVER_CHANNEL-1], 0, sizeof(spp_service_buffer[SPP_DEBUG_SERVER_CHANNEL-1]));
    spp_create_sdp_record(spp_service_buffer[SPP_DEBUG_SERVER_CHANNEL-1], sdp_create_service_record_handle(), SPP_DEBUG_SERVER_CHANNEL, "Valiant Turtle Debug");
    btstack_assert(de_get_len(spp_service_buffer[SPP_DEBUG_SERVER_CHANNEL-1]) <= sizeof(spp_service_buffer[SPP_DEBUG_SERVER_CHANNEL-1]));
    sdp_register_service(spp_service_buffer[SPP_DEBUG_SERVER_CHANNEL-1]);
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
                // Incoming RFCOMM connection - map the RFCOMM CID to the server channel ID
                case RFCOMM_EVENT_INCOMING_CONNECTION:
                    rfcomm_event_incoming_connection_get_bd_addr(packet, event_addr);
                    rfcomm_server_channel = rfcomm_event_incoming_connection_get_server_channel(packet);
                    rfcomm_channel_id[rfcomm_server_channel-1] = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);
                    debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_INCOMING_CONNECTION event on server channel %u with CID %u\n", rfcomm_server_channel, rfcomm_channel_id[rfcomm_server_channel-1]);
                    
                    rfcomm_accept_connection(rfcomm_channel_id[rfcomm_server_channel-1]);
                    debug_printf("btcomms_packet_handler():   Connection request accepted from client %s\n", bd_addr_to_str(event_addr));
                    break;

                // RFCOMM channel opened - determine MTU and allocate send buffers accordingly               
                case RFCOMM_EVENT_CHANNEL_OPENED:
                    if (rfcomm_event_channel_opened_get_status(packet)) {
                        debug_printf("btcomms_packet_handler(): RFCOMM channel open FAILED, status 0x%02x\n", rfcomm_event_channel_opened_get_status(packet));
                    } else {
                        rfcomm_server_channel = rfcomm_event_channel_opened_get_server_channel(packet);
                        rfcomm_channel_id[rfcomm_server_channel-1] = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_CHANNEL_OPENED event on server channel %u with CID %u\n", rfcomm_server_channel, rfcomm_channel_id[rfcomm_server_channel-1]);

                        mtu = rfcomm_event_channel_opened_get_max_frame_size(packet);
                        if (rfcomm_server_channel == SPP_CLI_SERVER_CHANNEL) debug_printf("btcomms_packet_handler():   RFCOMM channel open succeeded (Valiant Turtle CLI) - max frame size %u\n", mtu);
                        else debug_printf("btcomms_packet_handler():   RFCOMM channel open succeeded (Valiant Turtle Debug) - max frame size %u\n", mtu);
                        current_bt_state[rfcomm_server_channel-1] = BTCOMMS_CONNECTED;
                        channel_open[rfcomm_server_channel-1] = true;

                        // Malloc the send buffer size to match the MTU of the channel
                        sendBuffer[rfcomm_server_channel-1] = malloc(sizeof(char*) * mtu);

                        if (!sendBuffer[rfcomm_server_channel-1]) {
                            debug_printf("btcomms_initialise(): Line buffer memory allocation failed for server channel %u\n", rfcomm_server_channel); 
                            panic("Ran out of memory when allocating send buffer in btcomms_packet_handler()!\n");
                        }
                    }
                    break;

                // RFCOMM channel has been closed - flag it as closed and free the send buffer memory
                case RFCOMM_EVENT_CHANNEL_CLOSED:
                    requesting_cid = rfcomm_event_channel_closed_get_rfcomm_cid(packet);
                    debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_CHANNEL_CLOSED event with CID %u\n", requesting_cid);

                    // Check if requesting CID belongs to the CLI channel
                    if (requesting_cid == rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL-1]) {
                        current_bt_state[SPP_CLI_SERVER_CHANNEL-1] = BTCOMMS_DISCONNECTED;
                        channel_open[SPP_CLI_SERVER_CHANNEL-1] = false;
                        free(sendBuffer[SPP_CLI_SERVER_CHANNEL-1]);
                        debug_printf("btcomms_packet_handler():   RFCOMM CLI channel is closed\n");
                    } else if (requesting_cid == rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL-1]) {
                        current_bt_state[SPP_DEBUG_SERVER_CHANNEL-1] = BTCOMMS_DISCONNECTED;
                        channel_open[SPP_DEBUG_SERVER_CHANNEL-1] = false;
                        free(sendBuffer[SPP_DEBUG_SERVER_CHANNEL-1]);
                        debug_printf("btcomms_packet_handler():   RFCOMM Debug channel is closed\n");
                    } else {
                        debug_printf("btcomms_packet_handler():   Got a channel closed event for an unknown channel!\n");
                    }
                    break;

                case RFCOMM_EVENT_CAN_SEND_NOW:
                    requesting_cid = rfcomm_event_can_send_now_get_rfcomm_cid(packet);

                    // Check which server channel the requesting CID belongs too...
                    if (requesting_cid == rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL-1]) {
                        int16_t max_frame_size = rfcomm_get_max_frame_size(rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL-1]);

                        // Output the contents of the CLI output FIFO
                        int16_t pos = 0;
                        bool finished = false;
                        while (!finished) {
                            sendBuffer[SPP_CLI_SERVER_CHANNEL-1][pos] = fifo_out_read(SPP_CLI_SERVER_CHANNEL-1);
                            if (sendBuffer[SPP_CLI_SERVER_CHANNEL-1][pos] == 0) finished = true;
                            if (pos == max_frame_size-2) {
                                sendBuffer[SPP_CLI_SERVER_CHANNEL-1][pos+1] = 0;
                                finished = true;
                            }
                            pos++;
                        }

                        if (pos != 0) rfcomm_send(rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL-1], (uint8_t*)sendBuffer[SPP_CLI_SERVER_CHANNEL-1], (uint16_t)pos);
                    } else if (requesting_cid == rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL-1]) {
                        int16_t max_frame_size = rfcomm_get_max_frame_size(rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL-1]);

                        // Output the contents of the Debug output FIFO
                        int16_t pos = 0;
                        bool finished = false;
                        while (!finished) {
                            sendBuffer[SPP_DEBUG_SERVER_CHANNEL-1][pos] = fifo_out_read(SPP_DEBUG_SERVER_CHANNEL-1);
                            if (sendBuffer[SPP_DEBUG_SERVER_CHANNEL-1][pos] == 0) finished = true;
                            if (pos == max_frame_size-2) {
                                sendBuffer[SPP_DEBUG_SERVER_CHANNEL-1][pos+1] = 0;
                                finished = true;
                            }
                            pos++;
                        }

                        if (pos != 0) rfcomm_send(rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL-1], (uint8_t*)sendBuffer[SPP_DEBUG_SERVER_CHANNEL-1], (uint16_t)pos);
                    }
                    break;
                
                default:
                    // Received unhandled event
                    break;
            }
            break;

        case RFCOMM_DATA_PACKET:
            if (channel == rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL-1]) {
                // Place the incoming characters into our input FIFO
                for (int i=0; i<size; i++) fifo_in_write(SPP_CLI_SERVER_CHANNEL-1, (char)packet[i]);
            } else if (channel == rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL-1]) {
                // Place the incoming characters into our input FIFO
                for (int i=0; i<size; i++) fifo_in_write(SPP_DEBUG_SERVER_CHANNEL-1, (char)packet[i]);
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
    if (channel_open[SPP_CLI_SERVER_CHANNEL-1]) {
        // Process the CLI
        cli_process();

        // Check the CLI output buffer
        if (!fifo_is_out_empty(SPP_CLI_SERVER_CHANNEL-1)) {
            // Ask for a send event on the CLI channel
            rfcomm_request_can_send_now_event(rfcomm_channel_id[SPP_CLI_SERVER_CHANNEL-1]);
        }
    }

    // Ensure the RFCOMM channel for the Debug is valid (open and connected)
    if (channel_open[SPP_DEBUG_SERVER_CHANNEL-1]) {
        // Check the DEBUG output buffer
        if (!fifo_is_out_empty(SPP_DEBUG_SERVER_CHANNEL-1)) {
            // Ask for a send event on the DEBUG channel
            rfcomm_request_can_send_now_event(rfcomm_channel_id[SPP_DEBUG_SERVER_CHANNEL-1]);
        }
    }

    // Set up the next timer shot
    btstack_run_loop_set_timer(ts, BTCLIPROCESS_PERIOD_MS);
    btstack_run_loop_add_timer(ts);
} 

// A printf like function but outputs via BT SPP for CLI
void btcomms_printf_cli(const char *fmt, ...)
{
    if (channel_open[SPP_CLI_SERVER_CHANNEL-1]) {
        char lineBuffer[256];
        va_list args;
        va_start(args, fmt);

        int rc = vsnprintf(lineBuffer, 256, fmt, args);
        if (rc == -1 || rc >= 256) {
            panic("btcomms_printf_cli(): Line buffer overflow\n");
        }

        va_end(args);

        // Copy the output string to the output buffer
        for (uint16_t i = 0; i < strlen(lineBuffer); i++) fifo_out_write(SPP_CLI_SERVER_CHANNEL-1, lineBuffer[i]);
    }
}

// A printf like function but outputs via BT SPP for debug
void btcomms_printf_debug(const char *fmt, ...)
{
    if (channel_open[SPP_DEBUG_SERVER_CHANNEL-1]) {
        char lineBuffer[256];
        va_list args;
        va_start(args, fmt);
        
        int rc = vsnprintf(lineBuffer, 256, fmt, args);
        if (rc == -1 || rc >= 265) {
            panic("btcomms_printf_debug(): Line buffer overflow\n");
        }

        va_end(args);

        // Copy the output string to the output buffer
        for (uint16_t i = 0; i < strlen(lineBuffer); i++) fifo_out_write(SPP_DEBUG_SERVER_CHANNEL-1, lineBuffer[i]);
    }
}