/************************************************************************

    battery.scad
    
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

// Non-printable parts ------------------------------------------------------------------

module battery18650_protected()
{
    // 18650 Battery with protection circuit
    difference() {
        cyl(h=69, d=18.5);
        move([0,0,(69/2)]) cyl(h=0.5, d=13);
        move([0,0,-(69/2)]) cyl(h=0.5, d=13);
    }
    
    move([0,0,(69/2)+0.25]) cyl(h=1, d=5);
}

module battery18650()
{
    // 18650 Battery without protection circuit
    difference() {
        cyl(h=65, d=18.5);
        move([0,0,(65/2)]) cyl(h=0.5, d=13);
        move([0,0,-(65/2)]) cyl(h=0.5, d=13);
    }
    
    move([0,0,(65/2)+0.25]) cyl(h=1, d=5);
}

module batteries()
{
    move([9.5,9.5,0]) battery18650_protected();
    move([-9.5,-9.5,0]) battery18650_protected();
    move([-9.5,9.5,0]) battery18650_protected();
    move([9.5,-9.5,0]) battery18650_protected();
}

// Printable parts ----------------------------------------------------------------------

module battery_pack_clip()
{
    move([41.5,0,-15]) { 
        difference() {
            union() {
                move([+7,0,+2.5]) cuboid([2, 12+6,35]);
                move([-7,0,-2.5]) cuboid([2, 12+6,35]);

                difference() {
                    move([0,0,20]) ycyl(h=12+6,d=16);
                    move([0,0,20]) ycyl(h=15+6,d=12);
                }
            }

            move([0,0,5]) cuboid([12,14+12,30]);
            move([-5,0,8]) cuboid([12,14+12,60]);
        }
        
        // Tabs
        move([10,0,-13]) cuboid([6,18,4], chamfer=1, edges=EDGES_Z_ALL+EDGES_RIGHT);

        // Side protectors
        difference() {
            union() {
                move([+4,8 + 3,+2.5]) {
                    cuboid([8, 2,35]);
                    move([-4,0,17.5]) ycyl(h=2,d=16);
                }
                move([+4,-8 - 3,+2.5]) {
                    cuboid([8, 2,35]);
                    move([-4,0,17.5]) ycyl(h=2,d=16);
                }
            }

            move([-6,0,24]) cuboid([10, 20+12,30]);
        }

        // Clip
        move([8,-9,5]) {
            difference() {
                right_triangle([3, 18, 3]);
                move([4,9,0]) cuboid([3.5,20,3]);
            }
        }
    }
}

module battery_pack()
{
    move([0,-12.5,10]) {
        difference() {
            union() {
                cuboid([86-0.5,49-0.5,60], chamfer=1, edges=EDGES_Z_ALL);
                move([0,0,-21.5]) cuboid([88,49-0.5,17], chamfer=1, edges=EDGES_Z_ALL);
            }
            cuboid([81,44,64], chamfer=1, edges=EDGES_Z_ALL);
        }

        battery_pack_clip();
        xflip() battery_pack_clip();
    }
}

module render_battery_pack(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) {
            battery_pack();
        }
    } else {
        move([0,13,20]) battery_pack();
    }
}

module render_batteries(toPrint)
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

module render_battery_screws(toPrint)
{
    if (!toPrint) {
        move([44.5,-19,-3]) xrot(180) m3x10_screw();
        move([-44.5,-19,-3]) xrot(180) m3x10_screw();
        move([0,5,-3]) xrot(180) m3x10_screw();
    }
}