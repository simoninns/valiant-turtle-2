/************************************************************************

    toggle_switch.scad
    
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

include <threaded_inserts.scad>

module toggle_switch()
{
    color([0.8,0,0]) cuboid([13,6.5,9], chamfer=0.5); // Body

    color([0.8,0.8,0.8]) {
        move([0,0,0.5]) cuboid([9,7,8], chamfer=0.5); // Body
        move([0,0,4.251]) cuboid([13,6.75,0.5], chamfer=0.5, edges=EDGES_Z_ALL);
    }

    color([0.8,0.8,0.8]) move([0,0,9]) {
        difference() {
            cyl(h=9, d=6, chamfer2=0.5); // Outer shaft
            move([0,0,4]) cyl(h=4, d=4); // Outer shaft
        }
    }

    // Armature
    color([0.8,0.8,0.8]) move([0,0,12]) yrot(-20) {
        hull() {
            cyl(h=1, d=2.5); // Base
            move([0,0,9]) staggered_sphere(d=3);
        }
    }

    // Terminals
    color([0.8,0.8,0.8]) move([0,0,-6.5]) {
        difference() {
            union() {
                move([-4,0,0]) cuboid([0.75, 2, 4]);
                move([0,0,0]) cuboid([0.75, 2, 4]);
                move([+4,0,0]) cuboid([0.75, 2, 4]);
            }

            hull() {
                move([0,0,0]) xcyl(h=20,d=1.5);
                move([0,0,-1]) xcyl(h=20,d=1.5);
            }
        }
    }

    // Nuts
    color([0.8,0.8,0.8]) move([0,0,5 + 6]) {
        difference() {
            cyl(h=1.5, d=8, $fn=6);
            cyl(h=2, d=6);
        }

        // Washer
        move([0,0,-1]) cyl(h=0.75, d=12);
    }
}

module render_toggle_switch(toPrint)
{
    if (!toPrint) {
        move([-23.5,37,9.5]) xrot(180) toggle_switch();
    }
}