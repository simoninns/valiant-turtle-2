#!bin/bash
echo "Generating 3D STL model files..."
echo "  body_left.stl"
openscad -o ./stl/body_left.stl -D 'for_printing="Printing"' -D 'display_body_left="Yes"' ./scad/main.scad
echo "  body_right.stl"
openscad -o ./stl/body_right.stl -D 'for_printing="Printing"' -D 'display_body_right="Yes"' ./scad/main.scad
echo "  head.stl"
openscad -o ./stl/head.stl -D 'for_printing="Printing"' -D 'display_head="Yes"' ./scad/main.scad
echo "  head_cover.stl"
openscad -o ./stl/head_cover.stl -D 'for_printing="Printing"' -D 'display_head_cover="Yes"' ./scad/main.scad
echo "  shell.stl"
openscad -o ./stl/shell.stl -D 'for_printing="Printing"' -D 'display_shell="Yes"' ./scad/main.scad
echo "  motor_bay_left.stl"
openscad -o ./stl/motor_bay_left.stl -D 'for_printing="Printing"' -D 'display_motor_bay_left="Yes"' ./scad/main.scad
echo "  motor_bay_right.stl"
openscad -o ./stl/motor_bay_right.stl -D 'for_printing="Printing"' -D 'display_motor_bay_right="Yes"' ./scad/main.scad
echo "  motor_mount_left.stl"
openscad -o ./stl/motor_mount_left.stl -D 'for_printing="Printing"' -D 'display_motor_mount_left="Yes"' ./scad/main.scad
echo "  motor_mount_right.stl"
openscad -o ./stl/motor_mount_right.stl -D 'for_printing="Printing"' -D 'display_motor_mount_right="Yes"' ./scad/main.scad
echo "  wheel_left.stl"
openscad -o ./stl/wheel_left.stl -D 'for_printing="Printing"' -D 'display_wheel_left="Yes"' ./scad/main.scad
echo "  wheel_right.stl"
openscad -o ./stl/wheel_right.stl -D 'for_printing="Printing"' -D 'display_wheel_right="Yes"' ./scad/main.scad
echo "  main_pcb_mounts_front.stl"
openscad -o ./stl/main_pcb_mounts_front.stl -D 'for_printing="Printing"' -D 'display_main_pcb_mounts_front="Yes"' ./scad/main.scad
echo "  main_pcb_mounts_back.stl"
openscad -o ./stl/main_pcb_mounts_front.stl -D 'for_printing="Printing"' -D 'display_main_pcb_mounts_front="Yes"' ./scad/main.scad
echo "  main_pcb_screw_washer.stl"
openscad -o ./stl/main_pcb_screw_washer.stl -D 'for_printing="Printing"' -D 'display_main_pcb_screw_washer="Yes"' ./scad/main.scad
echo "  pen_holder_base.stl"
openscad -o ./stl/pen_holder_base.stl -D 'for_printing="Printing"' -D 'display_pen_holder_base="Yes"' ./scad/main.scad
echo "  pen_holder_top_small.stl"
openscad -o ./stl/pen_holder_top_small.stl -D 'for_printing="Printing"' -D 'display_pen_holder_top_small="Yes"' ./scad/main.scad
echo "  pen_holder_top_medium.stl"
openscad -o ./stl/pen_holder_top_medium.stl -D 'for_printing="Printing"' -D 'display_pen_holder_top_medium="Yes"' ./scad/main.scad
echo "  pen_holder_top_large.stl"
openscad -o ./stl/pen_holder_top_large.stl -D 'for_printing="Printing"' -D 'display_pen_holder_top_large="Yes"' ./scad/main.scad
echo "  pen_holder_cap.stl"
openscad -o ./stl/pen_holder_cap.stl -D 'for_printing="Printing"' -D 'display_pen_holder_cap="Yes"' ./scad/main.scad
echo "  servo_holder.stl"
openscad -o ./stl/servo_holder.stl -D 'for_printing="Printing"' -D 'display_servo_holder="Yes"' ./scad/main.scad
echo "  servo_horn.stl"
openscad -o ./stl/servo_horn.stl -D 'for_printing="Printing"' -D 'display_servo_horn="Yes"' ./scad/main.scad
echo "  male_connector_back.stl"
openscad -o ./stl/male_connector_back.stl -D 'for_printing="Printing"' -D 'display_male_connector_back="Yes"' ./scad/main.scad
echo "  male_connector_front.stl"
openscad -o ./stl/male_connector_front.stl -D 'for_printing="Printing"' -D 'display_male_connector_front="Yes"' ./scad/main.scad
echo "  logotype.stl"
openscad -o ./stl/logotype.stl -D 'for_printing="Printing"' -D 'display_logotype="Yes"' ./scad/main.scad
echo "  battery_pack.stl"
openscad -o ./stl/battery_pack.stl -D 'for_printing="Printing"' -D 'display_battery_pack="Yes"' ./scad/main.scad
echo "  battery_pack_upper_cover.stl"
openscad -o ./stl/battery_pack_upper_cover.stl -D 'for_printing="Printing"' -D 'display_battery_pack_upper_cover="Yes"' ./scad/main.scad
echo "  battery_pack_lower_cover.stl"
openscad -o ./stl/battery_pack_lower_cover.stl -D 'for_printing="Printing"' -D 'display_battery_pack_lower_cover="Yes"' ./scad/main.scad
echo "  battery_pack_connector_cover.stl"
openscad -o ./stl/battery_pack_connector_cover.stl -D 'for_printing="Printing"' -D 'display_battery_pack_connector_cover="Yes"' ./scad/main.scad
echo "  battery_pack_connector_lock.stl"
openscad -o ./stl/battery_pack_connector_lock.stl -D 'for_printing="Printing"' -D 'display_battery_pack_connector_lock="Yes"' ./scad/main.scad
echo "  battery_pack_bms_bracket.stl"
openscad -o ./stl/battery_pack_bms_bracket.stl -D 'for_printing="Printing"' -D 'display_battery_pack_bms_bracket="Yes"' ./scad/main.scad
echo "  battery_clip.stl"
openscad -o ./stl/battery_clip.stl -D 'for_printing="Printing"' -D 'display_battery_clip="Yes"' ./scad/main.scad
echo "  eye_surround.stl"
openscad -o ./stl/eye_surround.stl -D 'for_printing="Printing"' -D 'display_eye_surround="Yes"' ./scad/main.scad
echo "  eye_light_pipe.stl"
openscad -o ./stl/eye_light_pipe.stl -D 'for_printing="Printing"' -D 'display_eye_light_pipe="Yes"' ./scad/main.scad
echo "  stand.stl"
openscad -o ./stl/stand.stl -D 'for_printing="Printing"' -D 'display_stand="Yes"' ./scad/main.scad
echo "  stand_lower_cover.stl"
openscad -o ./stl/stand_lower_cover.stl -D 'for_printing="Printing"' -D 'display_stand_lower_cover="Yes"' ./scad/main.scad
echo "  stand_upper_cover.stl"
openscad -o ./stl/stand_upper_cover.stl -D 'for_printing="Printing"' -D 'display_stand_upper_cover="Yes"' ./scad/main.scad
echo "  eye_pcb_jig.stl"
openscad -o ./stl/eye_pcb_jig.stl -D 'for_printing="Printing"' -D 'display_eye_pcb_jig="Yes"' ./scad/main.scad
echo "  aux_pcb_mount.stl"
openscad -o ./stl/aux_pcb_mount.stl -D 'for_printing="Printing"' -D 'display_aux_pcb_mount="Yes"' ./scad/main.scad

echo "Generating 3D STL support enforcer files..."
echo "  shell_support_enforcer.stl"
openscad -o ./stl_support_enforcers/shell_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_shell_supports="Yes"' ./scad/main.scad
echo "  battery_pack_support_enforcer.stl"
openscad -o ./stl_support_enforcers/battery_pack_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_battery_pack_supports="Yes"' ./scad/main.scad
echo "  battery_pack_lower_cover_support_enforcer.stl"
openscad -o ./stl_support_enforcers/battery_pack_lower_cover_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_battery_pack_lower_cover_supports="Yes"' ./scad/main.scad
echo "  battery_pack_upper_cover_support_enforcer.stl"
openscad -o ./stl_support_enforcers/battery_pack_upper_cover_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_battery_pack_upper_cover_supports="Yes"' ./scad/main.scad
echo "  body_left_support_enforcer.stl"
openscad -o ./stl_support_enforcers/body_left_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_body_left_supports="Yes"' ./scad/main.scad
echo "  body_right_support_enforcer.stl"
openscad -o ./stl_support_enforcers/body_right_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_body_right_supports="Yes"' ./scad/main.scad
echo "  stand_lower_cover_support_enforcer.stl"
openscad -o ./stl_support_enforcers/stand_lower_cover_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_stand_lower_cover_supports="Yes"' ./scad/main.scad
echo "  stand_upper_cover_support_enforcer.stl"
openscad -o ./stl_support_enforcers/stand_upper_cover_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_stand_upper_cover_supports="Yes"' ./scad/main.scad
echo "  servo_horn_support_enforcer.stl"
openscad -o ./stl_support_enforcers/servo_horn_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_servo_horn_support="Yes"' ./scad/main.scad

echo "Generating 2D DXF files for KiCAD..."
echo "  main_pcb.dxf"
openscad -o ./dxf/main_pcb.dxf -D 'for_printing="Printing"' -D 'display_main_pcb="Yes"' ./scad/main.scad
echo "  aux_pcb.dxf"
openscad -o ./dxf/aux_pcb.dxf -D 'for_printing="Printing"' -D 'display_aux_pcb="Yes"' ./scad/main.scad
echo "  eye_pcb.dxf"
openscad -o ./dxf/eye_pcb.dxf -D 'for_printing="Printing"' -D 'display_eye_pcb="Yes"' ./scad/main.scad
echo "  logotype_2D.dxf"
openscad -o ./dxf/logotype_2D.dxf -D 'for_printing="Printing"' -D 'display_logotype_2D="Yes"' ./scad/main.scad

echo "Generating 2D SVG files for Inkscape..."
echo "  logotype_2D.svg"
openscad -o ./svg/logotype_2D.svg -D 'for_printing="Printing"' -D 'display_logotype_2D="Yes"' ./scad/main.scad

echo "Script complete"


