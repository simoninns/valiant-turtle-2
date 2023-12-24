/************************************************************************

    servo_holder.scad
    
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

module servo_holder()
{
    move([30.5,34.5,8.5]) {
        difference() {
            union() {
                difference() {
                    union() {
                        move([1,-14,0.5]) cuboid([7,7,16], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);
                        move([1,+14,0.5]) cuboid([7,7,16], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);
                    }

                    // Servo clearance
                    move([0,0,0]) cuboid([30,24,18]);
                }

                move([5,-1.5,-7]) cuboid([15,42,3], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);    
            }

            // Servo mounting holes
            move([0,14,1.5]) xcyl(h=10,d=2);
            move([0,-14,1.5]) xcyl(h=10,d=2);

            // M3 screw holes
            move([8,15,-7]) cyl(h=5,d=3);
            move([8,-18,-7]) cyl(h=5,d=3);
        }

        // Platform to make installing the servo easier
        move([4.5,0,-6]) cuboid([14,25,2], chamfer=0.5);
    }

    move([-30.5,34.5,8.5]) {
        difference() {
            move([-5,-1.5,-7]) cuboid([15,42,3], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);

            // M3 screw holes
            move([-8,15,-7]) cyl(h=5,d=3);
            move([-8,-18,-7]) cyl(h=5,d=3);
        }
    }
}

module pen_support()
{
    move([0,29,0]) {
        difference() {
            union() {
                cyl(h=24, d=25, center=false, chamfer2=0.5, $fn=8);
                move([0,0.5,1.5]) cuboid([60,35,3], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL); 
            }
            
            // Shaft center
            move([0,0,-1]) cyl(h=28, d=20.5, center=false, $fn=8);

            // Cut out for servo interface
            move([12,0,17]) cuboid([10,8.5,28]);

            // Servo horn clearance
            move([11.5,0,17.01]) cuboid([3,18,28]);

            // Round top edge of slot
            move([10,0,25]) xrot(45) cuboid([8.5,8.5,8.5]);
        }
    }
}

module render_servo_holder(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            servo_holder();
            pen_support();
        }
    } else {
        move([0,-29,0]) {
            servo_holder();
            pen_support();
        }
    }
}

module render_servo_holder_screws(crend, toPrint)
{
    if (!toPrint) {
        move([30.5,34.5,8.5]) {
            move([8,15,-5.5]) m3x10_screw();
            move([8,-18,-5.5]) m3x10_screw();
        }

        move([-30.5,34.5,8.5]) {
            move([-8,15,-5.5]) m3x10_screw();
            move([-8,-18,-5.5]) m3x10_screw();
        }
    }
}