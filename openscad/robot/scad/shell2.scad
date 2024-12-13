/************************************************************************

    shell2.scad
    
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

module pentagon_top(thickness, fillet) {
    // Calculate the points of the pentagon (with a radius of 57)
    points = [
        [57 * cos(0), 57 * sin(0)],
        [57 * cos(72), 57 * sin(72)],
        [57 * cos(144), 57 * sin(144)],
        [57 * cos(216), 57 * sin(216)],
        [57 * cos(288), 57 * sin(288)]
    ];
    
    // Render the pentagon
    for (i = [0 : len(points) - 1]) {
        next_i = (i + 1) % len(points);
        hull() {
            translate([points[i][0], points[i][1], 0])
                cylinder(d=fillet, h=thickness, center=true);
            translate([points[next_i][0], points[next_i][1], 0])
                cylinder(d=fillet, h=thickness, center=true);
        }
    }
}

module pentagon_side(thickness, fillet) {
    // Calculate the points of the irregular pentagon (radii of 52, 57 and 62)
    points = [
        [52 * cos(0), 0],
        [57 * cos(72), 62 * sin(72)],
        [57 * cos(144), 57 * sin(144)],
        [57 * cos(216), 57 * sin(216)],
        [57 * cos(288), 62 * sin(288)]
    ];
    
    // Render the pentagon
    for (i = [0 : len(points) - 1]) {
        next_i = (i + 1) % len(points);
        hull() {
            translate([points[i][0], points[i][1], 0])
                cylinder(d=fillet, h=thickness, center=true);
            translate([points[next_i][0], points[next_i][1], 0])
                cylinder(d=fillet, h=thickness, center=true);
        }
    }
}

module render_shell2(toPrint) {
    radial_width = 68 / (2 * sin(36));
    radial_height = 62 / (2 * sin(36));
    echo("radial_width = ", radial_width);
    echo("radial_height = ", radial_height);

    pentagon_top(3,1);
    pentagon_side(3, 1);

    //move([5,0,-2]) cuboid([100,10,2]);
}
