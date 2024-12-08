/************************************************************************

    base.scad
    
    Valiant Turtle 2 - Battery Charger
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

// Local includes
include <screws.scad>
include <bullet_connector.scad>
include <battery_cutout.scad>

module usbc_hole()
{
    hull() {
        move([0,+(2.75+0.125),0]) xcyl(h=7,d=3.5);
        move([0,-(2.75+0.125),0]) xcyl(h=7,d=3.5);
    }
}

// Marker to show where the feet should be attached
module foot_marker()
{
    difference() {
        move([0,0,0]) cuboid([13,13,1]);
        move([0,0,-1]) cuboid([11.5,11.5,4]);
    }
}

module charger_base()
{
    move([0,0,33]) {
        // Main body
        difference() {
            union() {
                difference() {
                    move([0,-2,0 - 7]) cuboid([110,78,26 + 14], chamfer=1, edges=EDGES_BOTTOM+EDGES_Z_ALL);
                    move([0,-2,3 - 7]) cuboid([110-4,78-4,26 + 14], chamfer=1, edges=EDGES_BOTTOM+EDGES_Z_ALL);
                }

                // Guides to keep the battery sliding in straight
                move([52,26.5,1 - 7]) cuboid([6,7,24 + 14]);
                move([52,-9.5,1 - 7]) cuboid([6,7,24 + 14]);

                xflip() move([52,26.5,1 - 7]) cuboid([6,7,24 + 14]);
                xflip() move([52,-9.5,1 - 7]) cuboid([6,7,24 + 14]);
            }
            
            move([0,-12 + 8,+4.5]) xrot(180) battery_access_hole_bottom();
            move([54,-28,-0.5]) usbc_hole();
            
            // Remove material around USB-C connector and PCB
            move([48 + 1,-28,0]) cuboid([10,13,6], chamfer=1);
            move([48 + 1,-28,-2.5]) cuboid([10,20,4], chamfer=1);

            // Markers to show where the stick-on feet should be placed
            move([0,0,-27.25]) {
                move([+45, +27,0]) foot_marker();
                move([+45, -31,0]) foot_marker();
                move([-45, +27,0]) foot_marker();
                move([-45, -31,0]) foot_marker();
            }
        }

        // Interior wall on connector side
        difference() {
            move([0,-17,-7]) cuboid([108,2,26 + 14]);
            move([-23.5,-17.5,5]) cuboid([20.25,6,30]);
            
            // Clearance to all insertion of the M2.5 threaded insert
            move([18.25,-34.25 + 13.5,0]) cyl(h=30,d=8);
        }

        // Interior wall on back side
        move([0,34,-6]) cuboid([96,2,26 + 12]);

        // Screw columns
        move([0,0,1]) difference() {
            // Main screw columns
            union() {
                // Back right
                move([+((110/2) - 4),+((74/2) - 4),-7]) cyl(h=38, d=8);

                // Front right - Need to allow some PCB clearance
                hull() {
                    move([+((110/2) - 4),-((78/2) - 2),8]) cyl(h=8, d=8);
                    move([+((110/2) - 4) + 2,-((78/2) - 2) - 2,-2]) cyl(h=1, d=2);
                }
                
                // Back left
                move([-((110/2) - 4),+((74/2) - 4),-7]) cyl(h=38, d=8);

                // Front left
                move([-((110/2) - 4),-((78/2) - 2),-7]) cyl(h=38, d=8);
            }

            // Holes for screw shafts
            move([+((110/2) - 4),+((74/2) - 4),0]) cyl(h=28, d=3);
            move([+((110/2) - 4),-((78/2) - 2),9]) cyl(h=8, d=3);
            move([-((110/2) - 4),+((74/2) - 4),0]) cyl(h=28, d=3);
            move([-((110/2) - 4),-((78/2) - 2),0]) cyl(h=28, d=3);

            // Threaded inserts
            move([0,0,17 - 7]) {
                move([+((110/2) - 4),+((74/2) - 4),0]) cyl(h=8, d=4);
                move([+((110/2) - 4),-((78/2) - 2),0]) cyl(h=8, d=4);
                move([-((110/2) - 4),+((74/2) - 4),0]) cyl(h=8, d=4);
                move([-((110/2) - 4),-((78/2) - 2),0]) cyl(h=8, d=4);
            }
        } 

        // PCB mounting columns for M2.5 threaded inserts
        difference() {
            union() {
                move([18.25,-35,-7 - 7]) cyl(h=6+14,d=6);
                move([18.25,-34.25 + 13.5,-7 - 7]) cyl(h=6+14,d=6);

                hull() {
                    move([18.25,-35,-7 - 12]) cyl(h=6+7,d=6);
                    move([18.25,-34.25 + 13.5,-7 - 12]) cyl(h=6+7,d=6);
                }
            }

            move([18.25,-35,-7]) cyl(h=8,d=3.5);
            move([18.25,-34.25 + 13.5,-7]) cyl(h=8,d=3.5);

            move([18.25,-35,-10]) cyl(h=14,d=2.5);
            move([18.25,-34.25 + 13.5,-10]) cyl(h=14,d=2.5);
        }
    }
    
    // Connector support
    difference() {
        union() {
            connector_support();
            move([-23.5,-22,27 - 7]) cuboid([24,11,14 + 14], chamfer=1, edges=EDGES_Z_ALL);
        }
        move([-23.5,-22 + 1.75,18]) cuboid([24-7.5,11,32+4]);

        // Cable pass-through
        move([-23.5,-26.5,20]) {
            move([0,0,-1]) cuboid([6,4,22]);
            move([0,0,10]) yrot(45) cuboid([4.25,4.25,4.25]);
        }
    }
}

module connector_support()
{
    move([0,-12 + 8,46]) xrot(180) {
    difference() {
            move([-23.5,18,6]) cuboid([24,11,12], chamfer=1, edges=EDGES_Z_ALL);
            move([-23.5,15.5,5]) cuboid([20.25,12.25,20]);

            // Slots for connector
            move([-12,16.5,1.5]) cuboid([3,3.25,16]);
            move([-12 - 23,16.5,1.5]) cuboid([3,3.25,16]);
        }

        // Top stays
        move([-23.5,17.5,11]) {
            move([-9.25,0,0]) yrot(90) right_triangle([2, 10, 2], center=true);
            move([+9.25,0,0]) yrot(180) right_triangle([2, 10, 2], center=true);
        }
    }
}

module render_charger_base(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) charger_base();
    } else {
        move([0,0,-20 + 14]) charger_base();
    }
}

module render_charger_base_screws(toPrint)
{
    if (!toPrint) {
        charger_base_screws();
    }
}