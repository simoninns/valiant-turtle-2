/************************************************************************

    label.scad
    
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

include <logotype.scad>

module label()
{
    difference() {
        move([0,0,-0.5]) cuboid([37,50,1], fillet=1, edges=EDGES_Z_ALL);
        move([0,0,31]) zflip() logotype();
    }

    // Clips
    move([0,+19.5,0.5]) cuboid([30-8,2,3]);
    move([0,+19.5 - 1,1.5]) xrot(360/12) xcyl(h=30-8,d=1, $fn=6);
    move([0,-19.5,0.5]) cuboid([30-8,2,3]);
    move([0,-19.5 + 1,1.5]) xrot(360/12) xcyl(h=30-8,d=1, $fn=6);

}

module label_mask()
{
    move([0,+20,1]) cuboid([30-8,3,4]);
    move([0,+18.5,3]) cuboid([30-8,3,4]);

    move([0,-20,1]) cuboid([30-8,3,4]);
    move([0,-18.5,3]) cuboid([30-8,3,4]);
}

module render_label(toPrint)
{
    if (!toPrint) {
        color([0.2, 0.2, 0.2]) move([0,0,32]) zflip() label();
    } else {
        move([0,0,1]) label();
    }
}