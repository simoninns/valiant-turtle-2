/************************************************************************

    pcb.scad
    
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

include <threaded_inserts.scad>

module pcb_mount_front()
{
    difference() {
        cyl(h=50, d=8, $fn=6);

        // Threaded insert slots
        move([0,0,21.1]) xrot(180) cyl(h=8,d=5);
        move([0,0,-21.1]) xrot(180) cyl(h=8,d=5);
    }

    move([0,0,25]) insertM3x57();
    move([0,0,-25]) xrot(180) insertM3x57();
}

module pcb_mount_back()
{
    difference() {
        union() {

            cyl(h=50, d=8, $fn=6);
            hull() {
            move([7,0,-19]) cyl(h=12, d=8, $fn=6);
            move([-7,0,-19]) cyl(h=12, d=8, $fn=6);
            }
        }

        // Threaded insert slots
        move([0,0,21.1]) xrot(180) cyl(h=8,d=5);
        move([7,0,-21.1]) xrot(180) cyl(h=8,d=5);
        move([-7,0,-21.1]) xrot(180) cyl(h=8,d=5);
    }

    move([0,0,25]) insertM3x57();
    move([7,0,-25]) xrot(180) insertM3x57();
    move([-7,0,-25]) xrot(180) insertM3x57();
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

module pcb()
{
    difference() {
        zrot(-90) cyl(h=1.5, d=140, $fn=5);

        // Hole for pen
        move([0,29,20]) zcyl(h=80, d=14);
    }
}

module render_pcb(crend, toPrint)
{
    if (!toPrint) {
        difference() {
            move([0,0,50.75]) color([0,0.6,0,1]) pcb();

            // M3 screw holes
            move([0,0,48]) {
                move([60,-20,0]) cyl(h=10, d=3.5);
                move([-60,-20,0]) cyl(h=10, d=3.5);
                move([0,52,0]) cyl(h=10, d=3.5);
            }
        }
    }
}

module render_pcb_mounts_front(crend, toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) pcb_mounts_front();
    } else {
        xrot(90) move([0,3.5,0]) pcb_mounts_front();
    }
}

module render_pcb_mounts_back(crend, toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) pcb_mounts_back();
    } else {
        xrot(90) move([0,3.5,0]) pcb_mounts_back();
    }
}