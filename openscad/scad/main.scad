/************************************************************************

    main.scad
    
    Valiant Turtle 2
    Copyright (C) 2024 Simon Inns
    
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
include <shell.scad>
include <motor_bay.scad>
include <motor_mounts.scad>
include <wheels.scad>
include <pcb.scad>
include <leds.scad>
include <head_cover.scad>
include <pen_holder_base.scad>
include <pen_holder_top.scad>
include <servo.scad>
include <servo_holder.scad>
include <battery.scad>
include <pen_holder_cap.scad>
include <logotype.scad>
include <toggle_switch.scad>
include <display_mount.scad>

// // Viewport translation
// $vpt = [0, 0, 0];
// // Viewport rotation
// $vpr = [55, 360 * $t, 360 * $t];
// // Viewport distance
// $vpd = 950;

/* [Rendering Parameters] */
for_printing = "Display"; // [Display, Printing]
pen_up = "Pen Up"; // [False, True]

/* [Printable Parts] */
display_body_left = "Yes"; // [Yes, No]
display_body_right = "Yes"; // [Yes, No]
display_head = "Yes"; // [Yes, No]
display_head_cover = "No"; // [Yes, No]
display_shell_lid = "No"; // [Yes, No]
display_shell = "No"; // [Yes, No]
display_shell_dot = "No"; // [Yes, No]
display_motor_bay = "Yes"; // [Yes, No]
display_motor_mounts = "No"; // [Yes, No]
display_wheels = "No"; // [Yes, No]
display_pcb_mounts_front = "No"; // [Yes, No]
display_pcb_mounts_back = "No"; // [Yes, No]
display_pen_holder_base = "No"; // [Yes, No]
display_pen_holder_top_small = "No"; // [Yes, No]
display_pen_holder_top_medium = "No"; // [Yes, No]
display_pen_holder_top_large = "No"; // [Yes, No]
display_pen_holder_cap = "No"; // [Yes, No]
display_servo_holder = "No"; // [Yes, No]
display_servo_horn = "No"; // [Yes, No]
display_logotype = "No"; // [Yes, No]
display_battery_holder = "No"; // [Yes, No]
display_battery_cover = "No"; // [Yes, No]
display_led_holders = "No"; // [Yes, No]
display_display_mount = "No"; // [Yes, No]

/* [Print Supports] */
display_shell_support = "No"; // [Yes, No]

/* [Non-Printable Parts] */
display_motor_small = "No"; // [Yes, No]
display_motor_large = "No"; // [Yes, No]
display_rotational_axis = "No"; // [Yes, No]
display_turning_circle = "No"; // [Yes, No]
display_tires = "No"; // [Yes, No]
display_pcb = "No"; // [Yes, No]
display_leds = "No"; // [Yes, No]
display_ball_bearing = "No"; // [Yes, No]
display_pen = "No"; // [Yes, No]
display_servo = "No"; // [Yes, No]
display_battery = "No"; // [Yes, No]
display_toggle_switch = "No"; // [Yes, No]

/* [Screws] */
display_motor_mounts_screws = "No"; // [Yes, No]
display_body_left_screws = "No"; // [Yes, No]
display_body_right_screws = "No"; // [Yes, No]
display_motor_bay_screws = "No"; // [Yes, No]
display_head_screws = "No"; // [Yes, No]
display_servo_holder_screws = "No"; // [Yes, No]
display_pcb_mounts_front_screws = "No"; // [Yes, No]
display_pcb_mounts_back_screws = "No"; // [Yes, No]
display_shell_screws = "No"; // [Yes, No]
display_battery_screws = "No"; // [Yes, No]

module main() {
    toPrint = (for_printing == "Printing") ? true:false;
    penUp = (pen_up == "True") ? true:false;

    d_body_left = (display_body_left == "Yes") ? true:false;
    d_body_right = (display_body_right == "Yes") ? true:false;
    d_head = (display_head == "Yes") ? true:false;
    d_shell_lid = (display_shell_lid == "Yes") ? true:false;
    d_shell = (display_shell == "Yes") ? true:false;
    d_shell_dot = (display_shell_dot == "Yes") ? true:false;
    d_motor_bay = (display_motor_bay == "Yes") ? true:false;
    d_motor_mounts = (display_motor_mounts == "Yes") ? true:false;
    d_wheels = (display_wheels == "Yes") ? true:false;
    d_pcb_mounts_front = (display_pcb_mounts_front == "Yes") ? true:false;
    d_pcb_mounts_back = (display_pcb_mounts_back == "Yes") ? true:false;
    d_head_cover = (display_head_cover == "Yes") ? true:false;
    d_pen_holder_base = (display_pen_holder_base == "Yes") ? true:false;
    d_pen_holder_top_small = (display_pen_holder_top_small == "Yes") ? true:false;
    d_pen_holder_top_medium = (display_pen_holder_top_medium == "Yes") ? true:false;
    d_pen_holder_top_large = (display_pen_holder_top_large == "Yes") ? true:false;
    d_pen_holder_cap = (display_pen_holder_cap == "Yes") ? true:false;
    d_servo_holder = (display_servo_holder == "Yes") ? true:false;
    d_servo_horn = (display_servo_horn == "Yes") ? true:false;
    d_logotype = (display_logotype == "Yes") ? true:false;
    d_battery_holder = (display_battery_holder == "Yes") ? true:false;
    d_battery_cover = (display_battery_cover == "Yes") ? true:false;
    d_led_holders = (display_led_holders == "Yes") ? true:false;
    d_display_mount = (display_display_mount == "Yes") ? true:false;

    // Print supports
    d_shell_support = (display_shell_support == "Yes") ? true:false;

    // Non-printable parts
    d_motor_small = (display_motor_small == "Yes") ? true:false;
    d_motor_large = (display_motor_large == "Yes") ? true:false;
    d_rotational_axis = (display_rotational_axis == "Yes") ? true:false;
    d_turning_circle = (display_turning_circle == "Yes") ? true:false;
    d_tires = (display_tires == "Yes") ? true:false;
    d_pcb = (display_pcb == "Yes") ? true:false;
    d_leds = (display_leds == "Yes") ? true:false;
    d_ball_bearing = (display_ball_bearing == "Yes") ? true:false;
    d_pen = (display_pen == "Yes") ? true:false;
    d_servo = (display_servo == "Yes") ? true:false;
    d_battery = (display_battery == "Yes") ? true:false;
    d_toggle_switch = (display_toggle_switch == "Yes") ? true:false;

    // Screws
    d_motor_mounts_screws = (display_motor_mounts_screws == "Yes") ? true:false;
    d_body_left_screws = (display_body_left_screws == "Yes") ? true:false;
    d_body_right_screws = (display_body_right_screws == "Yes") ? true:false;
    d_motor_bay_screws = (display_motor_bay_screws == "Yes") ? true:false;
    d_head_screws = (display_head_screws == "Yes") ? true:false;
    d_servo_holder_screws = (display_servo_holder_screws == "Yes") ? true:false;
    d_pcb_mounts_front_screws = (display_pcb_mounts_front_screws == "Yes") ? true:false;
    d_pcb_mounts_back_screws = (display_pcb_mounts_back_screws == "Yes") ? true:false;
    d_shell_screws = (display_shell_screws == "Yes") ? true:false;
    d_battery_screws = (display_battery_screws == "Yes") ? true:false;

    // Render the printable parts
    if (d_body_left) render_body_left(toPrint);
    if (d_body_right) render_body_right(toPrint);
    if (d_head) render_head(toPrint);
    if (d_shell_lid) render_shell_lid(toPrint);
    if (d_shell) render_shell(toPrint);
    if (d_shell_dot) render_shell_dot(toPrint);
    if (d_motor_bay) render_motor_bay(toPrint);
    if (d_motor_mounts) render_motor_mounts(toPrint);
    if (d_wheels) render_wheels(toPrint);
    if (d_pcb_mounts_front) render_pcb_mounts_front(toPrint);
    if (d_pcb_mounts_back) render_pcb_mounts_back(toPrint);
    if (d_head_cover) render_head_cover(toPrint);
    if (d_pen_holder_base) render_pen_holder_base(toPrint, penUp);
    if (d_pen_holder_top_small) render_pen_holder_top_small(toPrint, penUp);
    if (d_pen_holder_top_medium) render_pen_holder_top_medium(toPrint, penUp);
    if (d_pen_holder_top_large) render_pen_holder_top_large(toPrint, penUp);
    if (d_pen_holder_cap) render_pen_holder_cap(toPrint,penUp);
    if (d_servo_holder) render_servo_holder(toPrint);
    if (d_servo_horn) render_micro_servo_horn(toPrint, penUp);
    if (d_logotype) render_logotype(toPrint);
    if (d_battery_holder) render_battery_holder(toPrint);
    if (d_battery_cover) render_battery_cover(toPrint);
    if (d_led_holders) render_led_holders(toPrint);
    if (d_display_mount) render_display_mount(toPrint);

    // Render the print supports
    if (d_shell_support) render_shell_support(toPrint);

    // Render the non-printable parts
    if (d_motor_small) render_motor_small(toPrint);
    if (d_motor_large) render_motor_large(toPrint);
    if (d_rotational_axis) render_rotational_axis(toPrint);
    if (d_turning_circle) render_turning_circle(toPrint);
    if (d_tires) render_tires(toPrint);
    if (d_pcb) render_pcb(toPrint);
    if (d_leds) render_leds(toPrint);
    if (d_ball_bearing) render_ball_bearing(toPrint);
    if (d_pen) render_pen(toPrint, penUp);
    if (d_servo) render_micro_servo(toPrint);
    if (d_battery) render_battery(toPrint);
    if (d_toggle_switch) render_toggle_switch(toPrint);

    // Render screws
    if (d_motor_mounts_screws) render_motor_mounts_screws(toPrint);
    if (d_body_left_screws) render_body_left_screws(toPrint);
    if (d_body_right_screws) render_body_right_screws(toPrint);
    if (d_motor_bay_screws) render_motor_bay_screws(toPrint);
    if (d_head_screws) render_head_screws(toPrint);
    if (d_servo_holder_screws) render_servo_holder_screws(toPrint);
    if (d_pcb_mounts_front_screws) render_pcb_mounts_front_screws(toPrint);
    if (d_pcb_mounts_back_screws) render_pcb_mounts_back_screws(toPrint);
    if (d_shell_screws) render_shell_screws(toPrint);
    if (d_battery_screws) render_battery_screws(toPrint);
}

// Set the arc resolution higher when in printing mode
if (for_printing == "Printing") {
    $fn=50;
    main();
} else {
    $fn=20;
    // Place the centre of the axis on the centre rotation point of the model
    //move([0,-29,6]) main();
    main();
}