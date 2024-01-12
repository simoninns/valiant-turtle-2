/************************************************************************

    pcb.scad
    
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

module pcb_mount_front()
{
    difference() {
        cyl(h=50, d=8, $fn=6);

        // Threaded insert slots
        move([0,0,19.1]) xrot(180) cyl(h=12,d=5);
        move([0,0,-19.1]) xrot(180) cyl(h=12,d=5);
    }

    move([0,0,25]) insertM3x57_th();
    move([0,0,-25]) xrot(180) insertM3x57_th();
}

module pcb_mount_back()
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
        move([0,0,19.1]) xrot(180) cyl(h=12,d=5);
        move([7,0,-19.1]) xrot(180) cyl(h=12,d=5);
        move([-7,0,-19.1]) xrot(180) cyl(h=12,d=5);
    }

    move([0,0,25]) insertM3x57_th();
    move([7,0,-25]) xrot(180) insertM3x57_th();
    move([-7,0,-25]) xrot(180) insertM3x57_th();
}

module pcb_mounts_front()
{
    move([0,0,25]) {
        move([60,-20,0]) pcb_mount_front();
        move([-60,-20,0]) pcb_mount_front();
    }
}

module pcb_mounts_back()
{
    move([0,0,25]) {
        move([0,52,0]) pcb_mount_back();
    }
}

module smPushButton()
{
    move([0,0,2.5]) {
        color([0.8,0.8,0.8]) cuboid([6.2, 6.2, 3.3], chamfer=0.5, edges=EDGES_ALL-EDGES_BOTTOM);
        move([0,0,2]) color([0.2,0.2,0.2]) cyl(h=1, d=3.5);
    }
}

module pcb_buttons()
{
    move([3+3.5,53 - 102,0]) smPushButton();
    move([-3-3.5,53 - 102,0]) smPushButton();
}

module pcb_oledDisplay()
{
    move([0,-30,1 + 3]) {
        difference() {
            color([0,0.3,0.8]) cuboid([28,28,1]); // PCB

            // Screw holes
            move([11.75,11.75,0]) cyl(h=4,d=2);
            move([-11.75,11.75,0]) cyl(h=4,d=2);
            move([11.75,-12.25,0]) cyl(h=4,d=2);
            move([-11.75,-12.25,0]) cyl(h=4,d=2);
        }

        // Screen
        move([0,1,1.5]) color([0.2,0.2,0.2]) cuboid([28,19,2]);
        move([0,3,2.75 - 0.125]) color([0.4,0.4,0.4]) cuboid([28,15,0.25]);
    }

    move([0,57 - 75,0]) {
        color([0.8,0.8,0.8]) { 
            move([-(2.54/2),0,0]) cyl(h=11,d=0.6, chamfer=0.2);
            move([(2.54/2),0,0]) cyl(h=11,d=0.6, chamfer=0.2);
            move([-(2.54) - (2.54/2) ,0,0]) cyl(h=11,d=0.6, chamfer=0.2);
            move([(2.54) + (2.54/2),0,0]) cyl(h=11,d=0.6, chamfer=0.2);
        }

        move([0,0,1.75]) color([0.2,0.2,0.2]) cuboid([10,2.5,2.5], chamfer=0.25, edges=EDGES_ALL-EDGES_TOP);
    }
}

module pcb_displayMount()
{
    move([0,37 - 71,0]) {
        // Display M2.5 Screw holes
        move([15,19.5,0]) cyl(h=4,d=2.5);
        move([-15,19.5,0]) cyl(h=4,d=2.5);
        move([15,-19.5,0]) cyl(h=4,d=2.5);
        move([-15,-19.5,0]) cyl(h=4,d=2.5);
    }

    // PCB header
    move([0,57 - 75,0]) {
        move([-(2.54/2),0,0]) cyl(h=4,d=1);
        move([(2.54/2),0,0]) cyl(h=4,d=1);
        move([-(2.54) - (2.54/2) ,0,0]) cyl(h=4,d=1);
        move([(2.54) + (2.54/2),0,0]) cyl(h=4,d=1);
    }
}

module pcb_complete()
{
    color([0,0.6,0,1]) difference() {
        pcb();
        pcb_penhole();
        pcb_screws();
        pcb_displayMount();
    }

    pcb_buttons();
    pcb_oledDisplay();
}

module pcb()
{
    zrot(-90) cyl(h=1.5, d=140, $fn=5);
}

module pcb_penhole()
{
    // Hole for pen
    move([0,29,20]) zcyl(h=80, d=14);
}

module pcb_screws()
{
     // M3 screw holes
    move([0,0,0]) {
        move([60,-20,0]) cyl(h=10, d=3.5);
        move([-60,-20,0]) cyl(h=10, d=3.5);
        move([0,52,0]) cyl(h=10, d=3.5);
    }
}

module render_pcb(toPrint)
{
    if (!toPrint) {
        difference() {
            move([0,0,50.75]) pcb_complete();
        }
    } else {
        // This will allow you to render and export a DXF file that
        // can be used as a KiCAD PCB outline...
        projection() {
            difference() {
                pcb();
                pcb_penhole();
                pcb_screws();
            }
        }
    }
}

module render_pcb_mounts_front(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) pcb_mounts_front();
    } else {
        xrot(90) move([0,3.5,0]) pcb_mount_front();
    }
}

module render_pcb_mounts_back(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) pcb_mounts_back();
    } else {
        xrot(90) move([0,3.5,0]) pcb_mount_back();
    }
}

module render_pcb_mounts_front_screws(toPrint)
{
    if (!toPrint) {
        move([60,-20,-3]) xrot(180) m3x10_screw();
        move([-60,-20,-3]) xrot(180) m3x10_screw();
    }
}

module render_pcb_mounts_back_screws(toPrint)
{
    if (!toPrint) {
        move([7,52,-3]) xrot(180) m3x10_screw();
        move([-7,52,-3]) xrot(180) m3x10_screw();
    }
}