/************************************************************************

    main.scad
    
    Valiant Turtle 2
    Copyright (C) 2023 Simon Inns
    
    This is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    Email: simon.inns@gmail.com
    
************************************************************************/

include <BOSL/constants.scad>
use <BOSL/transforms.scad>
use <BOSL/shapes.scad>

// Local includes
include <body.scad>
include <head.scad>
include <shell_top.scad>
include <shell_bottom.scad>
include <motor_bay.scad>
include <motor_mounts.scad>
include <wheels.scad>
include <pcb.scad>
include <leds.scad>
include <head_cover.scad>

// Rendering resolution
//
$fn=50;

// Select rendering parameters
//
use_colour = "Colour"; // [Colour, No colour]
for_printing = "Display"; // [Display, Printing]

display_body = "Yes"; // [Yes, No]
display_head = "Yes"; // [Yes, No]
display_shell_top = "Yes"; // [Yes, No]
display_shell_bottom = "Yes"; // [Yes, No]
display_motor_bay = "Yes"; // [Yes, No]
display_motor_mounts = "Yes"; // [Yes, No]
display_wheels = "Yes"; // [Yes, No]
display_pcb_mounts = "Yes"; // [Yes, No]
display_head_cover = "Yes"; // [Yes, No]
display_caster_ball_base = "Yes"; // [Yes, No]

// Non-printable parts
//
display_motor = "Yes"; // [Yes, No]
display_rotational_axis = "Yes"; // [Yes, No]
display_turning_circle = "Yes"; // [Yes, No]
display_tires = "Yes"; // [Yes, No]
display_pcb = "Yes"; // [Yes, No]
display_leds = "Yes"; // [Yes, No]

module main() {
    crend = (use_colour == "Colour") ? true:false;
    toPrint = (for_printing == "Printing") ? true:false;

    d_body = (display_body == "Yes") ? true:false;
    d_head = (display_head == "Yes") ? true:false;
    d_shell_top = (display_shell_top == "Yes") ? true:false;
    d_shell_bottom = (display_shell_bottom == "Yes") ? true:false;
    d_motor_bay = (display_motor_bay == "Yes") ? true:false;
    d_motor_mounts = (display_motor_mounts == "Yes") ? true:false;
    d_wheels = (display_wheels == "Yes") ? true:false;
    d_pcb_mounts = (display_pcb_mounts == "Yes") ? true:false;
    d_head_cover = (display_head_cover == "Yes") ? true:false;
    d_caster_ball_base = (display_caster_ball_base == "Yes") ? true:false;

    // Non-printable parts
    d_motor = (display_motor == "Yes") ? true:false;
    d_rotational_axis = (display_rotational_axis == "Yes") ? true:false;
    d_turning_circle = (display_turning_circle == "Yes") ? true:false;
    d_tires = (display_tires == "Yes") ? true:false;
    d_pcb = (display_pcb == "Yes") ? true:false;
    d_leds = (display_leds == "Yes") ? true:false;

    // Render the printable parts
    if (d_body) render_body(crend, toPrint);
    if (d_head) render_head(crend, toPrint);
    if (d_shell_top) render_shell_top(crend, toPrint);
    if (d_shell_bottom) render_shell_bottom(crend, toPrint);
    if (d_motor_bay) render_motor_bay(crend, toPrint);
    if (d_motor_mounts) render_motor_mounts(crend, toPrint);
    if (d_wheels) render_wheels(crend, toPrint);
    if (d_pcb_mounts) render_pcb_mounts(crend, toPrint);
    if (d_head_cover) render_head_cover(crend, toPrint);
    if (d_caster_ball_base) render_caster_ball_base(crend, toPrint);

    // Render the non-printable parts
    if (d_motor) render_motor(crend, toPrint);
    if (d_rotational_axis) render_rotational_axis(crend, toPrint);
    if (d_turning_circle) render_turning_circle(crend, toPrint);
    if (d_tires) render_tires(crend, toPrint);
    if (d_pcb) render_pcb(crend, toPrint);
    if (d_leds) render_leds(crend, toPrint);
}

main();