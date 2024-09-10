/************************************************************************

    servo_holder.scad
    
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

// Note: Both the left and right screw platforms are made to fit between the shell
// back screw mounts; this is to stop the shell sliding around sideways
module servo_holder_edges()
{
    move([30.5,34.5,8.5]) {
        difference() {
            union() {
                // Servo attachment towers
                move([-8,-14,0.5]) cuboid([7,4,16], chamfer=0.5, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);
                move([-8,+14,0.5]) cuboid([7,4,16], chamfer=0.5, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);

                // Right screw platform
                move([0.25,-2.5,-7]) cuboid([25.5,39,3], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL); 

                // Left screw platform
                move([-61.25,-2.5,-7]) cuboid([25.5,39,3], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);

                // Platform to make installing the servo easier
                move([4.5,0,-6]) cuboid([14,25,2], chamfer=0.5);
            }

            // Servo mounting holes
            move([-8,14,1.5]) xcyl(h=10,d=1.75);
            move([-8,-14,1.5]) xcyl(h=10,d=1.75);

            // M3 screw holes right
            move([8,12,-7]) cyl(h=5,d=3.5);
            move([8,-8,-7]) cyl(h=5,d=3.5);

            // M3 screw holes left
            move([-61,0,0]) {
                move([-8,12,-7]) cyl(h=5,d=3.5);
                move([-8,-8,-7]) cyl(h=5,d=3.5);
            }

            // M3 Recess
            move([8,12,-3.5 - 2]) cyl(h=3,d=6);
            move([8,-8,-3.5 - 2]) cyl(h=3,d=6);

            move([-61,0,0]) {
                move([-8,12,-3.5 - 2]) cyl(h=3,d=6);
                move([-8,-8,-3.5 - 2]) cyl(h=3,d=6);
            }

            // Hole for toggle switch
            move([-54,2.5,-6]) {
                cyl(h=12,d=7);
                move([6,0,0]) cyl(h=10,d=3);
            }
        }
    }
}

module pen_support()
{
    move([0,29,0.001]) {
        difference() {
            union() {
                cyl(h=24, d=25, center=false, chamfer2=0.5, $fn=8);
                move([0,0,1.5]) cuboid([60,33,3], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL); 
            }
            
            // Shaft center
            move([0,0,-1]) cyl(h=28, d=20.5, center=false, $fn=8);

            // Cut out for servo interface
            move([12,0,17]) cuboid([10,8.5,28]);

            // Servo horn clearance
            move([11.5,0,17.01]) cuboid([3,18,28]);

            // Round top edge of slot
            move([10,0,25]) xrot(45) cuboid([8.5,8.5,8.5]);

            // Clearance for servo horn in the base plate
            move([11.49,0,4]) cuboid([7,8.5,10]);
            move([13.5,0,4]) cuboid([7,12.5,6], chamfer=2, edges=EDGES_RIGHT+EDGES_X_ALL);

            // Hole for toggle switch
            move([-23.5,37-29,0]) {
                cyl(h=10,d=7);
                move([6,0,0]) cyl(h=10,d=3);
            }
        }
    }
}

module switch_support()
{
    move([-23.5,37,7]) {
        difference() {
            cuboid([17,10,8], chamfer=0.5, edges=EDGES_ALL-EDGES_BOTTOM);

            move([0,0,2]) cuboid([14,8,8]); // 13,6.5,9

            // Armature hole
            cyl(h=10,d=7);
            move([6,0,-6.99]) cyl(h=10,d=3, chamfer2=1.5);
        }
    }
}

module bullet_4mm_male()
{
    xrot(180) move([0,0,12.25/2]) difference() {
        union() {
            move([0,0,0]) cyl(h=12.25, d=3.25);
            move([0,0,2.25]) cyl(h=3.5, d=4);

            move([0,0,-3.5 - 0.125]) cyl(h=5, d=4.25);
            move([0,0,-4.5 +0.125]) cyl(h=3.5, d=4.75);
            move([0,0,-2.5 + 1]) cyl(h=0.75, d=4.75);
        }

        move([0,0,-9.5+4]) cyl(h=7, d=3.5);
        move([2,0,-5.25 + 0.5]) xcyl(h=4, d=2);
    }
}

module bullet_connector_male_mask()
{
    move([0,0,-9]) cyl(h=9,d=3.5);
    move([0,0,0.5]) cyl(h=1,d=3);
    move([0,0,-2.5]) cyl(h=5.5,d=5.5);
}

module male_connector_support()
{
    difference() {
        move([-23.5,18,6]) cuboid([24,11,12], chamfer=1, edges=EDGES_Z_ALL);
        move([-23.5,15.5,5]) cuboid([20.25,12.25,20]);

        // Slots for connector
        move([-12,16.5,1.5]) cuboid([3,3.25,16]);
        move([-12 - 23,16.5,1.5]) cuboid([3,3.25,16]);
    }

    // Top stays
    move([-23.5,17.5,11]) {
        move([-9.25,0,0]) yrot(90) right_triangle([2, 10, 2], center=true);
        move([+9.25,0,0]) yrot(180) right_triangle([2, 10, 2], center=true);
    }
}

module male_connector_back()
{
    difference() {
        move([-23.5,19,8.125]) {
            cuboid([20,5,7.75]);
            move([0,0,6]) cuboid([10,5,5]);
        }

        // Mask for the bullet connectors (male)
        move([-23.5,16.5,10.25]) {
            move([-3,0,0]) bullet_connector_male_mask();
            move([+3,0,0]) bullet_connector_male_mask();
        }

        // Cable clearance
        move([-23.5,16.5,11.5]) {
            move([-3,0,3.5]) cyl(h=8,d=3);
            move([+3,0,3.5]) cyl(h=8,d=3);
        }

        move([-23.5,17.5,11]) {
            move([-9.25,0,0]) yrot(90) right_triangle([2.01, 12, 2.01], center=true);
            move([+9.25,0,0]) yrot(180) right_triangle([2.01, 12, 2.01], center=true);
        }
    }

    // Slots
    difference() {
        union() {
            move([-13,17.25,4.75]) cuboid([2.75,1.5,9.5]);
            move([-13 - 21,17.25,4.75]) cuboid([2.75,1.5,9.5]);
        }
        move([-23.5,16,1.25]) cuboid([20.5,8,6]);
    }
}

module male_connector_front()
{
    difference() {
        move([-23.5,19 - 4.5,8.125]) {
            cuboid([20,4,7.75]);
            move([0,0,6]) cuboid([10,4,5]);
        }

        // Mask for the bullet connectors (male)
        move([-23.5,16.5,10.25]) {
            move([-3,0,0]) bullet_connector_male_mask();
            move([+3,0,0]) bullet_connector_male_mask();
        }

        // Cable clearance
        move([-23.5,16.5,11.5]) {
            move([-3,0,3.5]) cyl(h=8,d=3);
            move([+3,0,3.5]) cyl(h=8,d=3);
        }

        move([-23.5,17.5,11]) {
            move([-9.25,0,0]) yrot(90) right_triangle([2.01, 12, 2.01], center=true);
            move([+9.25,0,0]) yrot(180) right_triangle([2.01, 12, 2.01], center=true);
        }
    }

    // Slots
    difference() {
        union() {
            move([-13,15.75,4.75]) cuboid([2.75,1.5,9.5]);
            move([-13 - 21,15.75,4.75]) cuboid([2.75,1.5,9.5]);
        }
        move([-23.5,16,1.25]) cuboid([20.5,8,6]);
    }
}

module servo_holder()
{
    difference() {
        union() {
            servo_holder_edges();
            pen_support();
            switch_support();
        }

        // Cut-out for power connector
        move([-23.5,15.5,0]) cuboid([20.25,12.25,12]);

        // Slots for connector
        move([-13,16.5,1.5]) cuboid([3,3.25,16]);
        move([-11 - 23,16.5,1.5]) cuboid([3,3.25,16]);
    }

    male_connector_support();
}

module render_male_connector_back(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]);
        male_connector_back();

    } else {
        move([23,-7,21.5]) xrot(-90) male_connector_back();
    }
}

module render_male_connector_front(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]);
        male_connector_front();

    } else {
        move([23,7,-12.5]) xrot(90) male_connector_front();
    }
}

module render_servo_holder(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) servo_holder();

        // Add in the bullet connectors
        move([-23.5,16.5,10.25]) {
            move([-3,0,0]) bullet_4mm_male();
            move([+3,0,0]) bullet_4mm_male();
        }
    } else {
        move([0,-29,0]) servo_holder();
    }
}

module render_servo_holder_screws(toPrint)
{
    if (!toPrint) {
        move([30.5,34.5,8.5]) {
            move([8,12,-5.5 - 1.5]) m3x10_screw();
            move([8,-8,-5.5 - 1.5]) m3x10_screw();
        }

        move([-30.5,34.5,8.5]) {
            move([-8,12,-5.5 - 1.5]) m3x10_screw();
            move([-8,-8,-5.5 - 1.5]) m3x10_screw();
        }
    }
}