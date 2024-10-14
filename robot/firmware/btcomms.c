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
static btstack_timer_source_t btcomms_process_timer;
static btstack_packet_callback_registration_t hci_event_callback_registration;

static uint8_t spp_service_buffer[SPP_PORTS][150];

btcomms_state_t current_bt_state[SPP_PORTS];
static bool channel_open[SPP_PORTS];
static uint16_t rfcomm_channel_id[SPP_PORTS];

char *sendBuffer[SPP_PORTS];

// Initialise the Bluetooth stack and functionality
void btcomms_initialise(void)
{
    debug_printf("btcomms_initialise(): Initialising Bluetooth SPP with %d available virtual ports\n", SPP_PORTS);

    // Set initial state
    for (int i = 0; i < SPP_PORTS; i++) {
        channel_open[i] = false;
        channel_open[i] = false;
        current_bt_state[i] = BTCOMMS_OFF;
        current_bt_state[i] = BTCOMMS_OFF;
    }

    // Set up the FIFO buffers for incoming and outgoing characters
    fifo_initialise();

    // Set up SPP services
    btcomms_spp_service_setup();

    gap_discoverable_control(1);
    gap_ssp_set_io_capability(SSP_IO_CAPABILITY_DISPLAY_YES_NO);

    // Use the following to include the HW Address in the device name
    gap_set_local_name("Valiant Turtle 2 00:00:00:00:00:00");

    // Set the Class Of Device
    gap_set_class_of_device(BT_CLASS_OF_DEVICE);

    // Power on the Bluetooth device
    hci_power_control(HCI_POWER_ON);

    // Set state to disconnected
    for (int i = 0; i < SPP_PORTS; i++) {
        current_bt_state[i] = BTCOMMS_DISCONNECTED;
    }

    // Start the BT processing timer
    btcomms_one_shot_timer_setup();

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

    // Register one service per required virtual port
    // Note: Channel numbering must start from 1
    for (int i = 0; i < SPP_PORTS; i++) {
        // Reserve channel i+1, MTU maximum is limited by l2cap
        rfcomm_register_service(btcomms_packet_handler, i+1, 0xffff);  // Reserve channel 1, mtu (0xffff) limited by l2cap
    }

    // Initialise SDP
    sdp_init();

    // Set up required SPP Channels
    for (int i = 0; i < SPP_PORTS; i++) {
        memset(spp_service_buffer[i], 0, sizeof(spp_service_buffer[i]));
        char id_string[64];
        sprintf(id_string, "Valiant Turtle SPP channel %d", i+1);
        spp_create_sdp_record(spp_service_buffer[i], sdp_create_service_record_handle(), i+1, id_string);
        btstack_assert(de_get_len(spp_service_buffer[i]) <= sizeof(spp_service_buffer[i]));
        sdp_register_service(spp_service_buffer[i]);
    }
}

// Bluetooth packet handler
static void btcomms_packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
    bd_addr_t event_addr;
    int8_t rfcomm_server_channel;
    uint16_t mtu;
    uint16_t requesting_cid;

    switch (packet_type) {
        case HCI_EVENT_PACKET:
            switch (hci_event_packet_get_type(packet)) {
                // Incoming RFCOMM connection - map the RFCOMM CID to the server channel ID
                case RFCOMM_EVENT_INCOMING_CONNECTION:
                    rfcomm_event_incoming_connection_get_bd_addr(packet, event_addr);
                    rfcomm_server_channel = rfcomm_event_incoming_connection_get_server_channel(packet) - 1; // Note: Channels start from 1, so we offset by -1
                    rfcomm_channel_id[rfcomm_server_channel] = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);
                    debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_INCOMING_CONNECTION event on server channel %u with CID %u\n", rfcomm_server_channel+1, rfcomm_channel_id[rfcomm_server_channel]);
                    
                    rfcomm_accept_connection(rfcomm_channel_id[rfcomm_server_channel]);
                    debug_printf("btcomms_packet_handler():   Connection request accepted from client %s\n", bd_addr_to_str(event_addr));
                    break;

                // RFCOMM channel opened - determine MTU and allocate send buffers accordingly               
                case RFCOMM_EVENT_CHANNEL_OPENED:
                    if (rfcomm_event_channel_opened_get_status(packet)) {
                        debug_printf("btcomms_packet_handler(): RFCOMM channel open FAILED, status 0x%02x\n", rfcomm_event_channel_opened_get_status(packet));
                    } else {
                        rfcomm_server_channel = rfcomm_event_channel_opened_get_server_channel(packet) - 1; // Note: Channels start from 1, so we offset by -1
                        rfcomm_channel_id[rfcomm_server_channel] = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_CHANNEL_OPENED event on server channel %u with CID %u\n", rfcomm_server_channel+1, rfcomm_channel_id[rfcomm_server_channel]);

                        mtu = rfcomm_event_channel_opened_get_max_frame_size(packet);
                        debug_printf("btcomms_packet_handler():   RFCOMM channel %d open succeeded - max frame size %u\n", rfcomm_server_channel+1, mtu);
                        current_bt_state[rfcomm_server_channel] = BTCOMMS_CONNECTED;
                        channel_open[rfcomm_server_channel] = true;

                        // Malloc the virtual port's send buffer size to match the MTU of the channel
                        sendBuffer[rfcomm_server_channel] = malloc(sizeof(char*) * mtu);

                        if (!sendBuffer[rfcomm_server_channel]) {
                            debug_printf("btcomms_packet_handler(): Send buffer memory allocation failed for server channel %u\n", rfcomm_server_channel+1); 
                            panic("Ran out of memory when allocating send buffer in btcomms_packet_handler()!\n");
                        }
                    }
                    break;

                // RFCOMM channel has been closed - flag it as closed and free the send buffer memory
                case RFCOMM_EVENT_CHANNEL_CLOSED:
                    requesting_cid = rfcomm_event_channel_closed_get_rfcomm_cid(packet);
                    debug_printf("btcomms_packet_handler(): Received RFCOMM_EVENT_CHANNEL_CLOSED event with CID %u\n", requesting_cid);

                    // Match the requesting CID to an open server channel
                    rfcomm_server_channel = -1;
                    for (int i = 0; i < SPP_PORTS; i++) {
                        if (requesting_cid == rfcomm_channel_id[i]) {
                            rfcomm_server_channel = i;
                            break;
                        }
                    }

                    if (rfcomm_server_channel == -1) {
                        debug_printf("btcomms_packet_handler(): Error CID %u doesn't belong to any open server channel!\n", requesting_cid);
                        panic("Something bad happened to the Bluetooth stack!");
                    }

                    // Set the channel state to disconnected and free the send buffer memory
                    current_bt_state[rfcomm_server_channel] = BTCOMMS_DISCONNECTED;
                    channel_open[rfcomm_server_channel] = false;
                    free(sendBuffer[rfcomm_server_channel]);
                    debug_printf("btcomms_packet_handler():   RFCOMM channel %u is closed\n", rfcomm_server_channel+1);

                    break;

                case RFCOMM_EVENT_CAN_SEND_NOW:
                    requesting_cid = rfcomm_event_can_send_now_get_rfcomm_cid(packet);

                    // Match the requesting CID to an open server channel
                    rfcomm_server_channel = -1;
                    for (int i = 0; i < SPP_PORTS; i++) {
                        if (requesting_cid == rfcomm_channel_id[i]) {
                            rfcomm_server_channel = i;
                            break;
                        }
                    }

                    if (rfcomm_server_channel == -1) {
                        debug_printf("btcomms_packet_handler(): Error CID %u doesn't belong to any open server channel!\n", requesting_cid);
                        panic("Something bad happened to the Bluetooth stack!");
                    }

                    // Send any waiting data from the send buffer
                    int16_t max_frame_size = rfcomm_get_max_frame_size(rfcomm_channel_id[rfcomm_server_channel]);

                    // Put the output FIFO contents into the send buffer
                    int16_t pos = 0;
                    bool finished = false;
                    while (!finished) {
                        sendBuffer[rfcomm_server_channel][pos] = fifo_out_read(rfcomm_server_channel);
                        if (sendBuffer[rfcomm_server_channel][pos] == 0) finished = true;
                        if (pos == max_frame_size-2) {
                            sendBuffer[rfcomm_server_channel][pos+1] = 0;
                            finished = true;
                        }
                        pos++;
                    }

                    // Transmit the send buffer
                    if (pos != 0) rfcomm_send(rfcomm_channel_id[rfcomm_server_channel], (uint8_t*)sendBuffer[rfcomm_server_channel], (uint16_t)pos);
                    break;
                
                default:
                    // Received unhandled event
                    break;
            }
            break;

        case RFCOMM_DATA_PACKET:
            // Match the requesting CID to an open server channel
            rfcomm_server_channel = -1;
            for (int i = 0; i < SPP_PORTS; i++) {
                if (channel == rfcomm_channel_id[i]) {
                    rfcomm_server_channel = i;
                    break;
                }
            }

            // Place the incoming characters into the associated channel's input FIFO
            for (int i=0; i<size; i++) {
                fifo_in_write(rfcomm_server_channel, (char)packet[i]);
            }
            break;

        default:
            break;
    }
}

static void btcomms_one_shot_timer_setup(void)
{
    // Set one-shot timer (to process FIFOs)
    btcomms_process_timer.process = &btcomms_process_handler;
    btstack_run_loop_set_timer(&btcomms_process_timer, SPP_PROCESS_PERIOD_MS);
    btstack_run_loop_add_timer(&btcomms_process_timer);
}

// Handler for the Bluetooth CLI Process timer
static void btcomms_process_handler(struct btstack_timer_source *ts)
{
    // Process any open channels
    for (int i = 0; i < SPP_PORTS; i++) {
        if (channel_open[i]) {
            // Check the output FIFO buffer for waiting data
            if (!fifo_is_out_empty(i)) {
                // Ask for a send event on the specified channel
                rfcomm_request_can_send_now_event(rfcomm_channel_id[i]);
            }
        }
    }

    // Set up the next timer shot
    btstack_run_loop_set_timer(ts, SPP_PROCESS_PERIOD_MS);
    btstack_run_loop_add_timer(ts);
}

// Returns true if a channel is open and false if it's closed
bool btcomms_is_channel_open(int8_t channel)
{
    return channel_open[channel];
}

// Read a character from a channel's FIFO input buffer
int btcomms_getchar(int8_t channel)
{
    int c = EOF;

    // If there is a character waiting, return it.  Otherwise return EOF
    if (!fifo_is_in_empty(channel)) c = (int)fifo_in_read(channel);

    return c;
}

// Write a character to a channel's FIFO output buffer
int btcomms_putchar(int8_t channel, char c)
{
    return fifo_out_write(channel, c);;
}