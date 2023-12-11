/************************************************************************

    head_cover.scad
    
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

module head_cover_half()
{
    pointA = [0,-52.5,0];
    pointB = [17.5,-52.5,0];
    pointC = [17.5,-121,0];
    pointD = [0,-139.5,0];

    difference() {
        move([0,0,-4]) hull() {
            move(pointA) cyl(h=2, d=1);
            move(pointB) cyl(h=2, d=1);
            move(pointC) cyl(h=2, d=1);
            move(pointD) cyl(h=2, d=1);
        }

        // Body mount screw hole
        move([12,-58,-4]) xrot(180) cyl(h=8,d=3.5);
    }
}

module head_cover()
{
    difference() {
        union() {
            head_cover_half();
            xflip() head_cover_half();
        }

        move([0,-109,-6]) cyl(h=10,d=25);
        move([0,-89,6.5 - 2]) cyl(h=21, d=7);
    }

    // Shell mounting screw hole
    difference() {
        move([0,-89,6.5]) cyl(h=21, d=9);
        move([0,-89,6.5 - 2]) cyl(h=21, d=7);
        move([0,-89,00]) cyl(h=80, d=3.5);
    }
}

module render_head_cover(crend, toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) head_cover();
    } else {
        move([0,89,5]) head_cover();
    }
}