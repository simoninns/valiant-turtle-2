/************************************************************************

    motor_mounts.scad
    
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
use <BOSL/nema_steppers.scad>

include <threaded_inserts.scad>

module nema17_motor()
{
    // Render the motor with the shaft pointing right and the cable to the back
    xrot(-90) yrot(90) nema17_stepper(h=40, shaft=5, shaft_len=20, orient=ORIENT_Z);
}

module wheel_body()
{
    // Main wheel body
    owd = 52;
    iwd = 47;

    move([0,0,0]) yrot(-90) cyl(h=0.5, d=owd);
    move([1,0,0]) yrot(-90) cyl(h=1.5, d2=owd, d1=iwd);

    move([2.25,0,0]) xcyl(h=3.5, d=owd - 4);
    move([3,0,0]) yrot(-90) cyl(h=1.5, d1=owd, d2=iwd);
    move([0.5 + 3.5,0,0]) xcyl(h=0.5, d=owd);
}

module wheel_hub()
{
    difference() {
        union() {
            move([7,0,0]) yrot(-90) cyl(h=7.5,d=22, chamfer=0.5);
            move([7.25,0,0]) cuboid([6,7,22], chamfer=0.5);
        }

        // Setting screw hole
        move([7.25,0,6]) xrot(180) cyl(h=12,d=3.25);

        // Threaded insert slot
        move([7.25,0,7.1]) xrot(180) cyl(h=8,d=5);
    }

    // Add in the screw insert
    difference() {
        move([7.25,0,11]) insertM3x57();
        
        // Setting screw hole
        move([7.25,0,6]) xrot(180) cyl(h=12,d=3.25);
    }
}

module wheel_hub_decoration()
{
    for (rot = [0:360/12: 360-1]) {
        xrot(rot) hull() {
            move([2,0,14]) yrot(-90) cyl(h=10,d=3);
            move([2,0,21.5]) yrot(-90) cyl(h=10,d=3);
        }

        xrot(rot) hull() {
            move([5.25,0,14]) yrot(-90) cyl(h=4,d=5, chamfer=1);
            move([5.25,0,21.5]) yrot(-90) cyl(h=4,d=5, chamfer=1);
        }
    }
}

module tire()
{
    // O-ring Tire - R31 - AS 568 225 - ID=47.22, OD=54.28, section=3.53
    move([2,0,0]) yrot(90) torus(id=47.22, od=54.28);
}

module wheel()
{
    difference() {
        union() {
            wheel_body();
            wheel_hub();
        }

        // Hub
        move([5,0,0]) yrot(-90) cyl(h=20,d=5);

        wheel_hub_decoration();
    }

    tire();
}

module mount_profile_right(pos)
{
    move(pos) yrot(-90) cyl(h=3, d=3, fillet1=1.5);
}

module mount_profile_left(pos)
{
    move(pos) yrot(-90) cyl(h=3, d=3, fillet2=1.5);
}

module motor_bay()
{
    pointA = [0,0,0];
    pointB = [0,0,-17];
    pointC = [0,30 - 10,-27];
    pointD = [0,65,-27];
    pointE = [0,70,-25];
    pointF = [0,75,-20];
    pointG = [0,80,0];

    width = 65;

    // Outer side panel
    move([120.5,-12,-1.5]) {
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
    move([120.5 - width,-12,-1.5]) {
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

    // Front panel
    hull() {
        move([120.5,-12,-1.5]) {
            mount_profile_right(pointA);
            mount_profile_right(pointB);
        }

        move([120.5 - width,-12,-1.5]) {
            mount_profile_left(pointA);
            mount_profile_left(pointB);
        }
    }

    hull() {
        move([120.5,-12,-1.5]) {
            mount_profile_right(pointB);
            mount_profile_right(pointC);
        }

        move([120.5 - width,-12,-1.5]) {
            mount_profile_left(pointB);
            mount_profile_left(pointC);
        }
    }

    // Base
    difference() {
        hull() {
            move([120.5,-12,-1.5]) {
                mount_profile_right(pointC);
                mount_profile_right(pointD);
            }

            move([120.5 - width,-12,-1.5]) {
                mount_profile_left(pointC);
                mount_profile_left(pointD);
            }
        }

        // Cut-out to allow wheel to come through
        move([109,30,-28]) cuboid([8,40,10], chamfer=1);
    }

    hull() {
        move([120.5,-12,-1.5]) {
            mount_profile_right(pointD);
            mount_profile_right(pointE);
        }

        move([120.5 - width,-12,-1.5]) {
            mount_profile_left(pointD);
            mount_profile_left(pointE);
        }
    }

    hull() {
        move([120.5,-12,-1.5]) {
            mount_profile_right(pointE);
            mount_profile_right(pointF);
        }

        move([120.5 - width,-12,-1.5]) {
            mount_profile_left(pointE);
            mount_profile_left(pointF);
        }
    }

    hull() {
        move([120.5,-12,-1.5]) {
            mount_profile_right(pointF);
            mount_profile_right(pointG);
        }

        move([120.5 - width,-12,-1.5]) {
            mount_profile_left(pointF);
            mount_profile_left(pointG);
        }
    }
}

module nema17_mount()
{
    move([3.5,0,0]) {
        difference() {
            // Faceplate
            move([0,0,0]) cuboid([7,46,46], chamfer=1, edges=EDGES_ALL-EDGES_LEFT);
            
            // Add NEMA 17 mount holes
            rotate([0,-90,0]) nema17_mount_holes(depth=8, l=0, $fn=60);

            // Recess the mount holes
            move([5.5 - 3,31/2,31/2]) xcyl(h=4,d=6);
            move([5.5 - 3,31/2,-31/2]) xcyl(h=4,d=6);
            move([5.5 - 3,-31/2,31/2]) xcyl(h=4,d=6);
            move([5.5 - 3,-31/2,-31/2]) xcyl(h=4,d=6);

            // Chamfer the edge around the shaft
            move([7,0,0]) rotate([0,-90,0]) cyl(h=10,d=25, chamfer2=2, $fn=60);
        }
        
        // Lip to align stepper motor to mount holes
        difference() {
            move([-(7/2) - 2.5,0,0]) cuboid([5,46,46], chamfer=1, edges=EDGES_X_ALL);
            move([-(7/2) - 2.5,0,0]) cuboid([6,43,43]);
        }
    }
}

module complete_mount()
{
    move([98,64-34,-6]) nema17_motor();
    move([107,64-34,-6]) wheel();
    move([98,64-34,-6]) nema17_mount();
    motor_bay();
}

module render_motor_mounts(crend, toPrint)
{
    // Render the rotational axis to assist with the design
    //move([0,64 - 34,-6]) xcyl(h=255,d=2);

    // Render the turning circle
    //move([0,64-34,-33.5]) tube(h=1,od=226, id=226-3);
    //move([0,64-34,-33.5]) tube(h=1,od=280, id=280-3);

    complete_mount();
    xflip() complete_mount();
}