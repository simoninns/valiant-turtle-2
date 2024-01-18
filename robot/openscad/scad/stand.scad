/************************************************************************

    stand.scad
    
    Valiant Turtle 2
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

module sideStand()
{
    move([-47,0,0]) {
        difference() {
            union() {
                hull() {
                    move([0,20,0]) cuboid([4,60,10], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
                    move([30,20,20]) xrot(-45) move([0,0,-94]) cuboid([4,40,4], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
                }   

                hull() {
                    move([26,-30,0]) cuboid([4,40,10], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
                    move([32,0,0]) xrot(-45) move([0,0,-94]) cuboid([4,100,4], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
                }
            }

            move([0,-24,2]) cuboid([100,5,10], chamfer=1);
            move([26,-15,6]) cuboid([10,15,4], chamfer=1);
            
            move([0,-4,6]) cuboid([100,8,10], chamfer=1);
            move([8.5,31.5,1]) cyl(h=10,d=12);
        }
    }
}

module stand()
{
    difference() {
        union() {
            move([0,-15,-8]) {
                move([0,0,0]) sideStand();
                move([0,0,0]) xflip() sideStand();
            }

            // Back stay
            move([0,0,-152]) xrot(-45) move([0,-70,0.5]) cuboid([98,4,14], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);


            hull() {
                move([0,0,-152]) xrot(-45) move([17,-90,0.5]) cuboid([4,4,14], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
                move([0,0,-152]) xrot(-45) move([47,-72,0.5]) cuboid([4,4,14], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
            }

            hull() {
                move([0,0,-152]) xrot(-45) move([-17,-90,0.5]) cuboid([4,4,14], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
                move([0,0,-152]) xrot(-45) move([-47,-72,0.5]) cuboid([4,4,14], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
            }

            // Front stay
            move([0,0,-152]) xrot(-45) move([0,-150,13]) cuboid([34,4,38], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);
        }

        move([0,0,0]) xrot(-45) move([0,0,-117]) cuboid([100,140,10]);
        move([0,-50,-5]) cuboid([37,100,10]);
        move([0,10,-152]) xrot(45) move([0,0,70.1]) cuboid([150,30,10]);
    }
}

module render_stand(toPrint)
{
    if (!toPrint) {
        color([0,0.8,0,1]) {
            move([0,0,0]) {
                stand();
            }
        }
    } else {  
        move([0,0,112]) xrot(45) stand();
    }
}