#!bin/bash
echo "Generating 3D STL model files..."
echo "  case_base.stl"
openscad -o ./stl/case_base.stl -D 'for_printing="Printing"' -D 'display_case_base="Yes"' ./scad/main.scad
echo "  case_top.stl"
openscad -o ./stl/case_top.stl -D 'for_printing="Printing"' -D 'display_case_top="Yes"' ./scad/main.scad
echo "  panel_front.stl"
openscad -o ./stl/panel_front.stl -D 'for_printing="Printing"' -D 'display_panel_front="Yes"' ./scad/main.scad
echo "  panel_back.stl"
openscad -o ./stl/panel_back.stl -D 'for_printing="Printing"' -D 'display_panel_back="Yes"' ./scad/main.scad
echo "  panel_left.stl"
openscad -o ./stl/panel_left.stl -D 'for_printing="Printing"' -D 'display_panel_left="Yes"' ./scad/main.scad
echo "  panel_right.stl"
openscad -o ./stl/panel_right.stl -D 'for_printing="Printing"' -D 'display_panel_right="Yes"' ./scad/main.scad
echo "  label.stl"
openscad -o ./stl/label.stl -D 'for_printing="Printing"' -D 'display_label="Yes"' ./scad/main.scad
echo "  logo.stl"
openscad -o ./stl/logo.stl -D 'for_printing="Printing"' -D 'display_logo="Yes"' ./scad/main.scad
echo "  led_holder.stl"
openscad -o ./stl/led_holder.stl -D 'for_printing="Printing"' -D 'display_led_holder="Yes"' ./scad/main.scad

echo "Generating 2D DXF files for KiCAD..."
echo "  pcb.dxf"
openscad -o ./dxf/pcb.dxf -D 'for_printing="Printing"' -D 'display_pcb="Yes"' ./scad/main.scad

echo "Script complete"


