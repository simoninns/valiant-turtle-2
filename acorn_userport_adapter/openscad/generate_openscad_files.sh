#!bin/bash
echo "Generating 3D STL model files..."
echo "  case_bottom.stl"
openscad -o ./stl/case_bottom.stl -D 'for_printing="Printing"' -D 'display_case_bottom="Yes"' ./scad/main.scad
echo "  case_top.stl"
openscad -o ./stl/case_top.stl -D 'for_printing="Printing"' -D 'display_case_top="Yes"' ./scad/main.scad

echo "Script complete"


