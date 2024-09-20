/************************************************************************

    head.scad
    
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

include <screws.scad>

module head_lip_profile(loc1, loc2)
{
    hull() {
        move(loc1) {
            move([0,0,-5]) cyl(h=10,d=3);
        }

        move(loc2) {
            move([0,0,-5]) cyl(h=10,d=3);
        }
    }
}

module head_profile(loc)
{
    move(loc) {
        move([0,0,-1.5]) cyl(h=3,d=2, chamfer2=1);
    }
}

module head_base_profile(loc)
{
    move(loc) {
        move([0,0,-1.5]) cyl(h=3,d=3);
    }
}

module head_shape()
{
    pointA = [0,-50,0];
    pointB = [20,-50,0];
    pointC = [20,-121.5,0];
    pointD = [0.5,-143,0];
    pointJ = [0,-143,0];

    pointE = [0,-54,18];
    pointF = [9.5,-54,18];
    pointG = [9.5,-122,18];
    pointH = [0.5,-143 + 11,18];
    pointI = [0,-143 + 11,18];

    // Base of head
    head_lip_profile(pointA, pointB);
    head_lip_profile(pointB, pointC);
    head_lip_profile(pointC, pointD);
    head_lip_profile(pointD, pointJ);

    // Top of head
    hull() {
        head_profile(pointE);
        head_profile(pointF);
        head_profile(pointG);
        head_profile(pointH);
        head_profile(pointI);
    }

    // Side of head
    hull() {
        head_profile(pointF);
        head_profile(pointG);
        head_base_profile(pointB);
        head_base_profile(pointC);
    }

    // Front of head
    hull() {
        head_profile(pointG);
        head_profile(pointH);
        head_profile(pointI);
        head_base_profile(pointC);
        head_base_profile(pointD);
        head_base_profile(pointJ);
    }

    // Back of head
    hull() {
        head_profile(pointE);
        head_profile(pointF);
        head_base_profile(pointA);
        head_base_profile(pointB);
    }

    // Add a platform for the threaded inserts
    hull() {
        move([13.25,-60,0.25]) cuboid([10.5,17,0.5]);
        move([9.5,-61,15]) cuboid([3,16,0.5]);
    } 
}

module half_head()
{
    difference() {
        union() {
            head_shape();

            // Front threaded insert
            difference() {
                hull() {
                    move([0,-133,3]) xrot(180) cyl(h=12,d=8);
                    move([0,-133+2,14]) xrot(180) cuboid([5,2,2]);
                    move([0,-138,-2]) xrot(180) cuboid([7,6,2]);
                }

                // Threaded insert slot
                move([0,-133,-7 +6]) xrot(180) cyl(h=8,d=4);
                move([0,-133,-7 +6]) xrot(180) cyl(h=10,d=3);

                // Slice half
                move([-5.5,-133,5]) cuboid([10,17,20]);

                // Space for LED holder
                move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) xcyl(h=7,d=11);

            }

            // Standoff tab
            move([0,-121.25,15]) cuboid([2,4,2], chamfer=0.5, edges=EDGES_X_BOT);
        }

        // Slot for shell screw guide
        move([0,-89,7 +4.5]) cyl(h=10, d=11);

        // Eye socket (7mm for LED with grommet)
        move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) xcyl(h=16,d=7);
        
        // Back access
        move([0,-50,6]) cuboid([16,20,18]);

        // Body mounting
        move([0,-51.5,-6]) cuboid([50,40,12],chamfer=1);

        // Round off the top lower edge
        move([0,-67.5,-12]) xrot(45) cuboid([50,10,10]);

        // Threaded insert slot
        move([12,-58,-4 + 6]) xrot(180) cyl(h=8,d=4);
        move([12,-58,-4 + 6]) xrot(180) cyl(h=10,d=3);

        // Shell mounting screw hole
        move([0,-89,20]) cyl(h=20, d=3.5);
    }
    
    // Eye PCB mounting threaded insert
    difference() {
        move([0,-107,12.75]) xrot(180) cyl(h=6,d=8);
        move([0,-107,12.75 - 1]) xrot(180) cyl(h=8,d=4);
    }
}

module head_shell_screw_guide()
{
    // Screw guide for shell mounting hole
    difference() {
        move([0,-89,6.75]) cyl(h=19.5, d=11);
        move([0,-89,7]) cyl(h=26, d=8);
    }
}

module head()
{
    half_head();
    xflip() half_head();
}

module render_head(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            head();
        }
    } else {
        xrot(180) move([0,90,-18]) {
            head();
        }
    }
}

module render_head_shell_screw_guide(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            head_shell_screw_guide();
        }
    } else {
        xrot(180) move([0,90,-16.5]) {
            head_shell_screw_guide();
        }
    }
}

module head_screws()
{
    move([12,-58,-7]) xrot(180) m3x10_screw();
    move([-12,-58,-7]) xrot(180) m3x10_screw();

    move([0,-133,-7]) xrot(180) m3x10_screw();
}

module render_head_screws(toPrint)
{
    if (!toPrint) {
        head_screws();
    }
}