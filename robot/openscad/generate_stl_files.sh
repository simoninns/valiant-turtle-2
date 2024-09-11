#!bin/bash
echo "Generating STL model files..."
openscad -o ./stl/body_left.stl -D 'for_printing="Printing"' -D 'display_body_left="Yes"' ./scad/main.scad
openscad -o ./stl/body_right.stl -D 'for_printing="Printing"' -D 'display_body_right="Yes"' ./scad/main.scad
openscad -o ./stl/head.stl -D 'for_printing="Printing"' -D 'display_head="Yes"' ./scad/main.scad
openscad -o ./stl/head_shell_screw_guide.stl -D 'for_printing="Printing"' -D 'display_head_shell_screw_guide="Yes"' ./scad/main.scad
openscad -o ./stl/head_cover.stl -D 'for_printing="Printing"' -D 'display_head_cover="Yes"' ./scad/main.scad
openscad -o ./stl/shell_lid.stl -D 'for_printing="Printing"' -D 'display_shell_lid="Yes"' ./scad/main.scad
openscad -o ./stl/shell.stl -D 'for_printing="Printing"' -D 'display_shell="Yes"' ./scad/main.scad
openscad -o ./stl/shell_dot.stl -D 'for_printing="Printing"' -D 'display_shell_dot="Yes"' ./scad/main.scad
openscad -o ./stl/motor_bay.stl -D 'for_printing="Printing"' -D 'display_motor_bay="Yes"' ./scad/main.scad
openscad -o ./stl/motor_mounts.stl -D 'for_printing="Printing"' -D 'display_motor_mounts="Yes"' ./scad/main.scad
openscad -o ./stl/wheels.stl -D 'for_printing="Printing"' -D 'display_wheels="Yes"' ./scad/main.scad
openscad -o ./stl/main_pcb_mounts_front.stl -D 'for_printing="Printing"' -D 'display_main_pcb_mounts_front="Yes"' ./scad/main.scad
openscad -o ./stl/main_pcb_mounts_back.stl -D 'for_printing="Printing"' -D 'display_main_pcb_mounts_back="Yes"' ./scad/main.scad
openscad -o ./stl/pen_holder_base.stl -D 'for_printing="Printing"' -D 'display_pen_holder_base="Yes"' ./scad/main.scad
openscad -o ./stl/pen_holder_top_small.stl -D 'for_printing="Printing"' -D 'display_pen_holder_top_small="Yes"' ./scad/main.scad
openscad -o ./stl/pen_holder_top_medium.stl -D 'for_printing="Printing"' -D 'display_pen_holder_top_medium="Yes"' ./scad/main.scad
openscad -o ./stl/pen_holder_top_large.stl -D 'for_printing="Printing"' -D 'display_pen_holder_top_large="Yes"' ./scad/main.scad
openscad -o ./stl/pen_holder_cap.stl -D 'for_printing="Printing"' -D 'display_pen_holder_cap="Yes"' ./scad/main.scad
openscad -o ./stl/servo_holder.stl -D 'for_printing="Printing"' -D 'display_servo_holder="Yes"' ./scad/main.scad
openscad -o ./stl/servo_horn.stl -D 'for_printing="Printing"' -D 'display_servo_horn="Yes"' ./scad/main.scad
openscad -o ./stl/male_connector_back.stl -D 'for_printing="Printing"' -D 'display_male_connector_back="Yes"' ./scad/main.scad
openscad -o ./stl/male_connector_front.stl -D 'for_printing="Printing"' -D 'display_male_connector_front="Yes"' ./scad/main.scad
openscad -o ./stl/logotype.stl -D 'for_printing="Printing"' -D 'display_logotype="Yes"' ./scad/main.scad
openscad -o ./stl/battery_pack.stl -D 'for_printing="Printing"' -D 'display_battery_pack="Yes"' ./scad/main.scad
openscad -o ./stl/battery_pack_upper_cover.stl -D 'for_printing="Printing"' -D 'display_battery_pack_upper_cover="Yes"' ./scad/main.scad
openscad -o ./stl/battery_pack_lower_cover.stl -D 'for_printing="Printing"' -D 'display_battery_pack_lower_cover="Yes"' ./scad/main.scad
openscad -o ./stl/battery_pack_connector_cover.stl -D 'for_printing="Printing"' -D 'display_battery_pack_connector_cover="Yes"' ./scad/main.scad
openscad -o ./stl/battery_pack_connector_lock.stl -D 'for_printing="Printing"' -D 'display_battery_pack_connector_lock="Yes"' ./scad/main.scad
openscad -o ./stl/eye_surround.stl -D 'for_printing="Printing"' -D 'display_eye_surround="Yes"' ./scad/main.scad
openscad -o ./stl/eye_light_pipe.stl -D 'for_printing="Printing"' -D 'display_eye_light_pipe="Yes"' ./scad/main.scad
openscad -o ./stl/eye_light_pipe_surround.stl -D 'for_printing="Printing"' -D 'display_eye_light_pipe_surround="Yes"' ./scad/main.scad
openscad -o ./stl/display_mount.stl -D 'for_printing="Printing"' -D 'display_display_mount="Yes"' ./scad/main.scad
openscad -o ./stl/stand.stl -D 'for_printing="Printing"' -D 'display_stand="Yes"' ./scad/main.scad
openscad -o ./stl/stand_battery_cover.stl -D 'for_printing="Printing"' -D 'display_stand_battery_cover="Yes"' ./scad/main.scad

echo "Generating STL support files..."
openscad -o ./stl_supports/shell_support.stl -D 'for_printing="Printing"' -D 'display_shell_support="Yes"' ./scad/main.scad

echo "Script complete"


