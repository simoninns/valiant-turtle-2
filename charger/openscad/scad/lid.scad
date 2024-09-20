/************************************************************************

    lid.scad
    
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
include <battery_cutout.scad>

module charger_lid()
{
    move([0,0,47.5]) {
        difference() {
            move([0,-2,0]) cuboid([110,78,3], chamfer=1, edges=EDGES_TOP+EDGES_Z_ALL);
            move([0,-12 + 8,0]) xrot(180) battery_access_hole_top();

            //move([-1.5,0,0]) cuboid([50,100,10]);

            // Screw head recess
            move([+((110/2) - 4),+((74/2) - 4),3 - 2]) cyl(h=3, d=6);
            move([+((110/2) - 4),-((78/2) - 2),3 - 2]) cyl(h=3, d=6);
            move([-((110/2) - 4),+((74/2) - 4),3 - 2]) cyl(h=3, d=6);
            move([-((110/2) - 4),-((78/2) - 2),3 - 2]) cyl(h=3, d=6);

            // Screw holes
            move([+((110/2) - 4),+((74/2) - 4),3 - 3]) cyl(h=6, d=3.25);
            move([+((110/2) - 4),-((78/2) - 2),3 - 3]) cyl(h=6, d=3.25);
            move([-((110/2) - 4),+((74/2) - 4),3 - 3]) cyl(h=6, d=3.25);
            move([-((110/2) - 4),-((78/2) - 2),3 - 3]) cyl(h=6, d=3.25);

            // Light pipes recess
            move([27,-34,1.25]) cuboid([3.25,3.25,2]);
            move([27 -3.75,-34,1.25]) cuboid([3.25,3.25,2]);

            // Light pipes hole
            move([26.5,-34,0]) cuboid([2.25,3.25,6]);
            move([23.75,-34,0]) cuboid([2.25,3.25,6]);
        }

        

        // Light pipe support
        difference() {
            move([26.125 - 1,-34,-7.5]) cuboid([8,5,14], chamfer=1, edges=EDGES_Z_ALL);
            move([26.125 - 1,-30.5,-7.5]) cuboid([8,4,17]);

            move([26.5,-33.75,-6]) cuboid([2.25,3.75,20]);
            move([26.5-2.75,-33.75,-6]) cuboid([2.25,3.75,20]);
        }
    }
}

module charger_lid_screws()
{
    move([0,0,48]) {
        move([+((110/2) - 4),+((74/2) - 4),0]) m3x10_screw();
        move([+((110/2) - 4),-((78/2) - 2),0]) m3x10_screw();
        move([-((110/2) - 4),+((74/2) - 4),0]) m3x10_screw();
        move([-((110/2) - 4),-((78/2) - 2),0]) m3x10_screw();
    }
}

module render_charger_lid(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) charger_lid();
    } else {
        move([0,0,49]) xrot(180) charger_lid();
    }
}

module render_charger_lid_screws(toPrint)
{
    if (!toPrint) {
        charger_lid_screws();
    }
}