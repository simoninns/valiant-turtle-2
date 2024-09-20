/************************************************************************

    battery_cutout.scad
    
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

module battery_access_hole_top()
{
    // Main body of battery
    move([0,-12.5,0]) cuboid([86,49,22], chamfer=1, edges=EDGES_Z_ALL);

    // Screw columns
    hull() {
        move([+45.5,5.5,-1.5]) cyl(h=12,d=8.25);
        move([-45.5,5.5,-1.5]) cyl(h=12,d=8.25);
    }
    hull() {
        move([+45.5,-5.5 - 25,-1.5]) cyl(h=12,d=8.25);
        move([-45.5,-5.5 - 25,-1.5]) cyl(h=12,d=8.25);
    }

    // Remove small tabs (as they will just break anyway)
    move([0,-12.5,0]) cuboid([96,30,22]);

    // Clip recesses
    move([0,-12.5,0]) cuboid([101,25,22]);

    // Power connector cut-out
    move([-23.5,15.5,0]) cuboid([20.25,12.25,12]);
}

module battery_access_hole_bottom()
{
    // Main body of battery
    move([0,-12.5,0]) cuboid([86,49,22], chamfer=1, edges=EDGES_Z_ALL);

    // Screw columns
    hull() {
        move([+45.5,5.5,-1.5]) cyl(h=12,d=8.5);
        move([-45.5,5.5,-1.5]) cyl(h=12,d=8.5);
    }
    hull() {
        move([+45.5,-5.5 - 25,-1.5]) cyl(h=12,d=8.5);
        move([-45.5,-5.5 - 25,-1.5]) cyl(h=12,d=8.5);
    }

    // Trim the edges for easier insertion
    move([0,-12.5,0]) cuboid([88,28,22]);
}