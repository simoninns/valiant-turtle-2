/************************************************************************

    pen_holder_cap.scad
    
    Valiant Turtle 2
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

module pen_holder_cap()
{
    move([0,0,4]) {
        difference() {
            cyl(h=14, d=12, chamfer2=0.5);
            move([0,0,-8 + 6]) cyl(h=14, d=8, chamfer2=0.5);

            // Knurled top outer
            for(rota=[0: 360/16: 360]) { // for(variable = [start : increment : end])
                rotate([0,0,rota]) move([6.25,0,3.25 - 4.5]) cyl(h=12, d=1.5, chamfer2=0.25); // Top
            }

            // Test only
            //move([0,-9,-8 + 6.5]) cuboid([18,18,18]);
        }
    }
}

module render_pen_holder_cap(crend, toPrint, penUp)
{
    if (!toPrint) {
        color([0.8,0.8,0.8]) {
            if(penUp) move([0,29,-25 + 4]) xrot(180) pen_holder_cap();
            else move([0,29,-25]) xrot(180) pen_holder_cap();
        }
    } else {
        move([0,0,11]) xrot(180) pen_holder_cap();
    }
}    