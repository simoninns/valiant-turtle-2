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
    dpt=10;

    move([0,0,-5]) hull() {
        // move([0,119.5 - 210,0]) {
        //     cuboid([43,65,dpt]);
        //     move([0,-32.5,-(dpt/2)]) xrot(90) right_triangle([21.5,dpt,21.5]);
        //     yrot(180) move([0,-32.5,-(dpt/2)]) xrot(90) right_triangle([21.5,dpt,21.5]);
        // }

        // move([0,119.5 - 210,15]) {
        //     cuboid([22,65,20]);
        //     move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
        //     yrot(180) move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
        // }
    }

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
}

module head()
{
    difference() {
        head_shape();

        // Eye socket (6mm for LED with grommet)
        move([5,-122 - 5,8]) zrot(-45) xcyl(h=16,d=6);

        // Back access
        move([0,-50,8.51]) cuboid([18,20,20-3]);
    }
    
}

module render_head(crend, toPrint)
{
    head();
    xflip() head();
}