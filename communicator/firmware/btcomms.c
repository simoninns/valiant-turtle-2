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
static btstack_timer_source_t btcomms_process_timer;
static btstack_packet_callback_registration_t hci_event_callback_registration;
static btstack_context_callback_registration_t handle_sdp_client_query_request;

static bd_addr_t peer_addr[BTCOMMS_MAX_CLIENTS];
static btcomms_state_t current_bt_state[BTCOMMS_MAX_CLIENTS];
static bool channel_open[BTCOMMS_MAX_CLIENTS];
static uint16_t rfcomm_channel_id[BTCOMMS_MAX_CLIENTS];

char *sendBuffer[BTCOMMS_MAX_CLIENTS];

void btcomms_initialise(void)
{
     // Set initial state
    for (int i = 0; i < BTCOMMS_MAX_CLIENTS; i++) {
        channel_open[i] = false;
        current_bt_state[i] = BTCOMMS_OFF;
        rfcomm_channel_id[i] = 0;
    }

    // Set up the FIFO buffers for incoming and outgoing characters
    fifo_initialise();

    // Initialise the L2CAP and RFCOMM stacks
    l2cap_init();
    rfcomm_init();

    // Register for HCI events
    hci_event_callback_registration.callback = &btcomms_packet_handler;
    hci_add_event_handler(&hci_event_callback_registration);

    // Initialise SSP
    gap_ssp_set_io_capability(SSP_IO_CAPABILITY_DISPLAY_YES_NO);

    // Power on the Bluetooth device
    hci_power_control(HCI_POWER_ON);

    // Set state to disconnected
    for (int i = 0; i < BTCOMMS_MAX_CLIENTS; i++) {
        current_bt_state[i] = BTCOMMS_DISCONNECTED;
    }

    // Start the BT processing timer
    btcomms_one_shot_timer_setup();

    printf_debug("btcomms_initialise(): Bluetooth is powered on\r\n");
}

// Start scanning for a server using COD
static void btcomms_start_scan()
{
    printf_debug("btcomms_start_scan(): Starting inquiry scan...\r\n");
    current_bt_state[0] = BTCOMMS_COD_SCANNING;
    gap_inquiry_start(SCAN_INQUIRY_INTERVAL);
}

// Stop scanning for a server using COD
static void btcomms_stop_scan()
{
    printf_debug("btcomms_stop_scan(): Stopping inquiry scan...\r\n");
    current_bt_state[0] = BTCOMMS_COD_SCAN_COMPLETE;
    gap_inquiry_stop();
}

// RFCOMM event handler
static void btcomms_handle_query_rfcomm_event(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
    UNUSED(packet_type);
    UNUSED(channel);
    UNUSED(size);

    switch (hci_event_packet_get_type(packet)){
        case SDP_EVENT_QUERY_RFCOMM_SERVICE:
            printf_debug("btcomms_handle_query_rfcomm_event(): SDP_EVENT_QUERY_RFCOMM_SERVICE\r\n");
            rfcomm_channel_id[0] = sdp_event_query_rfcomm_service_get_rfcomm_channel(packet);
            break;
        case SDP_EVENT_QUERY_COMPLETE:
            // Did the event query fail?
            if (sdp_event_query_complete_get_status(packet)){
                printf_debug("btcomms_handle_query_rfcomm_event(): SDP query failed, status 0x%02x\r\n", sdp_event_query_complete_get_status(packet));
                btcomms_show_error(sdp_event_query_complete_get_status(packet));
                btcomms_start_scan();
                break;
            }

            // Did we get a valid RFCOMM channel ID?
            if (rfcomm_channel_id[0] == 0){
                printf_debug("btcomms_handle_query_rfcomm_event(): No SPP service found\r\n");
                break;
            }

            // Query successful
            printf_debug("btcomms_handle_query_rfcomm_event(): SDP query done, found RFCOMM server channel 0x%02x.\r\n", rfcomm_channel_id[0]);
            rfcomm_create_channel(btcomms_packet_handler, peer_addr[0], rfcomm_channel_id[0], NULL); 
            break;
        default:
            break;
    }
}

// SDP client query handler
static void btcomms_handle_start_sdp_client_query(void * context)
{
    UNUSED(context);
    if (current_bt_state[0] != BTCOMMS_SEND_SDP_QUERY) return;
    current_bt_state[0] = BTCOMMS_SDP_QUERY_SENT;
    sdp_client_query_rfcomm_channel_and_name_for_uuid(&btcomms_handle_query_rfcomm_event, peer_addr[0], BLUETOOTH_ATTRIBUTE_PUBLIC_BROWSE_ROOT);
    printf_debug("btcomms_handle_start_sdp_client_query(): Started SDP client query for channel and uuid\r\n");            
}

// General communications packet handler
static void btcomms_packet_handler(uint8_t packet_type, uint16_t channel, uint8_t *packet, uint16_t size)
{
    UNUSED(channel);

    bd_addr_t event_addr;
    uint32_t class_of_device;
    uint16_t requesting_cid;
    uint8_t rfcomm_server_channel;

    // SPP
    uint16_t rfcomm_mtu;
    uint16_t rfcomm_cid = 0;

	switch (packet_type) {
		case HCI_EVENT_PACKET:
			switch (hci_event_packet_get_type(packet)) {

                case BTSTACK_EVENT_STATE:
                    if (btstack_event_state_get_state(packet) != HCI_STATE_WORKING) return;
                    btcomms_start_scan();
                    break;

                case GAP_EVENT_INQUIRY_RESULT:
                    if (current_bt_state[0] != BTCOMMS_COD_SCANNING) break;
                    class_of_device = gap_event_inquiry_result_get_class_of_device(packet);
                    gap_event_inquiry_result_get_bd_addr(packet, event_addr);
                    if (class_of_device == BT_CLASS_OF_DEVICE){
                        memcpy(peer_addr[0], event_addr, 6);
                        printf_debug("btcomms_packet_handler(): COD matched peer found with BT MAC: %s\r\n", bd_addr_to_str(peer_addr[0]));
                        btcomms_stop_scan();
                    } else {
                        printf_debug("btcomms_packet_handler(): Device found: %s with incorrect COD: 0x%06x\r\n",
                            bd_addr_to_str(event_addr), (int) class_of_device);
                    }                        
                    break;
                    
                case GAP_EVENT_INQUIRY_COMPLETE:
                    switch (current_bt_state[0]){
                        case BTCOMMS_COD_SCANNING:
                            // The inquiry time period has elapsed and we didn't find a suitable peer...                    
                            printf_debug("btcomms_packet_handler(): Inquiry complete - Peer not found, restarting scan\r\n");
                            btcomms_start_scan();
                            break;                        
                        case BTCOMMS_COD_SCAN_COMPLETE:
                            // The inquiry found a suitable peer with the correct COD
                            printf_debug("btcomms_packet_handler(): Peer with correct COD found. Now starting to connect and query for available SPP services\r\n");
                            current_bt_state[0] = BTCOMMS_SEND_SDP_QUERY;
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
                    printf_debug("btcomms_packet_handler(): SSP User Confirmation Request with numeric value '%06"PRIu32"'\r\n",
                        little_endian_read_32(packet, 8));
                    printf_debug("btcomms_packet_handler(): SSP User Confirmation Auto accept\n");
                    break;

                case RFCOMM_EVENT_INCOMING_CONNECTION:
                    rfcomm_event_incoming_connection_get_bd_addr(packet, event_addr);
                    rfcomm_server_channel = rfcomm_event_incoming_connection_get_server_channel(packet);
                    rfcomm_cid = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);
                    printf_debug("btcomms_packet_handler(): RFCOMM channel 0x%02x requested for %s\r\n", rfcomm_server_channel, bd_addr_to_str(event_addr));
                    rfcomm_accept_connection(rfcomm_cid);
					break;
					
				case RFCOMM_EVENT_CHANNEL_OPENED:
					if (rfcomm_event_channel_opened_get_status(packet)) {
                        printf_debug("btcomms_packet_handler(): RFCOMM channel open failed, status 0x%02x\r\n", rfcomm_event_channel_opened_get_status(packet));
                    } else {
                        rfcomm_cid = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        rfcomm_mtu = rfcomm_event_channel_opened_get_max_frame_size(packet);
                        printf_debug("btcomms_packet_handler(): RFCOMM channel open succeeded. New RFCOMM Channel ID 0x%02x, max frame size %u\r\n", rfcomm_cid, rfcomm_mtu);

                        current_bt_state[0] = BTCOMMS_CONNECTED;
                        channel_open[0] = true;

                        // Malloc the virtual port's send buffer size to match the MTU of the channel
                        sendBuffer[0] = malloc(sizeof(char*) * rfcomm_mtu);
                        
                        if (!sendBuffer[0]) {
                            printf_debug("btcomms_packet_handler(): Send buffer memory allocation failed for server channel %u\n", rfcomm_server_channel+1); 
                            panic("Ran out of memory when allocating send buffer in btcomms_packet_handler()!\n");
                        }

                        // Disable page/inquiry scan to get max performance
                        gap_discoverable_control(0);
                        gap_connectable_control(0);
                    }
					break;

                case RFCOMM_EVENT_CHANNEL_CLOSED:
                    printf_debug("btcomms_packet_handler(): RFCOMM channel closed\r\n");

                    // Set the channel state to disconnected and free the send buffer memory
                    current_bt_state[0] = BTCOMMS_DISCONNECTED;
                    channel_open[0] = false;
                    rfcomm_channel_id[0] = 0;
                    free(sendBuffer[0]);

                    // Start scanning again
                    gap_discoverable_control(1);
                    gap_connectable_control(1);
                    btcomms_start_scan();
                    break;

                case RFCOMM_EVENT_CAN_SEND_NOW:
                    requesting_cid = rfcomm_event_can_send_now_get_rfcomm_cid(packet);

                    // Match the requesting CID to an open server channel (only 1 channel supported at the moment)
                    rfcomm_server_channel = 0;

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
                    break;
			}
            break;
                        
        case RFCOMM_DATA_PACKET:
            // Place the incoming characters into the associated channel's input FIFO
            for (int i=0; i<size; i++) {
                fifo_in_write(0, (char)packet[i]);
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
    for (int i = 0; i < BTCOMMS_MAX_CLIENTS; i++) {
        if (channel_open[i]) {
            // Check the output FIFO buffer for waiting data
            if (!fifo_is_out_empty(i)) {
                // Ask for a send event on the specified channel
                rfcomm_request_can_send_now_event(rfcomm_channel_id[i]);
            }

            // Check the input FIFO buffer for waiting data
            if (!fifo_is_in_empty(i)) {
                while (!fifo_is_in_empty(i)) {
                    char c = (int)fifo_in_read(i);
                    uart_putc(UART0_ID, c);
                }
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
    return fifo_out_write(channel, c);
}

// Taken from https://github.com/bluekitchen/btstack/blob/master/src/bluetooth.h#L211
void btcomms_show_error(int32_t error_code)
{
    if (error_code == ERROR_CODE_SUCCESS) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_SUCCESS\r\n", error_code);
    if (error_code == ERROR_CODE_UNKNOWN_HCI_COMMAND) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_UNKNOWN_HCI_COMMAND\r\n", error_code);
    if (error_code == ERROR_CODE_UNKNOWN_CONNECTION_IDENTIFIER) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_UNKNOWN_CONNECTION_IDENTIFIER\r\n", error_code);
    if (error_code == ERROR_CODE_HARDWARE_FAILURE) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_HARDWARE_FAILURE\r\n", error_code);
    if (error_code == ERROR_CODE_PAGE_TIMEOUT) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_PAGE_TIMEOUT\r\n", error_code);
    if (error_code == ERROR_CODE_AUTHENTICATION_FAILURE) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_AUTHENTICATION_FAILURE\r\n", error_code);
    if (error_code == ERROR_CODE_PIN_OR_KEY_MISSING) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_PIN_OR_KEY_MISSING\r\n", error_code);
    if (error_code == ERROR_CODE_MEMORY_CAPACITY_EXCEEDED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_MEMORY_CAPACITY_EXCEEDED\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_TIMEOUT) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_TIMEOUT\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_LIMIT_EXCEEDED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_LIMIT_EXCEEDED\r\n", error_code);
    if (error_code == ERROR_CODE_SYNCHRONOUS_CONNECTION_LIMIT_TO_A_DEVICE_EXCEEDED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_SYNCHRONOUS_CONNECTION_LIMIT_TO_A_DEVICE_EXCEEDED\r\n", error_code);
    if (error_code == ERROR_CODE_ACL_CONNECTION_ALREADY_EXISTS) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_ACL_CONNECTION_ALREADY_EXISTS\r\n", error_code);
    if (error_code == ERROR_CODE_COMMAND_DISALLOWED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_COMMAND_DISALLOWED\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_REJECTED_DUE_TO_LIMITED_RESOURCES) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_REJECTED_DUE_TO_LIMITED_RESOURCES\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_REJECTED_DUE_TO_SECURITY_REASONS) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_REJECTED_DUE_TO_SECURITY_REASONS\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_REJECTED_DUE_TO_UNACCEPTABLE_BD_ADDR) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_REJECTED_DUE_TO_UNACCEPTABLE_BD_ADDR\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_ACCEPT_TIMEOUT_EXCEEDED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_ACCEPT_TIMEOUT_EXCEEDED\r\n", error_code);
    if (error_code == ERROR_CODE_UNSUPPORTED_FEATURE_OR_PARAMETER_VALUE) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_UNSUPPORTED_FEATURE_OR_PARAMETER_VALUE\r\n", error_code);
    if (error_code == ERROR_CODE_INVALID_HCI_COMMAND_PARAMETERS) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_INVALID_HCI_COMMAND_PARAMETERS\r\n", error_code);
    if (error_code == ERROR_CODE_REMOTE_USER_TERMINATED_CONNECTION) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_REMOTE_USER_TERMINATED_CONNECTION\r\n", error_code);
    if (error_code == ERROR_CODE_REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_LOW_RESOURCES) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_LOW_RESOURCES\r\n", error_code); 
    if (error_code == ERROR_CODE_REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_POWER_OFF) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_POWER_OFF\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_TERMINATED_BY_LOCAL_HOST) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_TERMINATED_BY_LOCAL_HOST\r\n", error_code);
    if (error_code == ERROR_CODE_REPEATED_ATTEMPTS) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_REPEATED_ATTEMPTS\r\n", error_code);
    if (error_code == ERROR_CODE_PAIRING_NOT_ALLOWED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_PAIRING_NOT_ALLOWED\r\n", error_code);
    if (error_code == ERROR_CODE_UNKNOWN_LMP_PDU) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_UNKNOWN_LMP_PDU\r\n", error_code);                  
    if (error_code == ERROR_CODE_UNSUPPORTED_REMOTE_FEATURE_UNSUPPORTED_LMP_FEATURE ) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_UNSUPPORTED_REMOTE_FEATURE_UNSUPPORTED_LMP_FEATURE\r\n", error_code);
    if (error_code == ERROR_CODE_SCO_OFFSET_REJECTED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_SCO_OFFSET_REJECTED\r\n", error_code);
    if (error_code == ERROR_CODE_SCO_INTERVAL_REJECTED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_SCO_INTERVAL_REJECTED\r\n", error_code);
    if (error_code == ERROR_CODE_SCO_AIR_MODE_REJECTED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_SCO_AIR_MODE_REJECTED\r\n", error_code);
    if (error_code == ERROR_CODE_INVALID_LMP_PARAMETERS_INVALID_LL_PARAMETERS ) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_INVALID_LMP_PARAMETERS_INVALID_LL_PARAMETERS\r\n", error_code);
    if (error_code == ERROR_CODE_UNSPECIFIED_ERROR) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_UNSPECIFIED_ERROR\r\n", error_code);
    if (error_code == ERROR_CODE_UNSUPPORTED_LMP_PARAMETER_VALUE_UNSUPPORTED_LL_PARAMETER_VALUE) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_UNSUPPORTED_LMP_PARAMETER_VALUE_UNSUPPORTED_LL_PARAMETER_VALUE\r\n", error_code);
    if (error_code == ERROR_CODE_ROLE_CHANGE_NOT_ALLOWED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_ROLE_CHANGE_NOT_ALLOWED\r\n", error_code);
    if (error_code == ERROR_CODE_LMP_RESPONSE_TIMEOUT_LL_RESPONSE_TIMEOUT) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_LMP_RESPONSE_TIMEOUT_LL_RESPONSE_TIMEOUT\r\n", error_code);
    if (error_code == ERROR_CODE_LMP_ERROR_TRANSACTION_COLLISION) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_LMP_ERROR_TRANSACTION_COLLISION\r\n", error_code);
    if (error_code == ERROR_CODE_LMP_PDU_NOT_ALLOWED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_LMP_PDU_NOT_ALLOWED\r\n", error_code);
    if (error_code == ERROR_CODE_ENCRYPTION_MODE_NOT_ACCEPTABLE) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_ENCRYPTION_MODE_NOT_ACCEPTABLE\r\n", error_code);
    if (error_code == ERROR_CODE_LINK_KEY_CANNOT_BE_CHANGED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_LINK_KEY_CANNOT_BE_CHANGED\r\n", error_code);
    if (error_code == ERROR_CODE_REQUESTED_QOS_NOT_SUPPORTED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_REQUESTED_QOS_NOT_SUPPORTED\r\n", error_code);
    if (error_code == ERROR_CODE_INSTANT_PASSED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_INSTANT_PASSED\r\n", error_code);
    if (error_code == ERROR_CODE_PAIRING_WITH_UNIT_KEY_NOT_SUPPORTED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_PAIRING_WITH_UNIT_KEY_NOT_SUPPORTED\r\n", error_code);
    if (error_code == ERROR_CODE_DIFFERENT_TRANSACTION_COLLISION) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_DIFFERENT_TRANSACTION_COLLISION\r\n", error_code);
    if (error_code == ERROR_CODE_RESERVED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_RESERVED\r\n", error_code);
    if (error_code == ERROR_CODE_QOS_UNACCEPTABLE_PARAMETER) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_QOS_UNACCEPTABLE_PARAMETER\r\n", error_code);
    if (error_code == ERROR_CODE_QOS_REJECTED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_QOS_REJECTED\r\n", error_code);
    if (error_code == ERROR_CODE_CHANNEL_CLASSIFICATION_NOT_SUPPORTED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CHANNEL_CLASSIFICATION_NOT_SUPPORTED\r\n", error_code);
    if (error_code == ERROR_CODE_INSUFFICIENT_SECURITY) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_INSUFFICIENT_SECURITY\r\n", error_code);
    if (error_code == ERROR_CODE_PARAMETER_OUT_OF_MANDATORY_RANGE) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_PARAMETER_OUT_OF_MANDATORY_RANGE\r\n", error_code);
    if (error_code == ERROR_CODE_ROLE_SWITCH_PENDING) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_ROLE_SWITCH_PENDING\r\n", error_code);
    if (error_code == ERROR_CODE_RESERVED_SLOT_VIOLATION) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_RESERVED_SLOT_VIOLATION\r\n", error_code);
    if (error_code == ERROR_CODE_ROLE_SWITCH_FAILED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_ROLE_SWITCH_FAILED\r\n", error_code);
    if (error_code == ERROR_CODE_EXTENDED_INQUIRY_RESPONSE_TOO_LARGE) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_EXTENDED_INQUIRY_RESPONSE_TOO_LARGE\r\n", error_code);
    if (error_code == ERROR_CODE_SECURE_SIMPLE_PAIRING_NOT_SUPPORTED_BY_HOST) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_SECURE_SIMPLE_PAIRING_NOT_SUPPORTED_BY_HOST\r\n", error_code);
    if (error_code == ERROR_CODE_HOST_BUSY_PAIRING) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_HOST_BUSY_PAIRING\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_REJECTED_DUE_TO_NO_SUITABLE_CHANNEL_FOUND) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_REJECTED_DUE_TO_NO_SUITABLE_CHANNEL_FOUND\r\n", error_code);
    if (error_code == ERROR_CODE_CONTROLLER_BUSY) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONTROLLER_BUSY\r\n", error_code);
    if (error_code == ERROR_CODE_UNACCEPTABLE_CONNECTION_PARAMETERS) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_UNACCEPTABLE_CONNECTION_PARAMETERS\r\n", error_code);
    if (error_code == ERROR_CODE_DIRECTED_ADVERTISING_TIMEOUT) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_DIRECTED_ADVERTISING_TIMEOUT\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_TERMINATED_DUE_TO_MIC_FAILURE) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_TERMINATED_DUE_TO_MIC_FAILURE\r\n", error_code);
    if (error_code == ERROR_CODE_CONNECTION_FAILED_TO_BE_ESTABLISHED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_CONNECTION_FAILED_TO_BE_ESTABLISHED\r\n", error_code);
    if (error_code == ERROR_CODE_MAC_CONNECTION_FAILED) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_MAC_CONNECTION_FAILED\r\n", error_code);
    if (error_code == ERROR_CODE_COARSE_CLOCK_ADJUSTMENT_REJECTED_BUT_WILL_TRY_TO_ADJUST_USING_CLOCK_DRAGGING) printf_debug("btcomms_show_error(): Error code %d - ERROR_CODE_COARSE_CLOCK_ADJUSTMENT_REJECTED_BUT_WILL_TRY_TO_ADJUST_USING_CLOCK_DRAGGING\r\n", error_code);
}