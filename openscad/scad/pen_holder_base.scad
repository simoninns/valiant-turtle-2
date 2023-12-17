/************************************************************************

    pen_holder_base.scad
    
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
use <BOSL/threading.scad>

module holder_body()
{
    // Base of holder
    move([0,0,0]) cyl(h=16, d=19, center=false);

    // Main Shaft
    move([0,0,15.5]) cyl(h=23, d=15.5, center=false, chamfer=0.25); // main shaft

    move([0,0,38]) cyl(h=8, d=15.5, center=false, chamfer=0.25);
    move([0,0,46 - 1]) cyl(h=5, d=8, center=false, chamfer=0.25); // tip

    // Servo arm interface
    difference() {
        move([0,0,0]) cyl(h=9.5, d=29, center=false);

        // Remove some material to make it look nicer
        for(rota=[0: 360/15: 360]) { // for(variable = [start : increment : end])
            rotate([0,0,rota]) move([11.5,0,4.75]) cyl(h=12, d=3); // Top
        }
    }

    // Knurled top outer
    for(rota=[0: 360/60: 360]) { // for(variable = [start : increment : end])
        rotate([0,0,rota]) move([14.5,0,4.75]) cyl(h=9.5, d=1, chamfer2=0.25); // Top
    }
}

module inner_profile()
{
    // Tip
    hull() {
        move([0,0,17]) cyl(h=51, d=12);
        move([0,0,44.5]) cyl(h=2, d=6);
    }

    // Mid section
    move([0,0,21 - 2]) cyl(h=70, d=6);
    hull() {
        move([0,0,4]) cyl(h=10, d=15.5);
        move([0,0,10+5.5]) cyl(h=1, d=12);
    }
}

module render_pen_holder_base(crend, toPrint)
{
    if (!toPrint) {
        color([0.8,0.8,0.8]) {
            move([0,29,16+7]) xrot(180) difference() {
                holder_body();
                inner_profile();
                move([0,0,3]) trapezoidal_threaded_rod(d=16, l=7, pitch=1.2, thread_angle=30, internal=true, $fn=32);
            }
        }
    } else {
        difference() {
            holder_body();
            inner_profile();
            move([0,0,3]) trapezoidal_threaded_rod(d=16, l=7, pitch=1.2, thread_angle=30, internal=true, $fn=32);
        }
    }
}

// Render mock-up model of a fine-liner pen
// (Based on a Faber Castell Multimark 1523 permanent with the eraser removed)
module pen()
{
    color([0.4,0.4,0.4]) move([0,29,53]) {
        move([0,0,43]) cyl(h=6, d=9);
        cyl(h=80, d=10.5);
        move([0,0,-55]) cyl(h=30, d=8.5);
        move([0,0,-72.5]) cyl(h=5, d=6);

        move([0,0,-78.5]) cyl(h=7, d2=6, d1=4);

        move([0,0,-83]) cyl(h=2, d2=2, d1=1);
        move([0,0,-84.5]) cyl(h=5, d=0.75);
    }
}

module render_pen(crend, toPrint)
{
    if (!toPrint) pen();
}