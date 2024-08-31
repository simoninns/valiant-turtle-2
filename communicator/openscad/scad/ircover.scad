/************************************************************************

    ircover.scad
    
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

module ircover()
{
    move([0,-(130/2) + 2.51,(25/2) + 5 - 1.5]) cuboid([50,1,20]);
}

module ircover_mask()
{
    move([0,-(130/2) + 2.5,(25/2) + 5 - 1.5]) cuboid([51,2,21]);
    move([0,-(130/2) + 1,(25/2) + 5 - 1.5]) cuboid([50-4,5,20-4], fillet=1, edges=EDGES_Y_ALL);
}

module render_ircover(toPrint)
{
    if (!toPrint) {
        color([1,0,0]) ircover();
    } else {
        // Not printable - needs to be 1mm clear/red acrylic
    }
}