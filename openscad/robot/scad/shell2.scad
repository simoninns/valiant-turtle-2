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

module pentagon(radial_width, radial_height, thickness, fillet) {
    // Compensate for fillet
    radial_width = radial_width - (fillet / 2);
    radial_height = radial_height - (fillet / 2);

    // Calculate the points of the pentagon
    points = [
        [0, radial_height],
        [radial_width * 0.951, radial_height * 0.309],
        [radial_width * 0.588, radial_height * -0.809],
        [-radial_width * 0.588, radial_height * -0.809],
        [-radial_width * 0.951, radial_height * 0.309]
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
    pentagon(105/2,100/2, 4, 1);
}
