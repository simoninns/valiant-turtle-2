/************************************************************************

    screws.scad
    
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

// M3x10mm DIN912 head screw (hex bolt)
module m3x10_screw()
{
    // Generic quick screw render (the BOSL version was really slow)
    color([0.8, 0.8, 0.8]) difference() {
        union() {
            move([0,0,1]) cyl(h=3,d=5, chamfer2=0.125);
            move([0,0,-5.5]) cyl(h=10,d=3);
        }

        move([0,0,2]) cyl(h=2,d=2.5, $fn=6);

        //move([0,0,2]) cuboid([1,3,1], chamfer=0.25);
        //move([0,0,2]) cuboid([3,1,1], chamfer=0.25);
    }
}
