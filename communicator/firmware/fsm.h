/************************************************************************ 

    fsm.h

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

#ifndef FSM_H_
#define FSM_H_

// Enum of possible states
// ENUM indication which stepper is required
typedef enum {
    fsm_state_byte_mode,
    fsm_state_command_mode,
    fsm_state_switch_from_byte_mode,
    fsm_state_switch_from_command_mode,
    fsm_state_forward_command,
    fsm_state_backward_command,
    fsm_state_left_command,
    fsm_state_right_command,
    fsm_state_scale_command,
    fsm_state_error
} fsm_states_t;

void fsm_initialise(void);
void fsm_process(uint8_t incoming_byte);
fsm_states_t fsm_byte_mode(uint8_t incoming_byte);
fsm_states_t fsm_command_mode(uint8_t incoming_byte);
fsm_states_t fsm_forward_command(uint8_t incoming_byte);
fsm_states_t fsm_backward_command(uint8_t incoming_byte);
fsm_states_t fsm_left_command(uint8_t incoming_byte);
fsm_states_t fsm_right_command(uint8_t incoming_byte);
fsm_states_t fsm_scale_command(uint8_t incoming_byte);

#endif /* FSM_H_ */