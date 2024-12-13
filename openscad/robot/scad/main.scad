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
include <main_pcb.scad>
include <aux_pcb.scad>
include <eyes.scad>
include <head_cover.scad>
include <pen_holder_base.scad>
include <pen_holder_top.scad>
include <servo.scad>
include <servo_holder.scad>
include <battery.scad>
include <battery_clip.scad>
include <pen_holder_cap.scad>
include <logotype.scad>
include <toggle_switch.scad>
include <stand.scad>

// // Viewport translation
// $vpt = [0, 0, 0];
// // Viewport rotation
// $vpr = [55, 360 * $t, 360 * $t];
// // Viewport distance
// $vpd = 950;

// Note: Default display must be "No" otherwise STL generation script will fail

/* [Rendering Parameters] */
// Select Display for viewing the model or Printing to orientate parts for STL generation
for_printing = "Display"; // [Display, Printing]
// Display with pen up or down
pen_up = "Up"; // [Up, Down]
// Origin on model or pen
origin_position = "Model"; // [Pen, Model]

/* [Printable Parts] */
display_body_left = "No"; // [Yes, No]
display_body_right = "No"; // [Yes, No]
display_head = "No"; // [Yes, No]
display_head_cover = "No"; // [Yes, No]
display_shell = "No"; // [Yes, No]
display_motor_bay_left = "No"; // [Yes, No]
display_motor_bay_right = "No"; // [Yes, No]
display_motor_mount_left = "No"; // [Yes, No]
display_motor_mount_right = "No"; // [Yes, No]
display_wheel_left = "No"; // [Yes, No]
display_wheel_right = "No"; // [Yes, No]
display_main_pcb_mounts_front = "No"; // [Yes, No]
display_main_pcb_mounts_back = "No"; // [Yes, No]
display_main_pcb_screw_washer = "No"; // [Yes, No]
display_pen_holder_base = "No"; // [Yes, No]
display_pen_holder_top_small = "No"; // [Yes, No]
display_pen_holder_top_medium = "No"; // [Yes, No]
display_pen_holder_top_large = "No"; // [Yes, No]
display_pen_holder_cap = "No"; // [Yes, No]
display_servo_holder = "No"; // [Yes, No]
display_servo_horn = "No"; // [Yes, No]
display_male_connector_back = "No"; // [Yes, No]
display_male_connector_front = "No"; // [Yes, No]
display_logotype = "No"; // [Yes, No]
display_battery_pack = "No"; // [Yes, No]
display_battery_pack_upper_cover = "No"; // [Yes, No]
display_battery_pack_lower_cover = "No"; // [Yes, No]
display_battery_pack_connector_cover = "No"; // [Yes, No]
display_battery_pack_connector_lock = "No"; // [Yes, No]
display_battery_pack_bms_bracket = "No"; // [Yes, No]
display_battery_clip = "No"; // [Yes, No]
display_eye_surround = "No"; // [Yes, No]
display_eye_light_pipe = "No"; // [Yes, No]
display_stand = "No"; // [Yes, No]
display_stand_lower_cover = "No"; // [Yes, No]
display_stand_upper_cover = "No"; // [Yes, No]
display_eye_pcb_jig = "No"; // [Yes, No]
display_aux_pcb_mount = "No"; // [Yes, No]
display_aux_pcb_screw_washer = "No"; // [Yes, No]
display_shell2 = "No"; // [Yes, No]

/* [Support Enforcers] */
display_shell_supports = "No"; // [Yes, No]
display_battery_pack_supports = "No"; // [Yes, No]
display_battery_pack_lower_cover_supports = "No"; // [Yes, No]
display_battery_pack_upper_cover_supports = "No"; // [Yes, No]
display_body_left_supports = "No"; // [Yes, No]
display_body_right_supports = "No"; // [Yes, No]
display_stand_lower_cover_supports = "No"; // [Yes, No]
display_stand_upper_cover_supports = "No"; // [Yes, No]

/* [Non-Printable Parts] */
display_motor_left = "No"; // [Yes, No]
display_motor_right = "No"; // [Yes, No]
display_rotational_axis = "No"; // [Yes, No]
display_turning_circle = "No"; // [Yes, No]
display_tire_left = "No"; // [Yes, No]
display_tire_right = "No"; // [Yes, No]
display_main_pcb = "No"; // [Yes, No]
display_aux_pcb = "No"; // [Yes, No]
display_eye_pcb = "No"; // [Yes, No]
display_ball_bearing = "No"; // [Yes, No]
display_pen = "No"; // [Yes, No]
display_servo = "No"; // [Yes, No]
display_batteries = "No"; // [Yes, No]
display_battery_pack_bms_pcb = "No"; // [Yes, No]
display_toggle_switch = "No"; // [Yes, No]
display_logotype_2D = "No"; // [Yes, No]
display_battery_clip_contacts = "No"; // [Yes, No]
display_male_bullet_connectors = "No"; // [Yes, No]
display_female_bullet_connectors = "No"; // [Yes, No]

/* [Screws] */
display_motor_mount_screws_left = "No"; // [Yes, No]
display_motor_mount_screws_right = "No"; // [Yes, No]
display_body_left_screws = "No"; // [Yes, No]
display_body_right_screws = "No"; // [Yes, No]
display_motor_bay_screws_left = "No"; // [Yes, No]
display_motor_bay_screws_right = "No"; // [Yes, No]
display_head_screws = "No"; // [Yes, No]
display_servo_holder_screws = "No"; // [Yes, No]
display_main_pcb_mounts_front_screws = "No"; // [Yes, No]
display_main_pcb_mounts_back_screws = "No"; // [Yes, No]
display_shell_screws = "No"; // [Yes, No]
display_battery_screws = "No"; // [Yes, No]
display_aux_pcb_screws = "No"; // [Yes, No]

module main() {
    // Rendering parameters
    toPrint = (for_printing == "Printing") ? true:false;
    penUp = (pen_up == "Up") ? true:false;

    // Set the origin
    originX = (origin_position == "Pen") ? 0:0;
    originY = (origin_position == "Pen") ? -29:0;
    originZ = (origin_position == "Pen") ? 6:0;

    // Printable parts
    d_body_left = (display_body_left == "Yes") ? true:false;
    d_body_right = (display_body_right == "Yes") ? true:false;
    d_head = (display_head == "Yes") ? true:false;
    d_shell = (display_shell == "Yes") ? true:false;
    d_motor_bay_left = (display_motor_bay_left == "Yes") ? true:false;
    d_motor_bay_right = (display_motor_bay_right == "Yes") ? true:false;
    d_motor_mount_left = (display_motor_mount_left == "Yes") ? true:false;
    d_motor_mount_right = (display_motor_mount_right == "Yes") ? true:false;
    d_wheel_left = (display_wheel_left == "Yes") ? true:false;
    d_wheel_right = (display_wheel_right == "Yes") ? true:false;
    d_main_pcb_mounts_front = (display_main_pcb_mounts_front == "Yes") ? true:false;
    d_main_pcb_mounts_back = (display_main_pcb_mounts_back == "Yes") ? true:false;
    d_main_pcb_screw_washer = (display_main_pcb_screw_washer == "Yes") ? true:false;
    d_head_cover = (display_head_cover == "Yes") ? true:false;
    d_pen_holder_base = (display_pen_holder_base == "Yes") ? true:false;
    d_pen_holder_top_small = (display_pen_holder_top_small == "Yes") ? true:false;
    d_pen_holder_top_medium = (display_pen_holder_top_medium == "Yes") ? true:false;
    d_pen_holder_top_large = (display_pen_holder_top_large == "Yes") ? true:false;
    d_pen_holder_cap = (display_pen_holder_cap == "Yes") ? true:false;
    d_servo_holder = (display_servo_holder == "Yes") ? true:false;
    d_servo_horn = (display_servo_horn == "Yes") ? true:false;
    d_male_connector_back = (display_male_connector_back == "Yes") ? true:false;
    d_male_connector_front = (display_male_connector_front == "Yes") ? true:false;
    d_logotype = (display_logotype == "Yes") ? true:false;
    d_battery_pack = (display_battery_pack == "Yes") ? true:false;
    d_battery_pack_upper_cover = (display_battery_pack_upper_cover == "Yes") ? true:false;
    d_battery_pack_lower_cover = (display_battery_pack_lower_cover == "Yes") ? true:false;
    d_battery_pack_connector_cover = (display_battery_pack_connector_cover == "Yes") ? true:false;
    d_battery_pack_connector_lock = (display_battery_pack_connector_lock == "Yes") ? true:false;
    d_battery_pack_bms_bracket = (display_battery_pack_bms_bracket == "Yes") ? true:false;
    d_battery_clip = (display_battery_clip == "Yes") ? true:false;
    d_eye_surround = (display_eye_surround == "Yes") ? true:false;
    d_eye_light_pipe = (display_eye_light_pipe == "Yes") ? true:false;
    d_stand = (display_stand == "Yes") ? true:false;
    d_stand_lower_cover = (display_stand_lower_cover == "Yes") ? true:false;
    d_stand_upper_cover = (display_stand_upper_cover == "Yes") ? true:false;
    d_eye_pcb_jig = (display_eye_pcb_jig == "Yes") ? true:false;
    d_aux_pcb_mount = (display_aux_pcb_mount == "Yes") ? true:false;
    d_aux_pcb_screw_washer = (display_aux_pcb_screw_washer == "Yes") ? true:false;
    d_shell2 = (display_shell2 == "Yes") ? true:false;

    // Support enforcers
    d_shell_supports = (display_shell_supports == "Yes") ? true:false;
    d_battery_pack_supports = (display_battery_pack_supports == "Yes") ? true:false;
    d_battery_pack_lower_cover_supports = (display_battery_pack_lower_cover_supports == "Yes") ? true:false;
    d_battery_pack_upper_cover_supports = (display_battery_pack_upper_cover_supports == "Yes") ? true:false;
    d_body_left_supports = (display_body_left_supports == "Yes") ? true:false;
    d_body_right_supports = (display_body_right_supports == "Yes") ? true:false;
    d_stand_lower_cover_supports = (display_stand_lower_cover_supports == "Yes") ? true:false;
    d_stand_upper_cover_supports = (display_stand_upper_cover_supports == "Yes") ? true:false;

    // Non-printable parts
    d_motor_left = (display_motor_left == "Yes") ? true:false;
    d_motor_right = (display_motor_right == "Yes") ? true:false;
    d_rotational_axis = (display_rotational_axis == "Yes") ? true:false;
    d_turning_circle = (display_turning_circle == "Yes") ? true:false;
    d_tire_left = (display_tire_left == "Yes") ? true:false;
    d_tire_right = (display_tire_right == "Yes") ? true:false;
    d_main_pcb = (display_main_pcb == "Yes") ? true:false;
    d_aux_pcb = (display_aux_pcb == "Yes") ? true:false;
    d_eye_pcb = (display_eye_pcb == "Yes") ? true:false;
    d_ball_bearing = (display_ball_bearing == "Yes") ? true:false;
    d_pen = (display_pen == "Yes") ? true:false;
    d_servo = (display_servo == "Yes") ? true:false;
    d_batteries = (display_batteries == "Yes") ? true:false;
    d_battery_pack_bms_pcb = (display_battery_pack_bms_pcb == "Yes") ? true:false;
    d_toggle_switch = (display_toggle_switch == "Yes") ? true:false;
    d_logotype_2D = (display_logotype_2D == "Yes") ? true:false;
    d_battery_clip_contacts = (display_battery_clip_contacts == "Yes") ? true:false;
    d_male_bullet_connectors = (display_male_bullet_connectors == "Yes") ? true:false;
    d_female_bullet_connectors = (display_female_bullet_connectors == "Yes") ? true:false;

    // Screws
    d_motor_mount_screws_left = (display_motor_mount_screws_left == "Yes") ? true:false;
    d_motor_mount_screws_right = (display_motor_mount_screws_right == "Yes") ? true:false;
    d_body_left_screws = (display_body_left_screws == "Yes") ? true:false;
    d_body_right_screws = (display_body_right_screws == "Yes") ? true:false;
    d_motor_bay_screws_left = (display_motor_bay_screws_left == "Yes") ? true:false;
    d_motor_bay_screws_right = (display_motor_bay_screws_right == "Yes") ? true:false;
    d_head_screws = (display_head_screws == "Yes") ? true:false;
    d_servo_holder_screws = (display_servo_holder_screws == "Yes") ? true:false;
    d_main_pcb_mounts_front_screws = (display_main_pcb_mounts_front_screws == "Yes") ? true:false;
    d_main_pcb_mounts_back_screws = (display_main_pcb_mounts_back_screws == "Yes") ? true:false;
    d_shell_screws = (display_shell_screws == "Yes") ? true:false;
    d_battery_screws = (display_battery_screws == "Yes") ? true:false;
    d_aux_pcb_screws = (display_aux_pcb_screws == "Yes") ? true:false;

    move([originX,originY,originZ]) {
        // Render the printable parts
        if (d_body_left) render_body_left(toPrint);
        if (d_body_right) render_body_right(toPrint);
        if (d_head) render_head(toPrint);
        if (d_shell) render_shell(toPrint);
        if (d_motor_bay_left) render_motor_bay_left(toPrint);
        if (d_motor_bay_right) render_motor_bay_right(toPrint);
        if (d_motor_mount_left) render_motor_mount_left(toPrint);
        if (d_motor_mount_right) render_motor_mount_right(toPrint);
        if (d_wheel_left) render_wheel_left(toPrint);
        if (d_wheel_right) render_wheel_right(toPrint);
        if (d_main_pcb_mounts_front) render_main_pcb_mounts_front(toPrint);
        if (d_main_pcb_mounts_back) render_main_pcb_mounts_back(toPrint);
        if (d_main_pcb_screw_washer) render_main_pcb_screw_washer(toPrint);
        if (d_head_cover) render_head_cover(toPrint);
        if (d_pen_holder_base) render_pen_holder_base(toPrint, penUp);
        if (d_pen_holder_top_small) render_pen_holder_top_small(toPrint, penUp);
        if (d_pen_holder_top_medium) render_pen_holder_top_medium(toPrint, penUp);
        if (d_pen_holder_top_large) render_pen_holder_top_large(toPrint, penUp);
        if (d_pen_holder_cap) render_pen_holder_cap(toPrint,penUp);
        if (d_servo_holder) render_servo_holder(toPrint);
        if (d_servo_horn) render_micro_servo_horn(toPrint, penUp);
        if (d_male_connector_back) render_male_connector_back(toPrint);
        if (d_male_connector_front) render_male_connector_front(toPrint);
        if (d_logotype) render_logotype(toPrint);
        if (d_battery_pack) render_battery_pack(toPrint);
        if (d_battery_pack_upper_cover) render_battery_pack_upper_cover(toPrint);
        if (d_battery_pack_lower_cover) render_battery_pack_lower_cover(toPrint);
        if (d_battery_pack_connector_cover) render_battery_pack_connector_cover(toPrint);
        if (d_battery_pack_connector_lock) render_battery_pack_connector_lock(toPrint);
        if (d_battery_pack_bms_bracket) render_battery_pack_bms_bracket(toPrint);
        if (d_battery_clip) render_battery_clip(toPrint);
        if (d_eye_surround) render_eye_surround(toPrint);
        if (d_eye_light_pipe) render_eye_light_pipe(toPrint);
        if (d_stand) render_stand(toPrint);
        if (d_stand_lower_cover) render_stand_lower_cover(toPrint);
        if (d_stand_upper_cover) render_stand_upper_cover(toPrint);
        if (d_eye_pcb_jig) render_eye_pcb_jig(toPrint);
        if (d_aux_pcb_mount) render_aux_pcb_mount(toPrint);
        if (d_aux_pcb_screw_washer) render_aux_pcb_screw_washer(toPrint);

        // Render the support enforcers
        if (d_shell_supports) render_shell_supports(toPrint);
        if (d_battery_pack_supports) render_battery_pack_supports(toPrint);
        if (d_battery_pack_lower_cover_supports) render_battery_pack_lower_cover_supports(toPrint);
        if (d_battery_pack_upper_cover_supports) render_battery_pack_upper_cover_supports(toPrint);
        if (d_body_left_supports) render_body_left_supports(toPrint);
        if (d_body_right_supports) render_body_right_supports(toPrint);
        if (d_stand_lower_cover_supports) render_stand_lower_cover_supports(toPrint);
        if (d_stand_upper_cover_supports) render_stand_upper_cover_supports(toPrint);

        // Render the non-printable parts
        if (d_motor_left) render_motor_left(toPrint);
        if (d_motor_right) render_motor_right(toPrint);
        if (d_rotational_axis) render_rotational_axis(toPrint);
        if (d_turning_circle) render_turning_circle(toPrint);
        if (d_tire_left) render_tire_left(toPrint);
        if (d_tire_right) render_tire_right(toPrint);
        if (d_main_pcb) render_main_pcb(toPrint);
        if (d_aux_pcb) render_aux_pcb(toPrint);
        if (d_eye_pcb) render_eye_pcb(toPrint);
        if (d_ball_bearing) render_ball_bearing(toPrint);
        if (d_pen) render_pen(toPrint, penUp);
        if (d_servo) render_micro_servo(toPrint);
        if (d_batteries) render_batteries(toPrint);
        if (d_battery_pack_bms_pcb) render_battery_pack_bms_pcb(toPrint);
        if (d_toggle_switch) render_toggle_switch(toPrint);
        if (d_logotype_2D) render_logotype_2D(toPrint);
        if (d_battery_clip_contacts) render_battery_clip_contacts(toPrint);
        if (d_male_bullet_connectors) render_male_bullet_connectors(toPrint);
        if (d_female_bullet_connectors) render_female_bullet_connectors(toPrint);

        // Render screws
        if (d_motor_mount_screws_left) render_motor_mount_screws_left(toPrint);
        if (d_motor_mount_screws_right) render_motor_mount_screws_right(toPrint);
        if (d_body_left_screws) render_body_left_screws(toPrint);
        if (d_body_right_screws) render_body_right_screws(toPrint);
        if (d_motor_bay_screws_left) render_motor_bay_screws_left(toPrint);
        if (d_motor_bay_screws_right) render_motor_bay_screws_right(toPrint);
        if (d_head_screws) render_head_screws(toPrint);
        if (d_servo_holder_screws) render_servo_holder_screws(toPrint);
        if (d_main_pcb_mounts_front_screws) render_main_pcb_mounts_front_screws(toPrint);
        if (d_main_pcb_mounts_back_screws) render_main_pcb_mounts_back_screws(toPrint);
        if (d_shell_screws) render_shell_screws(toPrint);
        if (d_battery_screws) render_battery_screws(toPrint);
        if (d_aux_pcb_screws) render_aux_pcb_screws(toPrint);
    }
}

// Set the arc resolution higher when in printing mode
if (for_printing == "Printing") {
    $fn=50;
    main();
} else {
    $fn=20;
    main();
}