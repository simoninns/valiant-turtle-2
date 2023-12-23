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

module pen_servo_interface()
{
    move([10,0,3.75]) cuboid([10,8,7.5], chamfer=0.5);
}

module holder_body()
{
    // Base of holder
    move([0,0,0]) cyl(h=23, d=20, center=false, chamfer=0.5, $fn=8);

    // Main Shaft (pen hole is 16mm)
    difference() {
        move([0,0,22]) cyl(h=23, d=15.75, center=false, chamfer2=0.5, $fn=8);
        move([0,-12,26]) cuboid([10,10,40]);
    }
    move([0,-5,45]) cuboid([3,4,1], chamfer=0.5);

    // Tip
    move([0,0,46 - 1]) cyl(h=5, d=8, center=false, chamfer2=0.5, $fn=32);

    pen_servo_interface();
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

module pen_holder()
{
    difference() {
        holder_body();
        inner_profile();
        move([0,0,3]) trapezoidal_threaded_rod(d=16, l=7, pitch=1.2, thread_angle=30, internal=true, $fn=32);
    }
}

module render_pen_holder_base(crend, toPrint, penUp)
{
    if (!toPrint) {
        color([0.8,0.8,0.8]) {
            if(penUp) move([0,29,23+4]) xrot(180) pen_holder();
            else move([0,29,23]) xrot(180) pen_holder();
        }
    } else {
        pen_holder();
    }
}

// Render mock-up model of a fine-liner pen
// (Based on a Faber Castell Multimark 1523 permanent with the eraser removed)
module pen()
{
    // Make the tip of the pen 1mm over the wheel base to ensure
    // that it makes good contact with the surface
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

module render_pen(crend, toPrint, penUp)
{
    if (!toPrint) {
        if (penUp) move([0,0,4]) pen();
        else pen();
    }
}