/************************************************************************

    head_cover.scad
    
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

module head_cover_half()
{
    pointA = [0,-52.5,0];
    pointB = [17.5,-52.5,0];
    pointC = [17.5,-121,0];
    pointD = [0,-139.5,0];

    difference() {
        move([0,0,-6]) hull() {
            move(pointA) cyl(h=6, d=1, chamfer1=0.5);
            move(pointB) cyl(h=6, d=1, chamfer1=0.5);
            move(pointC) cyl(h=6, d=1, chamfer1=0.5);
            move(pointD) cyl(h=6, d=1, chamfer1=0.5);
        }

        // Body mount screw holes
        move([12,-58,-4]) xrot(180) cyl(h=8,d=3.5);
        move([0,-133,-4]) xrot(180) cyl(h=8,d=3.5);

        // Screw head recess
        move([12,-58,-8.5]) xrot(180) cyl(h=4,d=7);
        move([0,-133,-8.5]) xrot(180) cyl(h=4,d=7);

        move([0,-144 + 35,3.5 - 22]) cyl(h=40, d=2.5); // Hole to release bearing through
    }
}

module bearing_mount()
{
    move([0,-144 + 35,3.5 - 22]) {
        difference() {        
            move([0,0,2]) cyl(h=18,d=24);
            move([0,0,-4.5]) ball_bearing(20.5);
            move([0,0,0]) cyl(h=40, d=2.5); // Hole to release bearing through
        }
    }
}

module head_cover()
{
    difference() {
        union() {
            head_cover_half();
            xflip() head_cover_half();
        }

        // Shell mount hole
        move([0,-89,6.5 - 4]) cyl(h=24, d=8);
        move([0,-89,-11]) cyl(h=8, d=10, chamfer=2);
    }

    bearing_mount();
}

module render_head_cover(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) head_cover();
    } else {
        move([0,-89,-3]) xrot(180) head_cover();
    }
}

module ball_bearing(diameter)
{
    staggered_sphere(d=diameter, circum=true, $fn=60);
}

module display_ball_bearing()
{
    move([0,-144 + 35,3.5 - 22]) {
        move([0,0,-4.5]) color([0.7,0.7,0.7,1]) ball_bearing(20);
    }
}

module render_ball_bearing(toPrint)
{
    if (!toPrint) {
        display_ball_bearing();
    }
}