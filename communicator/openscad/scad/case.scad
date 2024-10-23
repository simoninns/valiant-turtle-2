/************************************************************************

    case.scad
    
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

include <ircover.scad>
include <panel.scad>
include <label.scad>

// Basic chamfered shape for corners of the case (to be hull'ed together)
module case_edge()
{
    move([0,0,1]) cyl(h=2, d1=4, d2=8);
    move([0,0,9]) cyl(h=14, d=8);
}

// Note: These are designed to take M3 threaded inserts
// the original used clips
module pcb_peg()
{
    move([0,0,5]) {
        difference() {
            union() {
                move([0,0,0]) cyl(h=6, d=8);
                move([0,0,-2.5]) cyl(h=1, d1=10, d2=8);
            }
            move([0,0,7.5 - 6]) cyl(h=10, d=4);
        }
    }
}

// Marker to show where the feet should be attached
module foot_marker()
{
    difference() {
        move([0,0,0]) cuboid([13,13,1]);
        move([0,0,-1]) cuboid([11.5,11.5,3]);
    }
}

module case_common()
{
    difference() {
        hull() {
            move([+(105/2)-4,+(130/2)-4,0]) case_edge();
            move([-(105/2)+4,+(130/2)-4,0]) case_edge();
            move([+(105/2)-4,-(130/2)+4,0]) case_edge();
            move([-(105/2)+4,-(130/2)+4,0]) case_edge();
        }

        // Hollow the case with a 4mm wall
        hull() {
            move([+(105/2) - 8,+(130/2) - 8,10]) cyl(h=16, d=8);
            move([-(105/2) + 8,+(130/2) - 8,10]) cyl(h=16, d=8);
            move([+(105/2) - 8,-(130/2) + 8,10]) cyl(h=16, d=8);
            move([-(105/2) + 8,-(130/2) + 8,10]) cyl(h=16, d=8);
        }

        // Main panel cut-out
        move([0,17,11 + 5]) cuboid([83,130,22]); // Back
        move([0,-17,11 + 5]) cuboid([83,130,22]); // Front
        move([0,0,11 + 5]) cuboid([110,108,22]); // Sides

        // Panel slots
        panel_mask_left();
        panel_mask_right();
        panel_mask_back();
        panel_mask_front();
    }
    
    // Screw pillars back
    move([+(105/2) - 7,+(130/2) - 7,9]) cuboid([8,8,14], fillet=4, edges=EDGE_FR_LF+EDGE_BK_RT);
    move([-(105/2) + 7,+(130/2) - 7,9]) cuboid([8,8,14], fillet=4, edges=EDGE_FR_RT+EDGE_BK_LF);
    
    // Screw pillars front
    move([+(105/2) - 7,-(130/2) + 7,9]) cuboid([8,8,14], fillet=4, edges=EDGE_BK_LF);
    move([-(105/2) + 7,-(130/2) + 7,9]) cuboid([8,8,14], fillet=4, edges=EDGE_BK_RT);
}

module case_base()
{
    difference() {
        union() {
            case_common();
        }

        // Back M3 through-holes
        move([+(105/2) - 7,+(130/2) - 7,9]) cyl(h=22, d=6);
        move([-(105/2) + 7,+(130/2) - 7,9]) cyl(h=22, d=6);

        // Front M2 through-holes
        move([+(105/2) - 7,-(130/2) + 7,9]) cyl(h=22, d=6);
        move([-(105/2) + 7,-(130/2) + 7,9]) cyl(h=22, d=6);

        // Markers to show where the stick-on feet should be placed
        move([0,0,-0.25]) {
            move([+42,+48,0]) foot_marker();
            move([-42,+48,0]) foot_marker();
            move([+42,-48,0]) foot_marker();
            move([-42,-48,0]) foot_marker();
        }
    }

    move([0,0,13]) {
        difference() {
            union() {
                // Back M3 through-holes
                move([+(105/2) - 7,+(130/2) - 7,0.5]) cyl(h=5, d=7);
                move([-(105/2) + 7,+(130/2) - 7,0.5]) cyl(h=5, d=7);

                // Front M2 through-holes
                move([+(105/2) - 7,-(130/2) + 7,0.5]) cyl(h=5, d=7);
                move([-(105/2) + 7,-(130/2) + 7,0.5]) cyl(h=5, d=7);

                move([0,0,-1]) {
                    // Back M3 through-holes
                    move([+(105/2) - 7,+(130/2) - 7,0]) cyl(h=2, d1=8, d2=4);
                    move([-(105/2) + 7,+(130/2) - 7,0]) cyl(h=2, d1=8, d2=4);

                    // Front M2 through-holes
                    move([+(105/2) - 7,-(130/2) + 7,0]) cyl(h=2, d1=8, d2=4);
                    move([-(105/2) + 7,-(130/2) + 7,0]) cyl(h=2, d1=8, d2=4);
                }
            }

            move([0,0,-2]) {
                // Back M3 through-holes
                move([+(105/2) - 7,+(130/2) - 7,0]) cyl(h=2, d1=9.5, d2=3.5);
                move([-(105/2) + 7,+(130/2) - 7,0]) cyl(h=2, d1=9.5, d2=3.5);

                // Front M3 through-holes
                move([+(105/2) - 7,-(130/2) + 7,0]) cyl(h=2, d1=9.5, d2=3.5);
                move([-(105/2) + 7,-(130/2) + 7,0]) cyl(h=2, d1=9.5, d2=3.5);
            }

            // Back M3 screw holes
            move([+(105/2) - 7,+(130/2) - 7,0]) cyl(h=10, d=3.5);
            move([-(105/2) + 7,+(130/2) - 7,0]) cyl(h=10, d=3.5);

            // Front M3 screw holes
            move([+(105/2) - 7,-(130/2) + 7,0]) cyl(h=10, d=3.5);
            move([-(105/2) + 7,-(130/2) + 7,0]) cyl(h=10, d=3.5);
        }
    }

    // PCB pegs
    move([0,-24.5 + 12,0]) {
        move([+(65/2),+(75/2),0]) pcb_peg();
        move([-(65/2),+(75/2),0]) pcb_peg();
        move([+(65/2),-(75/2),0]) pcb_peg();
        move([-(65/2),-(75/2),0]) pcb_peg();
    }
}

module case_top()
{
    move([0,0,31]) zflip() {
        difference() {
            case_common();

            move([0,0,21-6]) {
                // Back M3 insert holes
                move([+(105/2) - 7,+(130/2) - 7,0]) cyl(h=10, d=4);
                move([-(105/2) + 7,+(130/2) - 7,0]) cyl(h=10, d=4);

                // Front M3 insert holes
                move([+(105/2) - 7,-(130/2) + 7,0]) cyl(h=10, d=4);
                move([-(105/2) + 7,-(130/2) + 7,0]) cyl(h=10, d=4);
            }

            move([0,0,21-14]) {
                // Back screw clearance holes
                move([+(105/2) - 7,+(130/2) - 7,0]) cyl(h=10, d=3.25);
                move([-(105/2) + 7,+(130/2) - 7,0]) cyl(h=10, d=3.25);

                // Front screw clearance holes
                move([+(105/2) - 7,-(130/2) + 7,0]) cyl(h=10, d=3.25);
                move([-(105/2) + 7,-(130/2) + 7,0]) cyl(h=10, d=3.25);
            }
        
            // Label mounting
            label_mask();
        }
    }
}

// M3x10mm DIN912 head screw (hex bolt)
module m3x10_screw()
{
    // Generic quick screw render (the BOSL version was really slow)
    color([0.8, 0.8, 0.8]) difference() {
        union() {
            move([0,0,1]) cyl(h=3,d=5.5, chamfer2=0.125);
            move([0,0,-5.5]) cyl(h=10,d=3);
        }

        move([0,0,2]) cyl(h=2,d=2.5, $fn=6);
    }
}

// M3x6mm DIN912 head screw (hex bolt)
module m3x6_screw()
{
    // Generic quick screw render (the BOSL version was really slow)
    color([0.8, 0.8, 0.8]) difference() {
        union() {
            move([0,0,1]) cyl(h=3,d=5.5, chamfer2=0.125);
            move([0,0,-3.5]) cyl(h=6,d=3);
        }

        move([0,0,2]) cyl(h=2,d=2.5, $fn=6);
    }
}

module case_screws()
{
    // Back M3 screw holes
    move([+(105/2) - 7,+(130/2) - 7,11]) xrot(180) m3x10_screw();
    move([-(105/2) + 7,+(130/2) - 7,11]) xrot(180) m3x10_screw();

    // Front M3 screw holes
    move([+(105/2) - 7,-(130/2) + 7,11]) xrot(180) m3x10_screw();
    move([-(105/2) + 7,-(130/2) + 7,11]) xrot(180) m3x10_screw();
}

module pcb_screws()
{
    // Standard PCB thickness is 1.6mm
    move([0,-24.5 + 12,8 + 1.6]) {
        move([+(65/2),+(75/2),0]) m3x6_screw();
        move([-(65/2),+(75/2),0]) m3x6_screw();
        move([+(65/2),-(75/2),0]) m3x6_screw();
        move([-(65/2),-(75/2),0]) m3x6_screw();
    }
}

module render_case_base(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) case_base();
    } else {
        case_base();
    }
}

module render_case_top(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) case_top();
    } else {
        zflip() move([0,0,-31]) case_top();
    }
}

module render_case_screws(toPrint)
{
    if (!toPrint) {
        case_screws();
    }
}

module render_pcb_screws(toPrint)
{
    if (!toPrint) {
        pcb_screws();
    }
}