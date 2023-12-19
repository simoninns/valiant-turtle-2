/************************************************************************

    head.scad
    
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

module head_lip_profile(loc1, loc2)
{
    hull() {
        move(loc1) {
            move([0,0,-5]) cyl(h=10,d=3);
        }

        move(loc2) {
            move([0,0,-5]) cyl(h=10,d=3);
        }
    }
}

module head_profile(loc)
{
    move(loc) {
        move([0,0,-1.5]) cyl(h=3,d=1);
    }
}

module head_base_profile(loc)
{
    move(loc) {
        move([0,0,-1.5]) cyl(h=3,d=3);
    }
}

module head_shape()
{
    pointA = [0,-50,0];
    pointB = [20,-50,0];
    pointC = [20,-122,0];
    pointD = [0,-143,0];

    pointE = [0,-54,18];
    pointF = [10,-54,18];
    pointG = [10,-122,18];
    pointH = [0,-143 + 10,18];

    // Base of head
    head_lip_profile(pointA, pointB);
    head_lip_profile(pointB, pointC);
    head_lip_profile(pointC, pointD);

    // Top of head
    hull() {
        head_profile(pointE);
        head_profile(pointF);
        head_profile(pointG);
        head_profile(pointH);
    }

    // Side of head
    hull() {
        head_profile(pointF);
        head_profile(pointG);
        head_base_profile(pointB);
        head_base_profile(pointC);
    }

    // Front of head
    hull() {
        head_profile(pointG);
        head_profile(pointH);
        head_base_profile(pointC);
        head_base_profile(pointD);
    }

    // Back of head
    hull() {
        head_profile(pointE);
        head_profile(pointF);
        head_base_profile(pointA);
        head_base_profile(pointB);
    }

    // Add a platform for the threaded inserts
    hull() {
        move([13.25,-60,0.25]) cuboid([10.5,17,0.5]);
        move([9.5,-61,15]) cuboid([3,16,0.5]);
    } 
}

module ball_bearing(diameter)
{
    staggered_sphere(d=diameter, circum=true, $fn=60);
}

module caster_ball_top()
{
    difference() { 
        hull() {
            difference() {
                move([0,0,32.5]) cyl(h=2,d=24);
                move([0,-10,32]) cuboid([20,10,4]);
                move([16,0,32]) cuboid([10,20,5]);
                move([-16,0,32]) cuboid([10,20,5]);
            }
            move([0,0,0]) cyl(h=14,d=24);
        }
        move([0,0,-4.5]) ball_bearing(20.5);
    }
}

module half_head()
{
    difference() {
        head_shape();

        // Eye socket (8mm for LED with grommet)
        move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) xcyl(h=16,d=7);

        // Back access
        move([0,-50,6]) cuboid([16,20,18]);

        // Body mounting
        move([0,-51.5,-6]) cuboid([50,40,12],chamfer=1);

        // Round off the top lower edge
        move([0,-67.5,-12]) xrot(45) cuboid([50,10,10]);

        // Threaded insert slot
        move([12,-58,3.9]) xrot(180) cyl(h=8,d=5);

        // Shell mounting screw hole
        move([0,-89,20]) cyl(h=20, d=3.5);
    }
    
    // Threaded insert
    move([12,-58,0]) xrot(180) insertM3x57();    
}

module head()
{
    half_head();
    xflip() half_head();
}

module display_ball_bearing()
{
    move([0,-144 + 35,3.5 - 22]) {
        move([0,0,-4.5]) color([0.7,0.7,0.7,1]) ball_bearing(20);
    }
}

module render_head(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            head();

            // Caster
            move([0,-144 + 35,3.5 - 22]) {
                caster_ball_top();
            }
        }
    } else {
        xrot(180) move([0,90,-18]) {
            head();

            // Caster
            move([0,-144 + 35,3.5 - 22]) {
                caster_ball_top();
            }
        }
    }
}

module render_ball_bearing(crend, toPrint)
{
    if (!toPrint) {
        display_ball_bearing();
    }
}

module head_screws()
{
    move([12,-58,-6]) xrot(180) m3x10_screw();
    move([-12,-58,-6]) xrot(180) m3x10_screw();
}

module render_head_screws(crend, toPrint)
{
    if (!toPrint) {
        head_screws();
    }
}