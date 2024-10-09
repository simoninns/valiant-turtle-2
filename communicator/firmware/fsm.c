/************************************************************************ 

    fsm.c

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

#include "debug.h"
#include "fsm.h"
#include "ir.h"

// Global for storing current state
fsm_states_t fsm_current_state;
fsm_states_t fsm_next_state;

// Initialise the Communicator Finite State Machine
void fsm_initialise()
{
    // Initialise state
    fsm_current_state = fsm_state_byte_mode;
    fsm_next_state = fsm_current_state;
}

void fsm_process(uint8_t incoming_byte)
{
    fsm_current_state = fsm_next_state;
    debug_printf("fsm_process(): Received 0x%02x\n", incoming_byte);

    switch (fsm_current_state) {
        case fsm_state_byte_mode:
            fsm_next_state = fsm_byte_mode(incoming_byte);
        break;

        default:
            debug_printf("fsm_process(): Unknown state!\n");
            fsm_next_state = fsm_state_byte_mode;
    }
}

// Byte mode state
fsm_states_t fsm_byte_mode(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;

    switch (incoming_byte) {
        case 0xFD:
            // Got the first byte of 'switch to command mode'
            return_state = fsm_state_switch_from_byte_mode;
            break;

        case 0x0D:
            // Got the initialisation command
            debug_printf("fsm_byte_mode(): Received INITIALIZE command.\n");
            return_state = fsm_state_byte_mode;
            break;

        default:
            // This is a standard byte command - interpret it
            debug_printf("fsm_byte_mode(): Byte command = 0x%02x\n", incoming_byte);

            uint8_t a = (incoming_byte & 0x80) >> 7;    // 0b 1000 0000
            uint8_t mm = (incoming_byte & 0x60) >> 5;   // 0b 0110 0000
            uint8_t p = (incoming_byte & 0x10) >> 4;    // 0b 0001 0000

            uint8_t ll = (incoming_byte & 0x0C) >> 2;    // 0b 0000 1100
            uint8_t rr = (incoming_byte & 0x03) >> 0;    // 0b 0000 0011

            debug_printf("fsm_byte_mode(): Command is:\n");

            if (mm == 0) debug_printf("  Step sequence 00 - Deactivate motor\n");
            else if (mm == 1) debug_printf("  Step sequence 01 - NO IDEA?\n");
            else if (mm == 2) debug_printf("  Step sequence 10 - Activate motor\n");
            else if (mm == 3) debug_printf("  Step sequence 11 - Step motor\n");
            else debug_printf("  Motor sequence ERROR\n");

            if (p == 0) debug_printf("  Pen down\n");
            else debug_printf("  Pen up\n");

            if (ll == 0) debug_printf("  Left motor off\n");
            else if (ll == 1) debug_printf("  Left motor forwards\n");
            else if (ll == 2) debug_printf("  Left motor backwards\n");
            else if (ll == 3) debug_printf("  Left motor on\n");

            if (rr == 0) debug_printf("  Right motor off\n");
            else if (rr == 1) debug_printf("  Right motor backwards\n");
            else if (rr == 2) debug_printf("  Right motor forwards\n");
            else if (rr == 3) debug_printf("  Right motor on\n");

            // Transmit the command to the robot
            // Note: we should probably toggle CTS/RTS or something when processing a byte?
            ir_send_byte(incoming_byte);

            // Stay in byte mode
            return_state = fsm_state_byte_mode;
    }

    // Return the next state
    return return_state;
}

// Command mode state
// Note: Command mode is not supported by the original communicator
// it is an addition by the following project:
// https://eccentriccreations.co.uk/valiant_turtle_reproduction_communicator.php
fsm_states_t fsm_command_mode(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;
    debug_printf("fsm_command_mode(): Received 0x%02x\n", incoming_byte);

    switch (incoming_byte) {
        case 0xFB:
            // Got the first byte of 'switch to byte mode'
            return_state = fsm_state_switch_from_command_mode;
            break;

        case 0x06:
            // Forward command
            return_state = fsm_state_forward_command;
            break;

        case 0x09:
            // Backward command
            return_state = fsm_state_backward_command;
            break;

        case 0x05:
            // Left command
            return_state = fsm_state_left_command;
            break;

        case 0x0A:
            // Right command
            return_state = fsm_state_right_command;
            break;

        case 0x20:
            // Pen up command
            debug_printf("fsm_command_mode(): Received PEN UP command\n"); 
            return_state = fsm_state_command_mode;
            break;

        case 0x10:
            // Pen down command
            debug_printf("fsm_command_mode(): Received PEN DOWN command\n");
            return_state = fsm_state_command_mode;
            break;

        case 0xFC:
            // Adjust scale command
            return_state = fsm_state_scale_command;
            break;

        case 0x0D:
            // Got the initialisation command
            debug_printf("fsm_command_mode(): Received INITIALIZE command - returning to byte mode\n");
            return_state = fsm_state_byte_mode;
            break;

        default:
            debug_printf("fsm_command_mode(): Incoming byte not handled! Byte = 0x%02x\n", incoming_byte);
    }

    // Return the next state
    return return_state;
}

// Switch from byte mode state
fsm_states_t fsm_switch_from_byte_mode(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;

    // Check that we received another 0xFD to switch to command mode
    // If not, stay in byte mode
    if (incoming_byte == 0xFD) {
        return_state = fsm_state_command_mode;
        debug_printf("fsm_switch_from_byte_mode(): Received Switch to command mode command\n");
    } else return_state = fsm_state_byte_mode;

    // Return the next state
    return return_state;
}

// Switch from command mode state
fsm_states_t fsm_switch_from_command_mode(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;

    // Check that we received another 0xFD to switch to byte mode
    // If not, stay in command mode
    if (incoming_byte == 0xFB) {
        return_state = fsm_state_byte_mode;
        debug_printf("fsm_switch_from_command_mode(): Received Switch to byte mode command\n");
    } else return_state = fsm_state_command_mode;

    // Return the next state
    return return_state;
}

fsm_states_t fsm_forward_command(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;

    debug_printf("fsm_forward_command(): Received FORWARD 0x%02x command\n", incoming_byte); 
    return_state = fsm_state_command_mode;

    // Return the next state
    return return_state;
}

fsm_states_t fsm_backward_command(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;

    debug_printf("fsm_backward_command(): Received BACKWARD 0x%02x command\n", incoming_byte); 
    return_state = fsm_state_command_mode;

    // Return the next state
    return return_state;
}

fsm_states_t fsm_left_command(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;

    debug_printf("fsm_left_command(): Received LEFT 0x%02x command\n", incoming_byte); 
    return_state = fsm_state_command_mode;

    // Return the next state
    return return_state;
}

fsm_states_t fsm_right_command(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;

    debug_printf("fsm_right_command(): Received RIGHT 0x%02x command\n", incoming_byte); 
    return_state = fsm_state_command_mode;

    // Return the next state
    return return_state;
}

fsm_states_t fsm_scale_command(uint8_t incoming_byte)
{
    fsm_states_t return_state = fsm_state_error;

    debug_printf("fsm_scale_command(): Received SCALE 0x%02x command\n", incoming_byte); 
    return_state = fsm_state_command_mode;

    // Return the next state
    return return_state;
}