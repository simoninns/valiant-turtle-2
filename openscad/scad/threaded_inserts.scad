/************************************************************************

    threaded_inserts.scad
    
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

// M3x5.7x4.6 threaded insert profile (CNC Kitchen)
// Blind hole
module insertM3x57()
{
    move([0,0,-4]) difference() {
        cyl(h=8,d=6);
        move([0,0,8 - 6.7]) cyl(h=8,d=3.9);
        move([0,0,3.5]) cyl(h=2,d=3.9+1, chamfer1=1);
    }
}

// M3x5.7x4.6 threaded insert profile (CNC Kitchen)
// Through hole
module insertM3x57_th()
{
    difference() {
        insertM3x57();
        move([0,0,-3.1 - 4]) cyl(h=2,d=3.25);
    }
}