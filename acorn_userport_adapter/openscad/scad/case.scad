/************************************************************************

    main.scad
    
    Valiant Turtle Parallel to Acorn BBC User-port adapter
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

module case_top()
{

}

module case_bottom()
{
    move([0,0,11]) {
        difference() {
            move([0,1,-7]) cuboid([44, 40, 8]);
            move([0,-1,0]) cuboid([40, 38+2, 18]);

            move ([33/2,0,-8]) cyl(h=8,d=3.25);
            move ([-(33/2),0,-8]) cyl(h=8,d=3.25);
        }

        move ([33/2,0,-8]) {
            difference() {
                cyl(h=2,d=6);
                cyl(h=8,d=3.25);
            }
        }
        move ([-(33/2),0,-8]) {
            difference() {
                cyl(h=2,d=6);
                cyl(h=8,d=3.25);
            }
        }

        move([0,-17,-8]) cuboid([40,4,2]);
        move([0,+17,-8]) cuboid([40,4,2]);
    }
}

module render_case_bottom(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) case_bottom();
    } else {
        case_bottom();
    }
}

module render_case_top(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) case_top();
    } else {
        case_top();
    }
}