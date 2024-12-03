/************************************************************************

    ircover.scad
    
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

module ircover(depth, width)
{
    move([-(depth/2)+2,0,(25/2) + 5 - 1.5]) cuboid([1,50,20]);
}

module ircover_mask(depth, width)
{
    move([-(depth/2)+2.5,0,0]) {
        move([0,0,(25/2) + 5 - 1.5]) cuboid([2,51,21]);
        move([-2,0,(25/2) + 5 - 1.5]) cuboid([5,50-4,20-4], fillet=1, edges=EDGES_X_ALL);
    }
}

module ircover_lock(depth, width)
{
    difference() {
        union() {
            move([-(depth/2)+3.25,0,(25/2) + 5 - 1.5]) cuboid([1.5,51,21]);
            move([-(depth/2)+3.5,0,(25/2) + 5 - 1.5]) cuboid([1,60,21]);
        }
        move([-(depth/2)+3.25,0,(25/2) + 5 - 1.5]) cuboid([5,50-2,20-2], fillet=1, edges=EDGES_X_ALL);
    }
}

module render_ircover(toPrint)
{
    if (!toPrint) {
        color([1,0,0]) ircover(80,122);
    } else {
        // Not printable - needs to be 1mm clear/red acrylic
    }
}

module render_ircover_lock(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) ircover_lock(80,122);
    } else {
        move([-16,0,-36]) yrot(90) ircover_lock(80,122);
    }
}