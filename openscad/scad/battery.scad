/************************************************************************

    battery.scad
    
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

// Note: The exact battery type is not currently known, so this module provides
// a mock up of what will reasonable fit into the available chassis space.

module battery()
{
    move([0,-17,20]) cuboid([90,46,40], chamfer=1);
}   

module render_battery(crend, toPrint)
{
    if (!toPrint) {
        color([0.3,0.8,0.5]) battery();
    }
}