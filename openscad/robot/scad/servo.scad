/************************************************************************

    servo.scad
    
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

module micro_servo_horn(angle)
{
    zrot(angle) difference() {
        union() {
            hull() {
                // Rounded rhombus
                move([0,0,0]) cyl(d=8, h=4, center=true, chamfer2=0.5);
                move([-7,0,0]) cyl(d=8, h=4, center=true, chamfer2=0.5);
            }

            // Shaft
            move([0,0,1.5]) cyl(d=7, h=4.5, center=true);
        }

        // Remove center material from shaft
        move([0,0,-2]) cyl(d=5, h=4, center=true);
        move([0,0,2]) cyl(d=2.5, h=6, center=true);
        move([0,0,2.5]) cyl(d=5, h=3, center=true);
    }

    // Servo shaft grip 21T d=4.8mm
    // Note: On a standard FFF printer this is more of a press-fit - but it works fine anyway
    for(rota=[0: 360/21: 360]) {
        rotate([0,0,rota]) move([5.25 / 2,0,2.25]) zrot(45) cuboid([0.5,0.5,3]);
    }
}

module micro_servo()
{
    // Colours
    shell_c = [0.1,0.4,0.9];
    shaft_c = [0.9,0.9,0.9];

    difference(){			
		union(){
            color(shell_c) {
                cuboid([23,12.5,22], center=true, chamfer=0.5);
                move([0,0,5]) cuboid([32,12,2], center=true, chamfer=0.5, edges=EDGES_Z_ALL);
                move([5.5,0,2.75]) cyl(r=6, h=25.75, $fn=20, center=true, chamfer=0.5);
                move([-.5,0,2.75]) cyl(r=1, h=25.75, $fn=20, center=true);
                move([-1,0,2.75]) cuboid([5,5.6,24.5], center=true, chamfer=0.5);
            }

			color(shaft_c) {
                move([5.5,0,3.65]) cyl(r=2.35, h=29.25, $fn=20, center=true);
            }
		}

		for ( mounting_hole = [14,-14] ){
			move([mounting_hole,0,5]) cyl(r=2.2, h=4, $fn=20, center=true);
		}	
	}
}

module render_micro_servo(toPrint)
{
    if (!toPrint) {
        move([32,34.5,11]) xrot(90) yrot(-90) {
            micro_servo();
        }
    }
}

module render_micro_servo_horn(toPrint, penUp)
{
    if (!toPrint) {
        move([0,0,0]) {
            color([0.9,0.9,0.9,1]) yrot(90) {
                move([-11,29,12.5]) {
                    if (penUp) micro_servo_horn(0);
                    else micro_servo_horn(90);
                }
            }
        }
    } else {
        move([0,0,2]) micro_servo_horn(0);
    }
}

module render_micro_servo_horn_support(toPrint)
{
    if (toPrint) {
        move([0,0,1.5]) cyl(h=3, d=5.5);
    }
}