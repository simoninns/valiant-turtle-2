/************************************************************************

    bullet_connector.scad
    
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

module bullet_4mm_male()
{
    xrot(180) move([0,0,12.25/2]) difference() {
        union() {
            move([0,0,0]) cyl(h=12.25, d=3.25);
            move([0,0,2.25]) cyl(h=3.5, d=4);

            move([0,0,-3.5 - 0.125]) cyl(h=5, d=4.25);
            move([0,0,-4.5 +0.125]) cyl(h=3.5, d=4.75);
            move([0,0,-2.5 + 1]) cyl(h=0.75, d=4.75);
        }

        move([0,0,-9.5+4]) cyl(h=7, d=3.5);
        move([2,0,-5.25 + 0.5]) xcyl(h=4, d=2);
    }
}

module bullet_connector_male_mask()
{
    move([0,0,-9]) cyl(h=9,d=3.5);
    move([0,0,0.5]) cyl(h=1,d=3);
    move([0,0,-2.5]) cyl(h=5.5,d=5.5);
}