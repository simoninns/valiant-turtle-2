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
static uint16_t rfcomm_channel_id;
static uint8_t  spp_service_buffer[150];
static btstack_packet_callback_registration_t hci_event_callback_registration;
static bool channel_open;
btComms_state_t current_bt_state;

// Set up Serial Port Profile (SPP)
static void spp_service_setup(void)
{
    // register for HCI events
    hci_event_callback_registration.callback = &packet_handler;
    hci_add_event_handler(&hci_event_callback_registration);

    l2cap_init();
    rfcomm_init();
    rfcomm_register_service(packet_handler, RFCOMM_SERVER_CHANNEL, 0xffff);  // reserved channel, mtu limited by l2cap

    // init SDP, create record for SPP and register with SDP
    sdp_init();
    memset(spp_service_buffer, 0, sizeof(spp_service_buffer));
    spp_create_sdp_record(spp_service_buffer, sdp_create_service_record_handle(), RFCOMM_SERVER_CHANNEL, "Valiant Turtle SPP");
    btstack_assert(de_get_len( spp_service_buffer) <= sizeof(spp_service_buffer));
    sdp_register_service(spp_service_buffer);
}

// Bluetooth packet handler
static void packet_handler (uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
    UNUSED(channel);

    bd_addr_t event_addr;
    uint8_t   rfcomm_channel_nr;
    uint16_t  mtu;
    int i;

    switch (packet_type) {
        case HCI_EVENT_PACKET:
            switch (hci_event_packet_get_type(packet)) {
                case HCI_EVENT_PIN_CODE_REQUEST:
                    // inform about pin code request
                    debug_printf("Bluetooth: Pin code request - using '0000'\n");
                    current_bt_state = BTCOMMS_PAIRING;
                    hci_event_pin_code_request_get_bd_addr(packet, event_addr);
                    gap_pin_code_response(event_addr, "0000");
                    break;

                case HCI_EVENT_USER_CONFIRMATION_REQUEST:
                    // ssp: inform about user confirmation request
                    debug_printf("Bluetooth: SSP User Confirmation Request with numeric value '%06"PRIu32"'\n", little_endian_read_32(packet, 8));
                    debug_printf("Bluetooth: SSP User Confirmation Auto accept\n");
                    current_bt_state = BTCOMMS_PAIRING;
                    break;

                case RFCOMM_EVENT_INCOMING_CONNECTION:
                    rfcomm_event_incoming_connection_get_bd_addr(packet, event_addr);
                    rfcomm_channel_nr = rfcomm_event_incoming_connection_get_server_channel(packet);
                    rfcomm_channel_id = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);
                    debug_printf("Bluetooth: RFCOMM channel %u requested for client %s\n", rfcomm_channel_nr, bd_addr_to_str(event_addr));
                    rfcomm_accept_connection(rfcomm_channel_id);
                    break;
               
                case RFCOMM_EVENT_CHANNEL_OPENED:
                    if (rfcomm_event_channel_opened_get_status(packet)) {
                        debug_printf("Bluetooth: RFCOMM channel open failed, status 0x%02x\n", rfcomm_event_channel_opened_get_status(packet));
                    } else {
                        rfcomm_channel_id = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        mtu = rfcomm_event_channel_opened_get_max_frame_size(packet);
                        debug_printf("Bluetooth: RFCOMM channel open succeeded. New RFCOMM Channel ID %u, max frame size %u\n", rfcomm_channel_id, mtu);
                        current_bt_state = BTCOMMS_CONNECTED;
                        channel_open = true;
                    }
                    break;
                case RFCOMM_EVENT_CAN_SEND_NOW:
                    // Output the contents of the output buffer
                    int16_t pos = 0;
                    char outputLine[128];
                    bool finished = false;
                    while (!finished) {
                        outputLine[pos] = fifo_out_read();
                        if (outputLine[pos] == 0) finished = true;
                        if (pos == 126) {
                            outputLine[pos+1] = 0;
                            finished = true;
                        }
                        pos++;
                    }

                    if (pos != 0) {
                        rfcomm_send(rfcomm_channel_id, (uint8_t*) outputLine, (uint16_t) pos);
                    }
                    break;

                case RFCOMM_EVENT_CHANNEL_CLOSED:
                    debug_printf("Bluetooth: RFCOMM channel is closed\n");
                    rfcomm_channel_id = 0;
                    current_bt_state = BTCOMMS_DISCONNECTED;
                    channel_open = false;
                    break;
                
                default:
                    break;
            }
            break;

        case RFCOMM_DATA_PACKET:
            // Place the incoming characters into our input buffer
            for (i=0;i<size;i++) fifo_in_write((char)packet[i]);
            break;

        default:
            break;
    }
}

// Initialise the Bluetooth stack and functionality
void btcomms_initialise(void)
{
    channel_open = false;
    current_bt_state = BTCOMMS_OFF;

    // Set up the FIFO buffer for incoming characters
    fifo_initialise();

    one_shot_timer_setup();
    spp_service_setup();

    gap_discoverable_control(1);
    gap_ssp_set_io_capability(SSP_IO_CAPABILITY_DISPLAY_YES_NO);

    // Use the following to include the HW Address in the device name
    //gap_set_local_name("VT2 00:00:00:00:00:00");
    gap_set_local_name("Valiant Turtle 2");

    // Power on the Bluetooth device
    hci_power_control(HCI_POWER_ON);
    current_bt_state = BTCOMMS_DISCONNECTED;

    debug_printf("Bluetooth: HCI is powered on\r\n");
}

static void one_shot_timer_setup(void)
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
    // Ensure the RFCOMM channel is valid
    if (channel_open) {
        // Process the CLI
        cli_process();

        // Check the output buffer
        if (!fifo_is_out_empty()) {
            // Ask for a send event
            rfcomm_request_can_send_now_event(rfcomm_channel_id);
        }
    } else {
        // If the channel is lost; hold the CLI in reset
        cli_initialise();
    }

    // Set up the next timer shot
    btstack_run_loop_set_timer(ts, BTCLIPROCESS_PERIOD_MS);
    btstack_run_loop_add_timer(ts);
} 

// Get the current bluetooth state
btComms_state_t btcomms_get_status(void)
{
    return current_bt_state;
}

// A printf like function but outputs via BT SPP
void btcomms_printf(const char *fmt, ...)
{
    static char lineBuffer[256];

    va_list args;
    va_start(args, fmt);
    vsprintf(lineBuffer, fmt, args);
    va_end(args);

    // Copy the output string to the output buffer
    for (uint16_t i = 0; i < strlen(lineBuffer); i++) fifo_out_write(lineBuffer[i]);
}