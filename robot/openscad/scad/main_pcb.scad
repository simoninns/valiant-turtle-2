/************************************************************************

    main_pcb.scad
    
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

module main_pcb_mount_front()
{
    difference() {
        cyl(h=50, d=8, $fn=6);

        // Threaded insert slots
        move([0,0,29 - 6]) xrot(180) cyl(h=8,d=4);
        move([0,0,-29 + 6]) xrot(180) cyl(h=8,d=4);
        move([0,0,0]) xrot(180) cyl(h=60,d=3);
    }
}

module main_pcb_mount_back()
{
    difference() {
        union() {
            cyl(h=50, d=8, $fn=6);
            
            hull() {
                move([0,0,-17]) cyl(h=16, d=8, $fn=6);
                move([7,0,-18.5]) cyl(h=13, d=8, $fn=6);
                move([-7,0,-18.5]) cyl(h=13, d=8, $fn=6);
            }
        }

        // Threaded insert slots
        move([0,0,29 - 6]) xrot(180) cyl(h=8,d=4);
        move([7,0,-29 + 6]) xrot(180) cyl(h=8,d=4);
        move([-7,0,-29 + 6]) xrot(180) cyl(h=8,d=4);

        move([0,0,29 - 9]) xrot(180) cyl(h=16,d=3);
        move([7,0,-29 + 9]) xrot(180) cyl(h=16,d=3);
        move([-7,0,-29 + 9]) xrot(180) cyl(h=16,d=3);
    }
}

module main_pcb_mounts_front()
{
    move([0,0,25]) {
        move([60,-20,0]) main_pcb_mount_front();
        move([-60,-20,0]) main_pcb_mount_front();
    }
}

module main_pcb_mounts_back()
{
    move([0,0,25]) {
        move([0,52,0]) main_pcb_mount_back();
    }
}

module main_pcb_complete()
{
    color([0,0.6,0,1]) difference() {
        main_pcb();
        main_pcb_penhole();
        main_pcb_screws();
        main_pcb_aux_screws();
    }
}

module main_pcb()
{
    zrot(-90) cyl(h=1.5, d=140, $fn=5);
}

module main_pcb_penhole()
{
    // Hole for pen
    move([0,29,20]) zcyl(h=80, d=14);
}

// Washer to protect PCB from metal screw head
module main_pcb_screw_washer()
{
    difference() {
        union() {
            move([0,0,-0.5]) cyl(h=3,d=8);
            move([0,0,1.5]) cyl(h=1,d1=8, d2=7);
        }
        move([0,0,1]) cyl(h=4,d=5.5);
        move([0,0,0]) cyl(h=6,d=3.5);
    }
}

module main_pcb_screws()
{
     // M3 screw holes
    move([0,0,0]) {
        move([60,-20,0]) cyl(h=10, d=3.5);
        move([-60,-20,0]) cyl(h=10, d=3.5);
        move([0,52,0]) cyl(h=10, d=3.5);
    }
}

// Screw holes for the aux board
module main_pcb_aux_screws()
{
    move([0,-23,0]) {
        move([+(50/2),+(45/2),0]) cyl(h=10, d=3.5);
        move([-(50/2),+(45/2),0]) cyl(h=10, d=3.5);
        move([+(50/2),-(45/2),0]) cyl(h=10, d=3.5);
        move([-(50/2),-(45/2),0]) cyl(h=10, d=3.5);
    }
}

module render_main_pcb(toPrint)
{
    if (!toPrint) {
        difference() {
            move([0,0,50.75]) main_pcb_complete();
        }
    } else {
        // This will allow you to render and export a DXF file that
        // can be used as a KiCAD PCB outline...
        projection() {
            difference() {
                main_pcb();
                main_pcb_penhole();
                main_pcb_screws();
                main_pcb_aux_screws();
            }
        }
    }
}

module render_main_pcb_mounts_front(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) main_pcb_mounts_front();
    } else {
        xrot(90) move([0,3.5,0]) main_pcb_mount_front();
    }
}

module render_main_pcb_mounts_back(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) main_pcb_mounts_back();
    } else {
        xrot(90) move([0,3.5,0]) main_pcb_mount_back();
    }
}

module render_main_pcb_mounts_front_screws(toPrint)
{
    if (!toPrint) {
        move([60,-20,-3]) xrot(180) m3x10_screw();
        move([-60,-20,-3]) xrot(180) m3x10_screw();

        move([60,-20,53]) m3x10_screw();
        move([-60,-20,53]) m3x10_screw();
    }
}

module render_main_pcb_mounts_back_screws(toPrint)
{
    if (!toPrint) {
        move([7,52,-3]) xrot(180) m3x10_screw();
        move([-7,52,-3]) xrot(180) m3x10_screw();

        move([0,52,53]) m3x10_screw();
    }
}

module render_main_pcb_screw_washer(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) {
            move([60,-20,53.5]) main_pcb_screw_washer();
            move([-60,-20,53.5]) main_pcb_screw_washer();
            move([0,52,53]) main_pcb_screw_washer();
        }
    } else {
        move([0,0,2]) main_pcb_screw_washer();
    }
}