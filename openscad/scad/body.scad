/************************************************************************

    body.scad
    
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

module body_profile(loc)
{
    move(loc) {
        move([0,0,3]) cyl(h=3,d=4,chamfer2=1);
    }
}

module rear_flipper(dpt)
{
    hull() {
        // Outer edge
        body_profile([120, 67.5 - 4, 0]);
        body_profile([120, 72.5, 0]);

        // Inner edge
        body_profile([74.5, 98, 0]);
        body_profile([53, 67.5 - 4, 0]);
    }
}

module front_flipper()
{
    hull() {
        // Flipper outer edge
        body_profile([120, -71.5, 0]);
        body_profile([120, -101, 0]);

        // Flipper front
        body_profile([74, -111.5, 0]);
        body_profile([15, -64, 0]);

        // Flipper back
        body_profile([54, -40, 0]);
    }
}

module head(dpt)
{
    hull() {
        move([0,119.5 - 210,0]) {
            cuboid([43,65,dpt]);
            move([0,-32.5,-(dpt/2)]) xrot(90) right_triangle([21.5,dpt,21.5]);
            yrot(180) move([0,-32.5,-(dpt/2)]) xrot(90) right_triangle([21.5,dpt,21.5]);
        }

        move([0,119.5 - 210,15]) {
            cuboid([22,65,20]);
            move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
            yrot(180) move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
        }
    }
}

module body_platform()
{
    move([0,0,-5]) {
        // Wheel platform
        hull() {
            // Back edge
            body_profile([120, 63.5, 0]);
            body_profile([-120,63.5,0]);

            // Left front
            body_profile([-73.5,-24.5,0]);
            body_profile([-120,-20,0]);

            // Right front
            body_profile([73.5,-24.5,0]);
            body_profile([120,-20,0]);
        }

        // Mid-body
        hull() {
            body_profile([-73.5,-24.5,0]);
            body_profile([73.5,-24.5,0]);
            body_profile([20,-64,0]);
            body_profile([-20,-64,0]);
        }

        // Front part of body/legs
        front_flipper(); // Left
        xflip() front_flipper();

        // // Rear part of body/legs
        rear_flipper(10); // Left
        xflip() rear_flipper(10); // Right

        // // Head
        //head(10);
    }
}

module wheel_cutouts()
{
    move([+90,25,-(4)]) cuboid([60,76,6*2], chamfer=2);
    move([-90,25,-(4)]) cuboid([60,76,6*2], chamfer=2);
}

module shell_mounts()
{
    // M3 screw holes back
    move([(97/2),65 - 9,-5]) zcyl(h=20, d=2.5);
    move([-(97/2),65 - 9,-5]) zcyl(h=20, d=2.5);

    // M3 screw hole front
    move([0,-90,15]) zcyl(h=20, d=2.5);
}

module render_body(crend, toPrint)
{
    difference() {
        body_platform();
        wheel_cutouts();
        // shell_mounts();
    }
    
}