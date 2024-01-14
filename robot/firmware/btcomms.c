/************************************************************************ 

    btcomms.c

    Valiant Turtle 2 - Raspberry Pi Pico W Firmware
    Copyright (C) 2023 Simon Inns

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
#include "command.h"

static uint16_t rfcomm_channel_id;
static uint8_t  spp_service_buffer[150];
static btstack_packet_callback_registration_t hci_event_callback_registration;
static char lineBuffer[128];
static bool readyToSend;
char btCliBuffer[10];

// Set up Serial Port Profile (SPP)
static void spp_service_setup(void)
{
    readyToSend = false;

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
                    printf("Bluetooth: Pin code request - using '0000'\n");
                    hci_event_pin_code_request_get_bd_addr(packet, event_addr);
                    gap_pin_code_response(event_addr, "0000");
                    break;

                case HCI_EVENT_USER_CONFIRMATION_REQUEST:
                    // ssp: inform about user confirmation request
                    printf("Bluetooth: SSP User Confirmation Request with numeric value '%06"PRIu32"'\n", little_endian_read_32(packet, 8));
                    printf("Bluetooth: SSP User Confirmation Auto accept\n");
                    break;

                case RFCOMM_EVENT_INCOMING_CONNECTION:
                    rfcomm_event_incoming_connection_get_bd_addr(packet, event_addr);
                    rfcomm_channel_nr = rfcomm_event_incoming_connection_get_server_channel(packet);
                    rfcomm_channel_id = rfcomm_event_incoming_connection_get_rfcomm_cid(packet);
                    printf("Bluetooth: RFCOMM channel %u requested for %s\n", rfcomm_channel_nr, bd_addr_to_str(event_addr));
                    rfcomm_accept_connection(rfcomm_channel_id);
                    break;
               
                case RFCOMM_EVENT_CHANNEL_OPENED:
                    if (rfcomm_event_channel_opened_get_status(packet)) {
                        printf("Bluetooth: RFCOMM channel open failed, status 0x%02x\n", rfcomm_event_channel_opened_get_status(packet));
                    } else {
                        rfcomm_channel_id = rfcomm_event_channel_opened_get_rfcomm_cid(packet);
                        mtu = rfcomm_event_channel_opened_get_max_frame_size(packet);
                        printf("Bluetooth: RFCOMM channel open succeeded. New RFCOMM Channel ID %u, max frame size %u\n", rfcomm_channel_id, mtu);
                    }
                    break;
                case RFCOMM_EVENT_CAN_SEND_NOW:
                    rfcomm_send(rfcomm_channel_id, (uint8_t*) lineBuffer, (uint16_t) strlen(lineBuffer));
                    readyToSend = true;
                    break;

                case RFCOMM_EVENT_CHANNEL_CLOSED:
                    printf("Bluetooth: RFCOMM channel closed\n");
                    rfcomm_channel_id = 0;
                    break;
                
                default:
                    break;
            }
            break;

        case RFCOMM_DATA_PACKET:
            printf("Bluetooth: RCV: '");
            for (i=0;i<size;i++){
                putchar(packet[i]);
            }
            printf("'\n");
            break;

        default:
            break;
    }
}

// Initialise the Bluetooth stack and functionality
void btcommsInitialise(void)
{
    one_shot_timer_setup();
    spp_service_setup();

    gap_discoverable_control(1);
    gap_ssp_set_io_capability(SSP_IO_CAPABILITY_DISPLAY_YES_NO);

    // Use the following to include the HW Address in the device name
    //gap_set_local_name("VT2 00:00:00:00:00:00");
    gap_set_local_name("Valiant Turtle 2");

    // Power on the Bluetooth device
    hci_power_control(HCI_POWER_ON);
}

static btstack_timer_source_t btCliProcessTimer;
static void one_shot_timer_setup(void)
{
    // Initialise the CLI
    btCliInitialise();

    // Set one-shot timer
    btCliProcessTimer.process = &btCliProcess_handler;
    btstack_run_loop_set_timer(&btCliProcessTimer, BTCLIPROCESS_PERIOD_MS);
    btstack_run_loop_add_timer(&btCliProcessTimer);
}

// Handler for the Bluetooth CLI Process timer
static void btCliProcess_handler(struct btstack_timer_source *ts)
{
    // Ensure the RFCOMM channel is valid
    if (rfcomm_channel_id) {
        // Process the CLI state-machine
        if (readyToSend) btCliProcess();
    } else {
        // If the channel is lost; hold the CLI in reset
        btCliInitialise();
    }

    // Set up the next timer shot
    btstack_run_loop_set_timer(ts, BTCLIPROCESS_PERIOD_MS);
    btstack_run_loop_add_timer(ts);
} 

// ------------------------------------------------------------------------------------------------------------------------------------------------------------

// State Globals
btCli_state_t btCliState;

// CLI Buffer
char btCliBuffer[10];
uint16_t btCliBufferPointer;
uint16_t btCliError;

void btCliResetCommandBuffers(void)
{
    btCliBufferPointer = 0;
    btCliError = BTERR_CMD_NONE;
}

void btCliInitialise(void)
{
    btCliState = BTCLI_START;
    btCliResetCommandBuffers();
}

void btCliProcess(void)
{
    switch(btCliState) {
        case BTCLI_START:
            btCliState = btCliState_Start();
            break;

        case BTCLI_PROMPT:
            btCliState = btCliState_Prompt();
            break;

        case BTCLI_COLLECT:
            btCliState = btCliState_Collect();
            break; 

        case BTCLI_INTERPRET:
            btCliState = btCliState_Interpret();
            break; 

        case BTCLI_ERROR:
            btCliState = btCliState_Error();
            break; 
    }
}

btCli_state_t btCliState_Start(void)
{
    // Show a banner on the CLI
    snprintf(lineBuffer, sizeof(lineBuffer), "\r\nValiant Turtle 2\r\nCopyright (C)2024 Simon Inns\r\nUse HLP to show available commands\r\n");
    readyToSend = false;
    rfcomm_request_can_send_now_event(rfcomm_channel_id);

    return BTCLI_PROMPT;
}

btCli_state_t btCliState_Prompt(void)
{
    // Show the prompt
    snprintf(lineBuffer, sizeof(lineBuffer), "\r\nVT2> ");
    readyToSend = false;
    rfcomm_request_can_send_now_event(rfcomm_channel_id);

    return BTCLI_COLLECT;
}

btCli_state_t btCliState_Collect(void)
{
    // Collect any input waiting
    const int cint = getchar_timeout_us(0);

    // Was anything received?
    if ((cint < 0) || (cint > 254)) {
      // didn't get anything
      return BTCLI_COLLECT;
    }

    // Was the character a <CR>?
    if (cint == 13) {
        // Has the buffer got contents?
        if (btCliBufferPointer > 0) {
            printf("\r\n");
            return BTCLI_INTERPRET;
        } else {
            return BTCLI_PROMPT;
        }
    }

    // Was the character a <BS>?
    if (cint == 8) {
        // Backspace
        if (btCliBufferPointer > 0) {
            putchar(8);
            putchar(32);
            putchar(8);
            btCliBufferPointer--;
        }
        return BTCLI_COLLECT;
    }

    // Buffer overflow?
    if (btCliBufferPointer == 8) {
        // Ignore further input until it's a <CR> or <BS>
        return BTCLI_COLLECT;
    }

    // Not a <CR>, so add the character to our buffer
    btCliBuffer[btCliBufferPointer] = cint;
    btCliBufferPointer++;

    // Display the received character
    putchar((char)cint);

    // All good, keep collecting
    return BTCLI_COLLECT;
}

btCli_state_t btCliState_Interpret(void)
{
    // Note: All commands are cccppppp where ccc is the command and ppppp is a numerical parameter

    // Check minimum length
    if (btCliBufferPointer < 3) {
        btCliError = BTERR_CMD_SHORT;
        return BTCLI_ERROR;
    }

    // Get the command (3 characters)
    char command[4];
    char parameter[6];
    uint16_t pointer = 0;

    for (pointer = 0; pointer < 3; pointer++) {
        command[pointer] = btCliBuffer[pointer];
    }
    command[pointer] = '\0'; // Terminate

    // Get the parameter (5 characters)
    for (pointer = 0; pointer < btCliBufferPointer-3; pointer++) {
        parameter[pointer] = btCliBuffer[pointer+3];
    }
    parameter[pointer] = '\0'; // Terminate

    // Convert command to uppercase
    btConvUppercase(command);

    // Convert parameter to integer
    uint16_t nparam = atoi(parameter);

    // Process the command
    if (commandProcess(command, nparam) != 0) {
        btCliError = BTERR_CMD_UNKNOWN;
        return BTCLI_ERROR;
    }

    // Empty the buffer and return to the prompting state
    btCliResetCommandBuffers();
    return BTCLI_PROMPT;
}

btCli_state_t btCliState_Error(void)
{
    switch(btCliError) {
        case BTERR_CMD_NONE:
            snprintf(lineBuffer, sizeof(lineBuffer), "E00 - OK\r\n");
            
            break;

        case BTERR_CMD_SHORT:
            snprintf(lineBuffer, sizeof(lineBuffer), "E01 - Command too short\r\n");
            break;

        case BTERR_CMD_UNKNOWN:
            snprintf(lineBuffer, sizeof(lineBuffer), "E02 - Unknown command\r\n");
            break;

        case BTERR_CMD_PARAMISSING:
            snprintf(lineBuffer, sizeof(lineBuffer), "E03 - Parameter missing\r\n");
            break;
    }
    rfcomm_request_can_send_now_event(rfcomm_channel_id);

    // Empty the buffer and return to the prompting state
    btCliResetCommandBuffers();
    return BTCLI_PROMPT;
}

// Convert a string to uppercase
void btConvUppercase(char *temp)
{
    char * name;
    name = strtok(temp,":");

    // Convert to upper case
    char *s = name;
    while (*s) {
        *s = toupper((unsigned char) *s);
        s++;
    }
}