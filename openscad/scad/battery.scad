/************************************************************************

    battery.scad
    
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

module battery18650()
{
    // 18650 Battery with protection circuit
    difference() {
        cyl(h=69, d=18.5);
        move([0,0,(69/2)]) cyl(h=0.5, d=13);
        move([0,0,-(69/2)]) cyl(h=0.5, d=13);
    }
    
    move([0,0,(69/2)+0.25]) cyl(h=1, d=5);
}

module batteries()
{
    move([9.5,9.5,0]) battery18650();
    move([-9.5,-9.5,0]) battery18650();
    move([-9.5,9.5,0]) battery18650();
    move([9.5,-9.5,0]) battery18650();
}

module battery_tab_slot(length)
{
    hull() {
        move([0,4.5,-(length/2)+1]) cuboid([1.5,1,4]);
        move([0,12.1,-(length/2)+1]) cuboid([2,1,4]);
    }

    hull() {
        move([0,4.5,(length/2)-1]) cuboid([1.5,1,4]);
        move([0,12.1,(length/2)-1]) cuboid([2,1,4]);
    }

    // Battery tab clearance
    move([0,6.5,(length/2)-2.25-0.125]) cuboid([7,9,0.75]);
    move([0,6.5,-(length/2)+2.25+0.125]) cuboid([7,9,0.75]);
}

module battery_tab_holder(length)
{
    move([0,4.75,(length/2)-2.5]) {
        difference() {
            move([0,2,0]) cuboid([9,10,2.5]);
            cuboid([5,14,3]);
            move([0,0,1]) cuboid([7,14,2.5]);

            move([0,7.5,0]) xrot(45) cuboid([10,9,3]);
        }
    }

    move([0,4.75,-(length/2)+2.5]) difference() {
        difference() {
            move([0,2,0]) cuboid([9,10,2.5]);
            cuboid([5,14,3]);
            move([0,0,-1]) cuboid([7,14,2.5]);

            move([0,7.5,0]) xrot(-45) cuboid([10,9,3]);
        }
    }
}

module battery18650_holder()
{
    length=83;

    difference() {
        union() {
            move([-21,-8 - 10,-(length/2)]) cuboid([42,40,length], chamfer=1, center=false, edges=EDGES_ALL-EDGES_FRONT);

            // Mounting lip
            hull() move([0,-17,0]) {
                move([0,-0.75,0]) cuboid([42+6,0.5, length+6], chamfer=1, edges=EDGES_Y_ALL);
                move([0,3,0]) cuboid([42,2, length], chamfer=1, edges=EDGES_Y_ALL);
            }

            // Screw mounts
            move([0,-13,44.5]) {
                hull() {
                    xrot(90) cyl(h=10,d=10, $fn=6);
                    move([0,12,-5]) cuboid([10,1,1]);
                }
            }
            
            move([0,-13,-44.5]) {
                hull() {
                    xrot(90) cyl(h=10,d=10, $fn=6);
                    move([0,12,5]) cuboid([10,1,1]);
                }
            }

            // Sticky-out bit to make it easier to remove batteries
            difference() {
                move([24,2,0]) cuboid([12,40,34],chamfer=1, edges=EDGES_ALL-EDGES_LEFT-EDGES_FRONT);
                move([22,-2,0]) cuboid([12,40+4,34-4],chamfer=1, edges=EDGES_ALL-EDGES_LEFT);
            }
        }
        move([0,-16,0]) cuboid([36,44,length-4],chamfer=0);

        // Threaded insert holes
        move([0,-15,44.5]) xrot(90) cyl(h=8,d=5);
        move([0,-15,-44.5]) xrot(90) cyl(h=8,d=5);

        // Lower battery area
        move([0,9.5,0]) {
            move([-9.5,0,0]) cyl(h=length-4, d=19.5);
            move([9.5,0,0]) cyl(h=length-4, d=19.5);

            // Centre clearance
            move([0,-1,0]) cuboid([10,18,length-4],chamfer=1);

            // Central cross-section
            move([20,-12,0]) cuboid([16,45,30],chamfer=1);

            // Base cut-out
            move([9.5,2,0]) cuboid([20-14,22,length-18], chamfer=1);
            move([0,2,0]) cuboid([20-14,22,length-18], chamfer=1);
            move([-9.5,2,0]) cuboid([20-14,22,length-18], chamfer=1);

            // Slots for battery tabs
            move([-9.5,0,0]) battery_tab_slot(length);
            move([9.5,0,0]) battery_tab_slot(length);
        }

        // Upper battery area
        move([0,-9.5,0]) {
            move([-9.5,0,0]) cyl(h=length-4, d=19.5);
            move([9.5,0,0]) cyl(h=length-4, d=19.5);

            // Slots for battery tabs
            move([-9.5,0,0]) battery_tab_slot(length);
            move([9.5,0,0]) battery_tab_slot(length);
        }
    }

    // Battery tab holders
    move([0,9.5 + 1,0]) {
        move([-9.5,0,0]) battery_tab_holder(length);
        move([9.5,0,0]) battery_tab_holder(length);
    }
    move([0,-9.5 + 1,0]) {
        move([-9.5,0,0]) battery_tab_holder(length);
        move([9.5,0,0]) battery_tab_holder(length);
    }

    // Threaded inserts for mounting
    move([0,-18,44.5]) xrot(90) insertM3x57_th();
    move([0,-18,-44.5]) xrot(90) insertM3x57_th();
}

module render_battery_holder(crend, toPrint)
{
    if (!toPrint) {
        color([0.4,0.4,0.5]) {
            move([0,-19,18]) {
                xrot(90) yrot(90) battery18650_holder();
            }
        }
    } else {
        move([0,0,21]) xrot(-90) battery18650_holder();
    }
}

module render_battery(crend, toPrint)
{
    if (!toPrint) {
        // 4 Batteries
        color([0.3,0.8,0.5]) {
            move([0,-19,19]) {
                xrot(90) yrot(90) batteries();
            }
        }
    }
}