/************************************************************************

    light_pipe.scad
    
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

module light_pipe()
{
    move([0,0,0]) cuboid([6,3,2], chamfer=0.75, edges=EDGES_TOP);

    hull() {
        move([0,0,-8]) cuboid([4,3,15]);
        move([0,0,-16.5]) cuboid([2,2,1]);
    }
}

module render_light_pipe(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.9,1]) move([25,-34,49]) {
            move([0,0,0]) light_pipe();
        }
    } else {
        move([8.5,0,1.5]) yrot(90) zrot(90) light_pipe();
    }
}