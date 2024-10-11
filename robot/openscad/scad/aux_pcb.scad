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

include <main_pcb.scad>

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

module aux_pcb_mount_pillar()
{
    difference() {
        // Pillar
        cyl(h=25, d=8);

        // Threaded insert slot
        move([0,0,12.5]) xrot(180) cyl(h=8,d=4);
        move([0,0,-12.5]) xrot(180) cyl(h=8,d=4);
        move([0,0,0]) xrot(180) cyl(h=28,d=3);
    }
}

module aux_pcb_mount()
{
    move([0,0,2.75]) {
        difference() {
            cuboid([50+2,45+2,4]);
            cuboid([50-2,45-2,8]);

            move([+(50/2),+(45/2),0]) cyl(h=25, d=8);
            move([-(50/2),+(45/2),0]) cyl(h=25, d=8);
            move([+(50/2),-(45/2),0]) cyl(h=25, d=8);
            move([-(50/2),-(45/2),0]) cyl(h=25, d=8);
        }
    }

    move([0,0,13.25]) {
        move([+(50/2),+(45/2),0]) aux_pcb_mount_pillar();
        move([-(50/2),+(45/2),0]) aux_pcb_mount_pillar();
        move([+(50/2),-(45/2),0]) aux_pcb_mount_pillar();
        move([-(50/2),-(45/2),0]) aux_pcb_mount_pillar();
    }
}

module aux_pcb_screw_washer()
{
    // Use the same part as the main PCB
    main_pcb_screw_washer();
}

module aux_pcb_screw_washers()
{
    move([0,0,0]) {
        move([+(50/2),+(45/2),0]) aux_pcb_screw_washer();
        move([-(50/2),+(45/2),0]) aux_pcb_screw_washer();
        move([+(50/2),-(45/2),0]) aux_pcb_screw_washer();
        move([-(50/2),-(45/2),0]) aux_pcb_screw_washer();
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

module render_aux_pcb_mount(toPrint)
{
    if (!toPrint) {
            move([0,-23,50.75]) color([0.2,0.2,0.2,1]) aux_pcb_mount();
    } else {
        move([0,0,-0.75]) aux_pcb_mount();
    }
}

module render_aux_pcb_screw_washer(toPrint)
{
    if (!toPrint) {
        move([0,-23,50.75]) color([0.2,0.2,0.2,1]) {
            move([0,0,29.25]) aux_pcb_screw_washers();
            zflip() move([0,0,2.75]) aux_pcb_screw_washers();
        }
    }
}

module render_aux_pcb_screws(toPrint)
{
    if (!toPrint) {
        // Top screws
        move([0,-23,79.5]) {
            move([+(50/2),+(45/2),0]) m3x10_screw();
            move([-(50/2),+(45/2),0]) m3x10_screw();
            move([+(50/2),-(45/2),0]) m3x10_screw();
            move([-(50/2),-(45/2),0]) m3x10_screw();
        }

        // Bottom screws
        move([0,-23,48.5]) {
            move([+(50/2),+(45/2),0]) xrot(180) m3x10_screw();
            move([-(50/2),+(45/2),0]) xrot(180) m3x10_screw();
            move([+(50/2),-(45/2),0]) xrot(180) m3x10_screw();
            move([-(50/2),-(45/2),0]) xrot(180) m3x10_screw();
        }
    }
}