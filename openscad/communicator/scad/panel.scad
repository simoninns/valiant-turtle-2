/************************************************************************

    panel.scad
    
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

module panel_front(depth,width)
{
    difference() {
        move([-(depth/2) + 2,0,16]) cuboid([2,width-11,26], fillet=1, edges=EDGES_X_ALL);
        ircover_mask(depth, width);
    }
}

module panel_mask_front(depth,width)
{
    move([-(depth/2)+2,0,16]) cuboid([2.25,width-11.25,26]);
}

module panel_back(depth,width)
{
    move([+(depth/2)-2,0,16]) {
        difference() {
            // Panel
            cuboid([2,width-11,26], fillet=1, edges=EDGES_X_ALL);

            // Parallel port cut out
            hull() {
                move([0,-45.5,-0.5]) xcyl(h=10, d=6);
                move([0,-12.25,-0.5]) xcyl(h=10, d=6);
            }

            move([0,-29,-0.5]) {
                hull() {
                    move([0,13,4]) xcyl(h=12, d=2);
                    move([0,-13,4]) xcyl(h=12, d=2);

                    move([0,11.75,-4]) xcyl(h=12, d=2);
                    move([0,-11.75,-4]) xcyl(h=12, d=2);
                }
            }

            // Serial port cut out
            hull() {
                move([0,45.5,-0.5]) xcyl(h=10, d=6);
                move([0,21,-0.5]) xcyl(h=10, d=6);
            }

            move([0,33.5,-0.5]) {
                hull() {
                    move([0,9,4]) xcyl(h=12, d=2);
                    move([0,-9,4]) xcyl(h=12, d=2);

                    move([0,7.5,-4]) xcyl(h=12, d=2);
                    move([0,-7.5,-4]) xcyl(h=12, d=2);
                }
            }
            
            // USB port cut out
            move([0,4.2,-4]) {
                hull() {
                    cuboid([10,8.5,2.5], fillet=1);
                    move([0,0,-1.5]) cuboid([10,7,2.5], fillet=1);
                }
            }

            // USB port recess
            move([5,4.2,-4.25]) {
                hull() {
                    move([0,0,2.5]) cuboid([10,8.25 + 6,2.5], chamfer=1, edges=EDGES_X_ALL+EDGES_LEFT);
                    move([0,0,-1 -2.5]) cuboid([10,8.25 + 6,2.5], chamfer=1, edges=EDGES_X_ALL+EDGES_LEFT);
                }
            }
        }
    }
}

module panel_mask_back(depth,width)
{
    move([+(depth/2)-2,0,16]) cuboid([2.25,width - 11.25,26]);
}

module panel_back_text(depth,width)
{
    move([+(depth/2)-1.6 + 0.6,-2.25,21.5]) {
        zrot(90) xrot(90) linear_extrude(0.8) {
            text("USB", size=4.5, font="Arial:style=Bold", $fn=100);
        }
    }

    move([+(depth/2)-1.6 + 0.6,-45,21.5]) {
        zrot(90) xrot(90) linear_extrude(0.8) {
            text("PARALLEL", size=4.5, font="Arial:style=Bold", $fn=100);
        }
    }

    move([+(depth/2)-1.6 + 0.6,22,21.5]) {
        zrot(90) xrot(90) linear_extrude(0.8) {
            text("SERIAL", size=4.5, font="Arial:style=Bold", $fn=100);
        }
    }
}

module panel_left(depth,width)
{
    move([0,(width/2)-2,16]) cuboid([depth-11,2,26], fillet=1, edges=EDGES_Y_ALL);
}

module panel_mask_left(depth,width)
{
    move([0,(width/2)-2,16]) cuboid([depth-11,2.25,26]);
}

module panel_right(depth,width)
{
    move([0,-(width/2)+2,16]) cuboid([depth-11,2,26], fillet=1, edges=EDGES_Y_ALL);
}

module panel_mask_right(depth,width)
{
    move([0,-(width/2)+2,16]) cuboid([depth-11,2.25,26]);
}

module render_panel_left(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2]) panel_left(80,122);
    } else {
        zrot(90) move([0,-16,60]) xrot(-90) panel_left(80,122);
    }
}

module render_panel_right(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2]) panel_right(80,122);
    } else {
        zrot(90) move([0,16,60]) xrot(90) panel_right(80,122);
    }
}

module render_panel_back(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2]) panel_back(80,122);
    } else {
        move([16,0,-37]) yrot(-90) panel_back(80,122);
    }
}

module render_panel_back_text(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.9]) panel_back_text(80,122);
    } else {
        move([16,0,-37]) yrot(-90) panel_back_text(80,122);
    }
}

module render_panel_front(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) panel_front(80,122);
    } else {
        move([16,0,39]) yrot(-90) panel_front(80,122);
    }
}