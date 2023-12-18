/************************************************************************

    motor_bay.scad
    
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

include <threaded_inserts.scad>

module mount_profile_right(pos)
{
    move(pos) yrot(-90) cyl(h=3, d=3, fillet1=1.5, $fn=16);
}

module mount_profile_left(pos)
{
    move(pos) yrot(-90) cyl(h=3, d=3, fillet2=1.5, $fn=16);
}

module motor_bay_side_panels()
{
    pointA = [0,0,-0.5];
    pointB = [0,0,-17];
    pointC = [0,30 - 10.5,-27];
    pointD = [0,65,-27];
    pointE = [0,70,-25];
    pointF = [0,75,-20];
    pointG = [0,80,-0.5];

    width = 65;
    pos = -13;

    // Outer side panel
    move([120.5,pos,-1.5]) {
        hull() {
            mount_profile_right(pointA);
            mount_profile_right(pointB);
            mount_profile_right(pointC);
            mount_profile_right(pointD);
            mount_profile_right(pointE);
            mount_profile_right(pointF);
            mount_profile_right(pointG);
        }
    }

    // Inner side panel
    move([120.5 - width,pos,-1.5]) {
        hull() {
            mount_profile_left(pointA);
            mount_profile_left(pointB);
            mount_profile_left(pointC);
            mount_profile_left(pointD);
            mount_profile_left(pointE);
            mount_profile_left(pointF);
            mount_profile_left(pointG);
        }
    }
}

module motor_bay_shape()
{
    pointA = [0,0,-0.5];
    pointB = [0,0,-17];
    pointC = [0,30 - 10.5,-27];
    pointD = [0,65,-27];
    pointE = [0,70,-25];
    pointF = [0,75,-20];
    pointG = [0,80,-0.5];

    width = 65;
    pos = -13;

    // Front part
    hull() {
        move([120.5,pos,-1.5]) {
            mount_profile_right(pointA);
            mount_profile_right(pointB);
        }

        move([120.5 - width,pos,-1.5]) {
            mount_profile_left(pointA);
            mount_profile_left(pointB);
        }
    }

    hull() {
        move([120.5,pos,-1.5]) {
            mount_profile_right(pointF);
            mount_profile_right(pointG);
        }

        move([120.5 - width,pos,-1.5]) {
            mount_profile_left(pointF);
            mount_profile_left(pointG);
        }
    }

    hull() {
        move([120.5,pos,-1.5]) {
            mount_profile_right(pointB);
            mount_profile_right(pointC);
        }

        move([120.5 - width,pos,-1.5]) {
            mount_profile_left(pointB);
            mount_profile_left(pointC);
        }
    }

    // Middle part
    difference() {
        hull() {
            move([120.5,pos,-1.5]) {
                mount_profile_right(pointC);
                mount_profile_right(pointD);
            }

            move([120.5 - width,pos,-1.5]) {
                mount_profile_left(pointC);
                mount_profile_left(pointD);
            }
        }

        // Cut-out to allow wheel to come through
        move([112.5,pos + 42,-28]) cuboid([15,40,10], chamfer=1);

        // Additional motor clearance
        move([74,pos + 42,-22.75]) cuboid([45,44,10], chamfer=1);

        // Wheel position marker to align wheel on axel
        move([110,pos + 42,-27]) cuboid([4.5,43,2]);
    }
    
    // Back part
    hull() {
        move([120.5,pos,-1.5]) {
            mount_profile_right(pointD);
            mount_profile_right(pointE);
        }

        move([120.5 - width,pos,-1.5]) {
            mount_profile_left(pointD);
            mount_profile_left(pointE);
        }
    }

    hull() {
        move([120.5,pos,-1.5]) {
            mount_profile_right(pointE);
            mount_profile_right(pointF);
        }

        move([120.5 - width,pos,-1.5]) {
            mount_profile_left(pointE);
            mount_profile_left(pointF);
        }
    }

    // Mount points to attach to main body
    difference() {
        union() {
            move([62,-8,-11]) cuboid([10,9,24]);
            move([62,60.5,-12]) cuboid([10,9.5,20]);

            difference() {
                move([112,-8,-13]) cuboid([20,9,20]);
                move([112-9,-7,-13]) zrot(45) cuboid([20,9,22]);
            }
            difference() {
                move([112,62,-12]) cuboid([20,7.5,23]);
                move([112-9,60,-13]) zrot(-45) cuboid([20,9,25]);
            }
        }

        // Front
        move([0,0,0.1]) {
            move([59.5 + 2.5,-7.5,-10]) xrot(180) cyl(h=18,d=5);
            move([116.5 - 2.5,-7.5,-10]) xrot(180) cyl(h=18,d=5);

            // Back
            move([59.5 + 2.5,62,-10]) xrot(180) cyl(h=18,d=5);
            move([116.5 - 2.5,62,-10]) xrot(180) cyl(h=18,d=5);   
        }

        // Clean up the outer edges
        move([100,70,-14]) xrot(-13) cuboid([90,10,20]);
        move([100,-10,-26]) xrot(62) cuboid([90,10,20]);
        move([100,66,-26]) xrot(-45) cuboid([90,10,20]);
    }
    
    

    // Add the inserts
    move([0,0,-2]) {
        move([59.5 + 2.5,-7.5,-3]) insertM3x57_th();
        move([116.5 - 2.5,-7.5,-3]) insertM3x57_th();
        move([59.5 + 2.5,62, -3]) insertM3x57_th();
        move([116.5 - 2.5,62,-3]) insertM3x57_th();
    }

    // Platform to attach the motor mounts to
    motor_platform();
}

module motor_platform()
{
    difference() {
        union() {
            move([76-4,2.5,-21]) cuboid([39,9,14], chamfer=1, edges=EDGES_X_ALL); 
            move([76-4,55.5,-21]) cuboid([39,9,14], chamfer=1, edges=EDGES_X_ALL); 
        }

        // Threaded insert slot
        move([86,5-2,-17.9]) xrot(180) cyl(h=8,d=5);
        move([90-25,5-2,-17.9]) xrot(180) cyl(h=8,d=5);

        move([86,53 + 2,-17.9]) xrot(180) cyl(h=8,d=5);
        move([90-18,53 + 2,-17.9]) xrot(180) cyl(h=8,d=5);

        // Trim mounts
        move([77.5,0,-32]) xrot(60) cuboid([42,10,14]);
        move([77.5,60,-32]) xrot(-50) cuboid([42,10,14]); 
    }

    // Threaded inserts
    move([86,5-2,-14]) insertM3x57();
    move([90-25,5-2,-14]) insertM3x57();

    move([86,53 + 2,-14]) insertM3x57();
    move([90-18,53 + 2,-14]) insertM3x57();
}

module body_recess()
{
    move([88,-7.5,-2.5]) cuboid([64,9,4]);
    move([88,62-1.5,-2.5]) cuboid([64,12,4]);
}

module motor_bay()
{
    difference() {
        motor_bay_shape();

        // Trim all the egdes to fit into body
        move([52,10,-25]) cuboid([10,120,50]);
        move([124,10,-25]) cuboid([10,120,50]);
        move([84,26,2]) cuboid([80,90,10]);
        move([84,69.5,-5]) cuboid([80,4,8]);

        // Recess the top of the body screw holes
        body_recess();
    }
}

module render_motor_bay(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            motor_bay();
            xflip() motor_bay();
        }
    } else {
        move([10,0,-57]) yrot(-90) motor_bay();
        xflip() move([10,0,-57]) yrot(-90) motor_bay();
    }
}

module motor_bay_screws()
{
    move([0,0,6]) {
        move([59.5 + 2.5,-7.5,-8]) m3x10_screw();
        move([116.5 - 2.5,-7.5,-8]) m3x10_screw();

        // Back
        move([59.5 + 2.5,62,-8]) m3x10_screw();
        move([116.5 - 2.5,62,-8]) m3x10_screw(); 
    }
}

module render_motor_bay_screws(crend, toPrint)
{
    if (!toPrint) {
        motor_bay_screws();
        xflip() motor_bay_screws();
    }
}