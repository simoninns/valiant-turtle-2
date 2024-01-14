/************************************************************************

    display_mount.scad
    
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

module buttons()
{
    move([0,-15.75,4.25]) {
        difference() {
            xcyl(h=26,d=2.5, $fn=6);
            move([0,0,-1.5]) cuboid([28,3,1]);
            move([0,0,0.75]) cuboid([28,3,1]);
        }

        move([6.5,0,-0.125]) {
            cyl(h=1.75,d=7, chamfer2=0.5);
            move([0,0,3]) cyl(h=5,d=5, chamfer2=0.5);
        }

        move([-6.5,0,-0.125]) {
            cyl(h=1.75,d=7, chamfer2=0.5);
            move([0,0,3]) cyl(h=5,d=5, chamfer2=0.5);
        }
    }
}

module display_mount_base()
{
    difference() {
        union() {
            move([0,-1,0]) cuboid([36,45,2], chamfer=0.5, edges=EDGES_Z_ALL);

            // OLED M2 screw holes
            move([0,3,1.5]) {
                move([11.75,11.75,0]) cyl(h=1,d=4);
                move([-11.75,11.75,0]) cyl(h=1,d=4);
                move([11.75,-12.25,0]) cyl(h=1,d=4);
                move([-11.75,-12.25,0]) cyl(h=1,d=4);
            }

            move([0,3,3]) {
                move([11.75,11.75,0]) cyl(h=2.5,d=2, chamfer2=0.5);
                move([-11.75,11.75,0]) cyl(h=2.5,d=2, chamfer2=0.5);
                move([11.75,-12.25,0]) cyl(h=2.5,d=2, chamfer2=0.5);
                move([-11.75,-12.25,0]) cyl(h=2.5,d=2, chamfer2=0.5);
            }

            // Button holder
            move([0,-15.75,3]) cuboid([29,4,4], chamfer=0.5, edges=EDGES_ALL-EDGES_BOTTOM);
        }

        // PCB mounting M2.5 screw holes
        move([0,-1,0]) {
            move([15,19.5,0]) cyl(h=8,d=3);
            move([-15,19.5,0]) cyl(h=8,d=3);
            move([15,-19.5,0]) cyl(h=8,d=3);
            move([-15,-19.5,0]) cyl(h=8,d=3);
        }

        // Display connector recess
        move([0,15,0]) cuboid([11,3,8]);

        // Push buttons
        move([3+3.5,-16,0]) cuboid([6.5+3, 7, 12]);
        move([-3-3.5,-16,0]) cuboid([6.5+3, 7, 12]);

        // Save some plastic
        move([0,2.75,0]) cuboid([30,19,4]);
        move([0,-1,0]) cuboid([18,19,4]);

        // Button holder
        move([0,-15.75,4.25]) xcyl(h=27,d=2.75, $fn=6);
        move([0,-15.75,4]) cuboid([4,5,6]);
    }

    move([0,-15.75,1.75]) cuboid([3,5,2], chamfer=0.5, edges=EDGES_ALL-EDGES_BOTTOM);
}

module display_mount_top()
{
    move([0,-1,4]) {
        difference() {
            cuboid([36,45,6], chamfer=0.5, edges=EDGES_ALL-EDGES_BOTTOM);
            move([0,0,-1.75]) cuboid([36-4,45-4,5], chamfer=0.5, edges=EDGES_Z_ALL);

            move([6.5,-14.75,1]) cyl(h=6,d=5.25);
            move([-6.5,-14.75,1]) cyl(h=6,d=5.25);

            move([0,-14.75,0.5-1]) {
                cuboid([22,8,4]);
                cuboid([32,5,4]);
            }

            // Display opening
            move([0,6,0]) cuboid([27,15,8]);
            move([0,6,4]) cuboid([27+2,15+2,4], chamfer=1);

            // PCB mounting M2.5 screw holes
            move([0,0,0]) {
                move([15,19.5,0]) cyl(h=8,d=3);
                move([-15,19.5,0]) cyl(h=8,d=3);
                move([15,-19.5,0]) cyl(h=8,d=3);
                move([-15,-19.5,0]) cyl(h=8,d=3);
            }
        }

        move([0,0,-0.75]) {
            difference() {
                union() {
                    move([15,19.5,0]) cyl(h=4.5,d=6);
                    move([-15,19.5,0]) cyl(h=4.5,d=6);
                    move([15,-19.5,0]) cyl(h=4.5,d=6);
                    move([-15,-19.5,0]) cyl(h=4.5,d=6);
                }

                move([15,19.5,0]) cyl(h=8,d=3);
                move([-15,19.5,0]) cyl(h=8,d=3);
                move([15,-19.5,0]) cyl(h=8,d=3);
                move([-15,-19.5,0]) cyl(h=8,d=3);

                // Screen clearance
                move([0,16.5,-1.75]) cuboid([29, 4,5]);
            }
        }
    }
}

module render_display_mount(toPrint)
{
    if (!toPrint) {
        move([0,-33,52.5]) {
            color([0.9,0.9,0.6,1]) display_mount_base();
            color([0.9,0.9,0.6,1]) display_mount_top();
            color([0.9,0.9,0.6,1]) buttons();
        }
    } else {
        move([-20,0,1]) display_mount_base();
        move([-20,-18,-3.25]) buttons();
        move([20,-2,7]) xrot(180) display_mount_top();
    }
}