#!bin/bash
echo "Generating 3D STL model files..."
echo "  base.stl"
openscad -o ./stl/base.stl -D 'for_printing="Printing"' -D 'display_charger_base="Yes"' ./scad/main.scad
echo "  lid.stl"
openscad -o ./stl/lid.stl -D 'for_printing="Printing"' -D 'display_charger_lid="Yes"' ./scad/main.scad
echo "  connector_front.stl"
openscad -o ./stl/connector_front.stl -D 'for_printing="Printing"' -D 'display_connector_front="Yes"' ./scad/main.scad
echo "  connector_back.stl"
openscad -o ./stl/connector_back.stl -D 'for_printing="Printing"' -D 'display_connector_back="Yes"' ./scad/main.scad
echo "  light_pipe.stl"
openscad -o ./stl/light_pipe.stl -D 'for_printing="Printing"' -D 'display_light_pipe="Yes"' ./scad/main.scad

echo "Generating 3D STL support enforcer files..."
echo "  charger_lid_support_enforcers.stl"
openscad -o ./stl_support_enforcers/charger_lid_support_enforcers.stl -D 'for_printing="Printing"' -D 'display_charger_lid_support_enforcers="Yes"' ./scad/main.scad
echo " connector_back_support_enforcer.stl"
openscad -o ./stl_support_enforcers/connector_back_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_connector_back_support="Yes"' ./scad/main.scad
echo "  connector_front_support_enforcer.stl"
openscad -o ./stl_support_enforcers/connector_front_support_enforcer.stl -D 'for_printing="Printing"' -D 'display_connector_front_support="Yes"' ./scad/main.scad

echo "Script complete"


