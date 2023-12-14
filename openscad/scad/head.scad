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

    pointE = [0,-54,20];
    pointF = [10,-54,20];
    pointG = [10,-122,20];
    pointH = [0,-143 + 10,20];

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
        move([9.5,-61,17]) cuboid([3,16,0.5]);
    } 
}

module ball_bearing(diameter)
{
    staggered_sphere(d=diameter, circum=true, $fn=60);
}

module caster_ball_base()
{
    difference() { 
        union() {
            move([0,0,-7.5 + 1.5]) cyl(h=2 + 3,d=26, chamfer=0.5); // Lip
            move([0,0,-11.5]) cyl(h=3,d1=16, d2=24, chamfer1=0.5, center=false); // Ball chamfer
        }

        move([0,0,-4.5]) ball_bearing(20.5);
        caster_ball_top();
    }
}

module caster_ball_top()
{
    difference() { 
        hull() {
            difference() {
                move([0,0,34]) cyl(h=4,d=24);
                //move([0,0,34]) zrot(45) cuboid([20,20,4]);
                move([0,-10,34]) cuboid([20,10,4]);
                move([16,0,34]) cuboid([10,20,5]);
                move([-16,0,34]) cuboid([10,20,5]);
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
        move([-1,-122,3]) zrot(-45) yrot(-22) move([10,0,0]) xcyl(h=16,d=7);

        // Back access
        move([0,-50,8]) cuboid([16,20,18]);

        // Body mounting slot
        move([0,-51.5,-1.5]) cuboid([50,40,3]);

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

module render_caster_ball_base(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            move([0,-144 + 35,3.5 - 22]) {
                caster_ball_base();
            }
        }
    } else {
        xrot(180) move([0,0,3.5]) caster_ball_base();
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

        move([0,-144 + 35,3.5 - 22]) {
            move([0,0,-4.5]) color([0.7,0.7,0.7,1]) ball_bearing(20);
        }
    } else {
        xrot(180) move([0,90,-20]) {
            head();

            // Caster
            move([0,-144 + 35,3.5 - 22]) {
                caster_ball_top();
            }
        }
    }
}