/************************************************************************

    panel.scad
    
    Valiant Turtle Communicator 2
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

include <ircover.scad>

module panel_left()
{
    move([-50.5,0,16]) cuboid([2,111,26], fillet=1, edges=EDGES_X_ALL); // Left
}

module panel_mask_left()
{
    move([-50.5,0,16]) cuboid([2.25,111.25,26]); // Left
}

module panel_right()
{
    move([50.5,0,16]) cuboid([2,111,26], fillet=1, edges=EDGES_X_ALL); // Right
}

module panel_mask_right()
{
    move([50.5,0,16]) cuboid([2.25,111.25,26]); // Right
}

module panel_back()
{
    move([0,64 - 1,16]) cuboid([86,2,26], fillet=1, edges=EDGES_Y_ALL); // Back
}

module panel_mask_back()
{
    move([0,64 - 1,16]) cuboid([86,2.25,26]); // Back
}

module panel_front()
{
    difference() {
        move([0,-(64 - 1),16]) cuboid([86,2,26], fillet=1, edges=EDGES_Y_ALL); // Front
        ircover_mask();
    }
}

module panel_mask_front()
{
    move([0,-(64 - 1),16]) cuboid([86,2.25,26]); // Front
}

module render_panel_left(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2]) panel_left();
    } else {
        move([16,0,51.5]) yrot(-90) panel_left();
    }
}

module render_panel_right(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2]) panel_right();
    } else {
        move([-16,0,51.5]) yrot(90) panel_right();
    }
}

module render_panel_back(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2]) panel_back();
    } else {
        zrot(90) move([0,-16,64]) xrot(-90) panel_back();
    }
}

module render_panel_front(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) panel_front();
    } else {
        zrot(90) move([0,16,64]) xrot(90) panel_front();
    }
}