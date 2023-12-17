/************************************************************************

    servo.scad
    
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

module nineg_servo_arm()
{
    shaft_c = [0.9,0.9,0.9];

    color(shaft_c) difference() {
        union() {
            move([5.5,0,18.5]) cyl(d=6.75, h=4.5, $fn=20, center=true);

            hull() {
                move([5.5,0,20]) cyl(d=6, h=1.5, $fn=20, center=true);
                move([5.5-15,0,20]) cyl(d=5, h=1.5, $fn=20, center=true);
            }
        }

        move([5.5,0,20]) cyl(d=4.5, h=2, $fn=20, center=true);
    }
}

module nineg_servo()
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

module render_9g_servo(crend, toPrint)
{
    if (!toPrint) {
        move([32,38,10]) xrot(-90) yrot(-90) {
            nineg_servo();
            nineg_servo_arm();
        }
    }
}