/************************************************************************

    base.scad
    
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

// Other project includes
include <../../../robot/openscad/scad/body.scad>

// Local includes
include <screws.scad>

module charger_base()
{
    move([0,0,23]) {
        difference() {
            cuboid([110,80,46], chamfer=1, edges=EDGES_BOTTOM+EDGES_Z_ALL);
            move([0,0,2]) cuboid([110-4,80-4,46], chamfer=1, edges=EDGES_BOTTOM+EDGES_Z_ALL);
        }

        // Screw columns
        move([0,0,0]) difference() {
            union() {
                move([+((110/2) - 5),+((80/2) - 5),0]) cyl(h=46, d=8);
                move([+((110/2) - 5),-((80/2) - 5),0]) cyl(h=46, d=8);
                move([-((110/2) - 5),+((80/2) - 5),0]) cyl(h=46, d=8);
                move([-((110/2) - 5),-((80/2) - 5),0]) cyl(h=46, d=8);
            }

            move([+((110/2) - 5),+((80/2) - 5),0]) cyl(h=46, d=3);
            move([+((110/2) - 5),-((80/2) - 5),0]) cyl(h=46, d=3);
            move([-((110/2) - 5),+((80/2) - 5),0]) cyl(h=46, d=3);
            move([-((110/2) - 5),-((80/2) - 5),0]) cyl(h=46, d=3);

            // Threaded inserts
            move([0,0,27 - 6]) {
                move([+((110/2) - 5),+((80/2) - 5),0]) cyl(h=8, d=4);
                move([+((110/2) - 5),-((80/2) - 5),0]) cyl(h=8, d=4);
                move([-((110/2) - 5),+((80/2) - 5),0]) cyl(h=8, d=4);
                move([-((110/2) - 5),-((80/2) - 5),0]) cyl(h=8, d=4);
            }
        } 
    }
}

module charger_base_screws()
{

}

module render_charger_base(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) charger_base();
    } else {
        charger_base();
    }
}

module render_charger_base_screws(toPrint)
{
    if (!toPrint) {
        charger_base_screws();
    }
}