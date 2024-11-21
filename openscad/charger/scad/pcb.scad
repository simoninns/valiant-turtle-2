/************************************************************************

    pcb.scad
    
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

module pcb()
{
    // Basic PCB
    difference() {
        color([0,0.6,0,1]) cuboid([18,37,1.75]);

        // Mounting holes
        move([+(7.75 - 0.5),-17.25 + 0.5,0]) cyl(h=4, d=2.5);
        move([-(7.75 - 0.5),-17.25 + 0.5,0]) cyl(h=4, d=2.5);
    }

    // USB-C connector
    color([0.8, 0.8, 0.8]) move([0,15 + 1.5,2.5]) {
        hull() {
            move([+(2.75+0.125),0,0]) ycyl(h=7,d=3.25);
            move([-(2.75+0.125),0,0]) ycyl(h=7,d=3.25);
        }
    }

    // CR LED (red)
    color([0.8, 0, 0]) move([8-2,(-17.75 - 0.125) + 7,1.25]) cuboid([2,1.25,1]);

    // OK LED (blue)
    color([0, 0, 0.8]) move([8-2,(-17.75 - 0.125) + 9,1.25]) cuboid([2,1.25,1]);

    // Inductor
    color([0.4, 0.4, 0.4]) move([-5.75 + 1,15.25 - 8,3]) cuboid([6.5,6.5,4.5]);

    // Battery connectors (for screw clearance check)
    color([0.8,0.8,0.0,1]) move([0,-16.5,1]) cuboid([9.5,4,0.5]);
}

module render_pcb(toPrint)
{
    if (!toPrint) {
        move([35,-28,30]) {
            zrot(-90) pcb();
        }
    }
}