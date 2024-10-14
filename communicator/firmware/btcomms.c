/************************************************************************ 

    btcomms.c

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
#include "uart.h"
#include "fifo.h"

// Globals
static uint8_t rfcomm_server_channel;

static uint8_t   test_data[NUM_ROWS * NUM_COLS];
static uint16_t  spp_test_data_len;

static btstack_packet_callback_registration_t hci_event_callback_registration;
static btstack_context_callback_registration_t handle_sdp_client_query_request;

static bd_addr_t peer_addr;
static state_t state;

// SPP
static uint16_t  rfcomm_mtu;
static uint16_t  rfcomm_cid = 0;
// static uint32_t  data_to_send =  DATA_VOLUME;

// Throughput tracking globals
static uint32_t test_data_transferred;
static uint32_t test_data_start;

void btcomms_initialise(void)
{
    l2cap_init();
    rfcomm_init();

    // Register for HCI events
    hci_event_callback_registration.callback = &btcomms_packet_handler;
    hci_add_event_handler(&hci_event_callback_registration);

    // Initialise SSP
    gap_ssp_set_io_capability(SSP_IO_CAPABILITY_DISPLAY_YES_NO);

    // Power on the Bluetooth device
    hci_power_control(HCI_POWER_ON);

    printf_debug("btcomms_initialise(): BT powered on\r\n");
}

// Start scanning for a server using COD
static void btcomms_start_scan()
{
    printf_debug("btcomms_start_scan(): Starting inquiry scan...\r\n");
    state = W4_PEER_COD;
    gap_inquiry_start(SCAN_INQUIRY_INTERVAL);
}

// Stop scanning for a server using COD
static void btcomms_stop_scan()
{
    printf_debug("btcomms_stop_scan(): Stopping inquiry scan...\r\n");
    state = W4_SCAN_COMPLETE;
    gap_inquiry_stop();
}

// Throughput tracking - test reset
static void btcomms_test_reset()
{
    test_data_start = btstack_run_loop_get_time_ms();
    test_data_transferred = 0;
}

// Throughput tracking - track transferred
static void btcomms_test_track_transferred(int bytes_sent)
{
    test_data_transferred += bytes_sent;
    // evaluate
    uint32_t now = btstack_run_loop_get_time_ms();
    uint32_t time_passed = now - test_data_start;
    if (time_passed < REPORT_INTERVAL_MS) return;
    // print speed
    int bytes_per_second = test_data_transferred * 1000 / time_passed;
    printf_debug("btcomms_test_track_transferred(): %u bytes -> %u.%03u kB/s\r\n", (int) test_data_transferred, (int) bytes_per_second / 1000, bytes_per_second % 1000);

    // restart
    test_data_start = now;
    test_data_transferred  = 0;
}

// Create SPP test data
static void btcomms_spp_create_test_data()
{
    int x,y;
    for (y=0;y<NUM_ROWS;y++){
        for (x=0;x<NUM_COLS-2;x++){
            test_data[y*NUM_COLS+x] = '0' + (x % 10);
        }
        test_data[y*NUM_COLS+NUM_COLS-2] = '\n';
        test_data[y*NUM_COLS+NUM_COLS-1] = '\r';
    }
}

// Send SPP test data packet
static void btcomms_spp_send_packet()
{
    rfcomm_send(rfcomm_cid, (uint8_t*) test_data, spp_test_data_len);
    btcomms_test_track_transferred(spp_test_data_len);
    rfcomm_request_can_send_now_event(rfcomm_cid);
}

// RFCOMM event handler
static void btcomms_handle_query_rfcomm_event(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
    UNUSED(packet_type);
    UNUSED(channel);
    UNUSED(size);

    switch (hci_event_packet_get_type(packet)){
        case SDP_EVENT_QUERY_RFCOMM_SERVICE:
            rfcomm_server_channel = sdp_event_query_rfcomm_service_get_rfcomm_channel(packet);
            break;
        case SDP_EVENT_QUERY_COMPLETE:
            if (sdp_event_query_complete_get_status(packet)){
                printf_debug("btcomms_handle_query_rfcomm_event(): SDP query failed, status 0x%02x\r\n", sdp_event_query_complete_get_status(packet));
                break;
            } 
            if (rfcomm_server_channel == 0){
                printf_debug("btcomms_handle_query_rfcomm_event(): No SPP service found\r\n");
                break;
            }
            printf_debug("btcomms_handle_query_rfcomm_event(): SDP query done, found RFCOMM server channel 0x%02x.\r\n", rfcomm_server_channel);
            rfcomm_create_channel(btcomms_packet_handler, peer_addr, rfcomm_server_channel, NULL); 
            break;
        default:
            break;
    }
}

// SDP client query handler
static void btcomms_handle_start_sdp_client_query(void * context)
{
    UNUSED(context);
    if (state != W2_SEND_SDP_QUERY) return;
    state = W4_RFCOMM_CHANNEL;
    sdp_client_query_rfcomm_channel_and_name_for_uuid(&btcomms_handle_query_rfcomm_event, peer_addr, BLUETOOTH_ATTRIBUTE_PUBLIC_BROWSE_ROOT);               
}

// General communications packet handler
static void btcomms_packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
    UNUSED(channel);

    bd_addr_t event_addr;
    uint8_t   rfcomm_channel_nr;
    uint32_t class_of_device;

	switch (packet_type) {
		case HCI_EVENT_PACKET:
			switch (hci_event_packet_get_type(packet)) {

                case BTSTACK_EVENT_STATE:
                    if (btstack_event_state_get_state(packet) != HCI_STATE_WORKING) return;
                    btcomms_start_scan();
                    break;

                case GAP_EVENT_INQUIRY_RESULT:
                    if (state != W4_PEER_COD) break;
                    class_of_device = gap_event_inquiry_result_get_class_of_device(packet);
                    gap_event_inquiry_result_get_bd_addr(packet, event_addr);
                    if (class_of_device == BT_CLASS_OF_DEVICE){
                        memcpy(peer_addr, event_addr, 6);
                        printf_debug("btcomms_packet_handler(): COD Peer found with MAC: %s\r\n", bd_addr_to_str(peer_addr));
                        btcomms_stop_scan();
                    } else {
                        printf_debug("btcomms_packet_handler(): Device found: %s with incorrect COD: 0x%06x\r\n", bd_addr_to_str(event_addr), (int) class_of_device);
                    }                        
                    break;
                    
                case GAP_EVENT_INQUIRY_COMPLETE:
                    switch (state){
                        case W4_PEER_COD:
                            // The inquiry time period has elapsed and we didn't find a suitable peer...                    
                            printf_debug("btcomms_packet_handler(): Inquiry complete\r\n");
                            printf_debug("btcomms_packet_handler(): Peer not found, starting scan again\r\n");
                            btcomms_start_scan();
                            break;                        
                        case W4_SCAN_COMPLETE:
                            // The inquiry found a suitable peer with the correct COD
                            printf_debug("btcomms_packet_handler(): Peer with correct COD found. Now starting to\r\n");
                            printf_debug("btcomms_packet_handler(): connect and query for available SPP services\r\n");
                            state = W2_SEND_SDP_QUERY;
                            handle_sdp_client_query_request.callback = &btcomms_handle_start_sdp_client_query;
                            (void) sdp_client_register_query_callback(&handle_sdp_client_query_request);
                            break;
                        default:
                            break;
                    }
                    break;

                case HCI_EVENT_PIN_CODE_REQUEST:
                    // inform about pin code request
                    printf_debug("btcomms_packet_handler(): Pin code request - using '0000'\r\n");
                    hci_event_pin_code_request_get_bd_addr(packet, event_addr);
                    gap_pin_code_response(event_addr, "0000");
                    break;

                case HCI_EVENT_USER_CONFIRMATION_REQUEST:
                    // inform about user confirmation request
                    printf_debug("btcomms_packet_handler(): SSP User Confirmation Request with numeric value '%06"PRIu32"'\r\n", little_endian_read_32(packet, 8));
                    printf_debug("btcomms_packet_handler(): SSP User Confirmation Auto accept\n");
                    break;

                case RFCOMM_EVENT_INCOMING_CONNECTION:
                    rfcomm_event_incoming_connection_get_bd_addr(packet, event_addr);
                    rfcomm_channel_nr = rfcomm_event_incoming_connection_get_server_channel(packet);
                    rfcomm_cid = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);
                    printf_debug("btcomms_packet_handler(): RFCOMM channel 0x%02x requested for %s\r\n", rfcomm_channel_nr, bd_addr_to_str(event_addr));
                    rfcomm_accept_connection(rfcomm_cid);
					break;
					
				case RFCOMM_EVENT_CHANNEL_OPENED:
					if (rfcomm_event_channel_opened_get_status(packet)) {
                        printf_debug("btcomms_packet_handler(): RFCOMM channel open failed, status 0x%02x\r\n", rfcomm_event_channel_opened_get_status(packet));
                    } else {
                        rfcomm_cid = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        rfcomm_mtu = rfcomm_event_channel_opened_get_max_frame_size(packet);
                        printf_debug("btcomms_packet_handler(): RFCOMM channel open succeeded. New RFCOMM Channel ID 0x%02x, max frame size %u\r\n", rfcomm_cid, rfcomm_mtu);
                        btcomms_test_reset();

                        // disable page/inquiry scan to get max performance
                        gap_discoverable_control(0);
                        gap_connectable_control(0);

                        // configure test data
                        spp_test_data_len = rfcomm_mtu;
                        if (spp_test_data_len > sizeof(test_data)){
                            spp_test_data_len = sizeof(test_data);
                        }
                        btcomms_spp_create_test_data();
                        state = SENDING;
                        // start sending
                        rfcomm_request_can_send_now_event(rfcomm_cid);
                    }
					break;

                case RFCOMM_EVENT_CAN_SEND_NOW:
                    btcomms_spp_send_packet();
                    break;

                case RFCOMM_EVENT_CHANNEL_CLOSED:
                    printf_debug("btcomms_packet_handler(): RFCOMM channel closed\r\n");
                    rfcomm_cid = 0;

                    // re-enable page/inquiry scan again
                    gap_discoverable_control(1);
                    gap_connectable_control(1);
                    break;

                default:
                    break;
			}
            break;
                        
        case RFCOMM_DATA_PACKET:
            //btcomms_test_track_transferred(size);
            
            // optional: print received data as ASCII text
            printf("btcomms_packet_handler(): RCV: '");
            for (int i=0;i<size;i++){
                putchar(packet[i]);
            }
            printf("'\r\n");

            break;

        default:
            break;
	}
}
