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
include <bullet_connector.scad>

module charger_base()
{
    move([0,0,23]) {
        difference() {
            //cuboid([110,80,46], chamfer=1, edges=EDGES_BOTTOM+EDGES_Z_ALL);
            move([0,0,-22.5]) cuboid([110,80,3], chamfer=1, edges=EDGES_BOTTOM+EDGES_Z_ALL);
            move([0,0,2]) cuboid([110-4,80-4,46], chamfer=1, edges=EDGES_BOTTOM+EDGES_Z_ALL);

            // Test
            //move([0,30,0]) cuboid([110+2,80+2,46+2], chamfer=1, edges=EDGES_BOTTOM+EDGES_Z_ALL);
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

    connector_support();
    difference() {
        move([-23.5,-22,18]) cuboid([24,11,32], chamfer=1, edges=EDGES_Z_ALL);
        move([-23.5,-22 + 1.75,18]) cuboid([24-7.5,11,32+4]);

        // Cabel pass-through
        move([-23.5,-30,11]) {
            hull() {
                right_triangle([6, 10, 6]);
                xflip() right_triangle([6, 10, 6]);
                move([0,5,-5]) cuboid([12,10,10]);
            }
        }
    }

    
}

module connector_support()
{
    move([0,-12 + 8,46]) xrot(180) {
    difference() {
            move([-23.5,18,6]) cuboid([24,11,12], chamfer=1, edges=EDGES_Z_ALL);
            move([-23.5,15.5,5]) cuboid([20.25,12.25,20]);

            // Slots for connector
            move([-12,16.5,1.5]) cuboid([3,3.25,16]);
            move([-12 - 23,16.5,1.5]) cuboid([3,3.25,16]);
        }

        // Top stays
        move([-23.5,17.5,11]) {
            move([-9.25,0,0]) yrot(90) right_triangle([2, 10, 2], center=true);
            move([+9.25,0,0]) yrot(180) right_triangle([2, 10, 2], center=true);
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