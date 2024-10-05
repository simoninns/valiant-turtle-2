/************************************************************************

    aux_pcb.scad
    
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

// Screw holes for the aux board
module aux_screws()
{
    move([0,0,0]) {
        move([+(50/2),+(45/2),0]) cyl(h=10, d=3.5);
        move([-(50/2),+(45/2),0]) cyl(h=10, d=3.5);
        move([+(50/2),-(45/2),0]) cyl(h=10, d=3.5);
        move([-(50/2),-(45/2),0]) cyl(h=10, d=3.5);
    }
}

// The aux PCB is to allow easy additions to the turtle without
// having to redesign the main control board.
module aux_pcb() 
{
    move([0,-23,1.5+25]) {
        difference() {
             color([0.0,0.6,0.0,1]) move([0,5,0]) cuboid([55+10,50+20,1.5]);
            aux_screws();
        }
    }
}

module render_aux_pcb(toPrint)
{
    if (!toPrint) {
        difference() {
            move([0,0,50.75]) aux_pcb();
        }
    } else {
        // This will allow you to render and export a DXF file that
        // can be used as a KiCAD PCB outline...
        projection() {
            aux_pcb();
        }
    }
}