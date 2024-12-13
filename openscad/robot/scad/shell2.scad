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

module pentagon_top(line, thickness, fillet) {
    // Calculate the points of the pentagon (with a radius of 57)
    // The fillet is subtracted from the radius to maintain the outer diameter
    radius = 57 - fillet / 2;
    points = [
        [radius * cos(0), radius * sin(0)],
        [radius * cos(72), radius * sin(72)],
        [radius * cos(144), radius * sin(144)],
        [radius * cos(216), radius * sin(216)],
        [radius * cos(288), radius * sin(288)]
    ];
    
    // Render the pentagon line
    next_i = (line + 1) % len(points);
    hull() {
        translate([points[line][0], points[line][1], 0])
            cylinder(d=fillet, h=thickness, center=true);
        translate([points[next_i][0], points[next_i][1], 0])
            cylinder(d=fillet, h=thickness, center=true);
    }
}

module pentagon_side(line, thickness, fillet) {
    // Calculate the points of the irregular pentagon (radii of 52, 57 and 62)
    // The fillet is subtracted from the radius to maintain the outer diameter
    radius1 = 52 - fillet / 2;
    radius2 = 57 - fillet / 2;
    radius3 = 62 - fillet / 2;

    points = [
        [radius1 * cos(0), 0],
        [radius2 * cos(72), radius3 * sin(72)],
        [radius2 * cos(144), radius2 * sin(144)],
        [radius2 * cos(216), radius2 * sin(216)],
        [radius2 * cos(288), radius3 * sin(288)]
    ];
    
    // Render the pentagon line
    next_i = (line + 1) % len(points);
    hull() {
        translate([points[line][0], points[line][1], 0])
            cylinder(d=fillet, h=thickness, center=true);
        translate([points[next_i][0], points[next_i][1], 0])
            cylinder(d=fillet, h=thickness, center=true);
    }
}

module shell2_body() {
    // Render the top of the shell by combining the top and side pentagons using hulls
    for (i=[0:4]) {
        hull() {
            pentagon_top(i, 3, 4);
            zrot((72 * i) + (72 / 2)) {
                move([71, 0, -38.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(2, 4, 4);
                    }
                }
            }
        }
    }

    // Render the sides of the shell by combining the side pentagons using hulls
    for (i=[0:4]) {
        hull() {
            zrot((72 * i) + (72 / 2)) {
                move([71, 0, -38.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(1, 4, 4);
                    }
                }
            }

            zrot((72 * (i + 1)) + (72 / 2)) {
                move([71, 0, -38.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(3, 4, 4);
                    }
                }
            }
        }
    }

    // Render the lower sides of the shell
    for (i=[0:4]) {
        hull() {
            zrot((72 * i) + (72 / 2)) {
                move([71, 0, -38.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(0, 4, 4);
                    }
                }
            }

            zrot(72/2) {
                zrot((72 * i) + (72 / 2)) {
                    move([71, 0, (-38.5 * 2.5)]) {
                        rotate([0, -57, 0]) {
                            pentagon_side(4, 4, 4);
                        }
                    }
                }
            }
        }
    }

    // Bottom part of the shell
    for (i=[0:4]) {
        hull() {
            zrot((72 * (i+1)) + (72 / 2)) {
                move([71, 0, -38.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(4, 4, 4);
                    }
                }
            }

            zrot(72/2) {
                zrot((72 * i) + (72 / 2)) {
                    move([71, 0, (-38.5 * 2.5)]) {
                        rotate([0, -57, 0]) {
                            pentagon_side(0, 4, 4);
                        }
                    }
                }
            }
        }
    }

    for (i=[0:4]) {
        hull() {
            zrot(72/2) {
                zrot((72 * i) + (72 / 2)) {
                    move([71, 0, (-38.5 * 2.5)]) {
                        rotate([0, -57, 0]) {
                            pentagon_side(1, 4, 4);
                        }
                    }
                }
            }

            zrot(72/2) {
                zrot((72 * (i+1)) + (72 / 2)) {
                    move([71, 0, (-38.5 * 2.5)]) {
                        rotate([0, -57, 0]) {
                            pentagon_side(3, 4, 4);
                        }
                    }
                }
            }
        }
    }
}

module shell2_base()
{
    // Slice the bottom of the dodecahedron to create the base
    difference() {
        move([0,1,112]) zrot(360/20) shell2_body();
        move([0,0,-129 + 104]) cuboid([180,180,50]);
    }
}

module render_shell2(toPrint) {
    shell2_base();
}
