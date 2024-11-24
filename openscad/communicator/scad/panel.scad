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

module panel_front(depth,width) // front
{
    difference() {
        move([-(depth/2) + 2,0,16]) cuboid([2,width-11,26], fillet=1, edges=EDGES_X_ALL);
        ircover_mask(depth, width);
    }
}

module panel_mask_front(depth,width)
{
    move([-(depth/2)+2,0,16]) cuboid([2.25,width-11.25,26]); // Left
}

module panel_back(depth,width) // back
{
    move([+(depth/2)-2,0,16]) cuboid([2,width-11,26], fillet=1, edges=EDGES_X_ALL);
}

module panel_mask_back(depth,width)
{
    move([+(depth/2)-2,0,16]) cuboid([2.25,width - 11.25,26]); // Right
}

module panel_left(depth,width) // left
{
    move([0,(width/2)-2,16]) cuboid([depth-11,2,26], fillet=1, edges=EDGES_Y_ALL);
}

module panel_mask_left(depth,width)
{
    move([0,(width/2)-2,16]) cuboid([depth-11,2.25,26]);
}

module panel_right(depth,width) // right
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
        move([-16,0,39]) yrot(90) panel_back(80,122);
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