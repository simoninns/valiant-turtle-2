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

module motor_bay_shape()
{
    pointA = [0,0,-0.5];
    pointB = [0,0,-17];
    pointC = [0,30 - 10,-27];
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

    // Front panel
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
            mount_profile_right(pointB);
            mount_profile_right(pointC);
        }

        move([120.5 - width,pos,-1.5]) {
            mount_profile_left(pointB);
            mount_profile_left(pointC);
        }
    }

    // Base
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
        move([109,pos + 42,-28]) cuboid([8,40,10], chamfer=1);
    }

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
}

module motor_platform()
{
    difference() {
        union() {
            move([77,3,-21]) cuboid([38,10,14], chamfer=1, edges=EDGES_X_ALL); 
            move([77,55,-21]) cuboid([38,10,14], chamfer=1, edges=EDGES_X_ALL); 
        }

        // Threaded insert slot
        move([86,5-2,-17.9]) xrot(180) cyl(h=8,d=5);
        move([90-25,5-2,-17.9]) xrot(180) cyl(h=8,d=5);

        move([86,53 + 2,-17.9]) xrot(180) cyl(h=8,d=5);
        move([90-25,53 + 2,-17.9]) xrot(180) cyl(h=8,d=5);

        // Trim mounts
        move([77.5,0,-32]) xrot(60) cuboid([42,10,14]);
        move([77.5,60,-32]) xrot(-50) cuboid([42,10,14]); 
    }

    // Threaded inserts
    move([86,5-2,-14]) insertM3x57();
    move([90-25,5-2,-14]) insertM3x57();

    move([86,53 + 2,-14]) insertM3x57();
    move([90-25,53 + 2,-14]) insertM3x57();
}

module motor_bay()
{
    motor_bay_shape();
    motor_platform();
}

module render_motor_bay(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            motor_bay();
            xflip() motor_bay();
        }
    } else {
        xrot(180) {
            motor_bay();
            xflip() motor_bay();
        }
    }
}

// Support Enforcers
module render_motor_bay_se(crend, toPrint)
{
    if (toPrint) {
        move([+88,-27,20]) cuboid([65,80,40]);
        xflip() move([+88,-27,20]) cuboid([65,80,40]);
    }
}