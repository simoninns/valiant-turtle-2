/************************************************************************

    logotype.scad
    
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

module rounded_line(from_coord, to_coord)
{
    hull() {
        move(from_coord) cyl(h=1, d=1.5);
        move(to_coord) cyl(h=1, d=1.5);
    }
}

module logo_flippers()
{
    // V
    rounded_line([-19,0,0], [-16,3,0]);
    rounded_line([-16,3,0], [-12,3,0]);

    // Back flippers
    rounded_line([1,15,0], [13,15,0]);
    rounded_line([1,15,0], [0,12,0]);
    rounded_line([13,15,0], [13.5,11,0]);
    rounded_line([13.5,11,0], [10,7.5,0]);

    // Front flippers
    rounded_line([-9,15,0], [-13,15,0]);
    rounded_line([-9,15,0], [-6,11,0]);
    rounded_line([-13,15,0], [-14,9,0]);
    rounded_line([-14,9,0],[-11,6.5,0]);
}

module logotype()
{
    move([0,0,31.51]) zrot(90) scale([0.9,0.9,1]) {
        // Outer dodec
        difference() {
            cyl(h=1, d=26, $fn=10);
            cyl(h=2, d=23, $fn=10);
        }

        // Inter pentagon
        difference() {
            cyl(h=1, d=16, $fn=5);
            cyl(h=2, d=13, $fn=5);
        }

        // Spokes
        for(rota=[0: 360/5: 360]) { // for(variable = [start : increment : end])
            rotate([0,0,rota]) move([10,0,0]) cuboid([5,1.5,1]);
        }

        // Roman numeral II
        move([1.5,0,0]) cuboid([1.5,5,1]);
        move([-1.5,0,0]) cuboid([1.5,5,1]);

        move([0,2,0]) cuboid([6,1.5,1]);
        move([0,-2,0]) cuboid([6,1.5,1]);

        // Flippers
        logo_flippers();
        yflip() logo_flippers();
    }
}

module render_logotype(toPrint)
{
    if (!toPrint) {
        color([0.9,0.5,0.0,1]) {
            logotype();
        }
    } else {
        move([0,0,32]) yrot(-180) logotype();
    }
}