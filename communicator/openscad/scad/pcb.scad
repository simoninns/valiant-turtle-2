/************************************************************************

    pcb.scad
    
    Valiant Turtle Communicator 2
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

include <holder.scad>

// Screw holes for the aux board
module pcb_screw_holes()
{
    move([0,10.25,0]) {
        move([+(65/2),+(75/2),0]) cyl(h=10, d=3.5);
        move([-(65/2),+(75/2),0]) cyl(h=10, d=3.5);
        move([+(65/2),-(75/2),0]) cyl(h=10, d=3.5);
        move([-(65/2),-(75/2),0]) cyl(h=10, d=3.5);
    }
}

module pcb() 
{
    difference() {
        move([0,-23,8.75]) {
            color([0.0,0.6,0.0,1]) move([0,25,0]) cuboid([80,119,1.5]);
        }

        move([0,-23,8.75]) {
            pcb_screw_holes();
        }

        // Add holes for the LEDs
        move([0,-46,16]) xrot(90) {
            six_leds();
        }
    }
}

module render_pcb(toPrint)
{
    if (!toPrint) {
        difference() {
            move([0,0,0]) pcb();
        }
    } else {
        // This will allow you to render and export a DXF file that
        // can be used as a KiCAD PCB outline...
        projection() {
            pcb();
        }
    }
}