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
    radius = 55 - fillet / 2;
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

module pentagon_bottom(thickness, fillet) {
    // Calculate the points of the pentagon (with a radius of 57)
    // The fillet is subtracted from the radius to maintain the outer diameter
    radius = 78 - fillet / 2;
    points = [
        [radius * cos(0), radius * sin(0)],
        [radius * cos(72), radius * sin(72)],
        [radius * cos(144), radius * sin(144)],
        [radius * cos(216), radius * sin(216)],
        [radius * cos(288), radius * sin(288)]
    ];
    
    // Render the pentagon
    for (line=[0:4]) {
        next_i = (line + 1) % len(points);
        hull() {
            translate([points[line][0], points[line][1], 0])
                cylinder(d=fillet, h=thickness, center=true);
            translate([points[next_i][0], points[next_i][1], 0])
                cylinder(d=fillet, h=thickness, center=true);
        }
    }
}

module pentagon_side(line, thickness, fillet) {
    // Calculate the points of the irregular pentagon (radii of 52, 57 and 62)
    // The fillet is subtracted from the radius to maintain the outer diameter
    radius1 = 50 - fillet / 2;
    radius2 = 55 - fillet / 2;
    radius3 = 60 - fillet / 2;

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

module shell_body() {
    // Render the top of the shell by combining the top and side pentagons using hulls
    for (i=[0:4]) {
        hull() {
            pentagon_top(i, 3, 5);
            zrot((72 * i) + (72 / 2)) {
                move([69, 0, -37.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(2, 4, 5);
                    }
                }
            }
        }
    }

    // Render the sides of the shell by combining the side pentagons using hulls
    for (i=[0:4]) {
        hull() {
            zrot((72 * i) + (72 / 2)) {
                move([69, 0, -37.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(1, 4, 5);
                    }
                }
            }

            zrot((72 * (i + 1)) + (72 / 2)) {
                move([69, 0, -37.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(3, 4, 5);
                    }
                }
            }
        }
    }

    // Render the lower sides of the shell
    for (i=[0:4]) {
        hull() {
            zrot((72 * i) + (72 / 2)) {
                move([69, 0, -37.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(0, 4, 5);
                    }
                }
            }

            zrot(72/2) {
                zrot((72 * i) + (72 / 2)) {
                    move([69, 0, (-37.5 * 2.5)]) {
                        rotate([0, -57, 0]) {
                            pentagon_side(4, 4, 5);
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
                move([69, 0, -37.5]) {
                    rotate([0, 57, 0]) {
                        pentagon_side(4, 4, 5);
                    }
                }
            }

            zrot(72/2) {
                zrot((72 * i) + (72 / 2)) {
                    move([69, 0, (-37.5 * 2.5)]) {
                        rotate([0, -57, 0]) {
                            pentagon_side(0, 4, 5);
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
                    move([69, 0, (-37.5 * 2.5)]) {
                        rotate([0, -57, 0]) {
                            pentagon_side(1, 4, 5);
                        }
                    }
                }
            }

            zrot(72/2) {
                zrot((72 * (i+1)) + (72 / 2)) {
                    move([69, 0, (-37.5 * 2.5)]) {
                        rotate([0, -57, 0]) {
                            pentagon_side(3, 4, 5);
                        }
                    }
                }
            }
        }
    }
}

module shell_wheel_arches()
{
    // Rear lower wall
    move([0,60.75,2.5]) {
        hull() {
            move([(242/2) - 3,0,0]) cyl(h=5, d=6);
            move([-((242/2) - 3),0,0]) cyl(h=5, d=6);
        }
    }

    // Right front wall
    move([0,-10,2.5]) {
        hull() {
            move([(242/2) - 3,0,0]) cyl(h=5, d=6);
            move([((242/2) - 3) - 50,0,0]) cyl(h=5, d=6);
        }
    }

    // Left front wall
    move([0,-10,2.5]) {
        hull() {
            move([-((242/2) - 3),0,0]) cyl(h=5, d=6);
            move([-((242/2) - 3) + 50,0,0]) cyl(h=5, d=6);
        }
    }

    // Right outside wall
    hull() {
        move([0,-10,2.5]) move([(242/2) - 2,0,0]) cyl(h=5, d=4);
        move([0,60.75,2.5]) move([(242/2) - 2,0,0]) cyl(h=5, d=4);
    }

    // Left outside wall
    hull() {
        move([0,-10,2.5]) move([-((242/2) - 2),0,0]) cyl(h=5, d=4);
        move([0,60.75,2.5]) move([-((242/2) - 2),0,0]) cyl(h=5, d=4);
    }

    // Right outside triangle
    hull() {
        move([0,-10,2.5]) move([(242/2) - 2,0,0]) cyl(h=5, d=4);
        move([0,30,25]) move([(242/2) - 2,0,0]) cyl(h=5, d=4);
    }

    hull() {
        move([0,60.75,2.5]) move([(242/2) - 2,0,0]) cyl(h=5, d=4);
        move([0,30,25]) move([(242/2) - 2,0,0]) cyl(h=5, d=4);
    }

    // Right over wheel
    hull() {
        move([-30,30,32]) move([(242/2) - 2,0,0]) cyl(h=5, d=4);
        move([0,30,25]) move([(242/2) - 2,0,0]) cyl(h=5, d=4);
    }
    hull() {
        move([-30,30,42]) move([(242/2) - 2,0,0]) cyl(h=20, d=4);
        move([-27.5,30,42]) move([(242/2) - 2,0,0]) cyl(h=26, d=4);
    }

    // Left outside triangle
    hull() {
        move([0,-10,2.5]) move([-((242/2) - 2),0,0]) cyl(h=5, d=4);
        move([0,30,25]) move([-((242/2) - 2),0,0]) cyl(h=5, d=4);
    }

    hull() {
        move([0,60.75,2.5]) move([-((242/2) - 2),0,0]) cyl(h=5, d=4);
        move([0,30,25]) move([-((242/2) - 2),0,0]) cyl(h=5, d=4);
    }

    // Left over wheel
    hull() {
        move([30,30,32]) move([-((242/2) - 2),0,0]) cyl(h=5, d=4);
        move([0,30,25]) move([-((242/2) - 2),0,0]) cyl(h=5, d=4);
    }
    hull() {
        move([30,30,42]) move([-((242/2) - 2),0,0]) cyl(h=20, d=4);
        move([27.5,30,42]) move([-((242/2) - 2),0,0]) cyl(h=26, d=4);
    }
}

module front_screw_mount()
{
    move([0,-93 + 6,23]) {
        difference() {
            move([0,-1.5,-1]) zrot(54) cyl(h=8,d=11,$fn=5);

            // Hole for threaded insert
            move([0,-2,0]) zcyl(h=12, d=4);
        }
    }
}

module front_screw_mount_mask()
{
    move([0,-93 + 6,23]) {
        // Hole for threaded insert
        move([0,-2,0]) zcyl(h=12, d=4);
    }
}

module back_screw_mount()
{
    difference() {
        union() {
            hull() {
                move([0,0,-1]) zrot((360/20)) zcyl(h=8, d=10, $fn=5);
                move([0,4,-3]) cuboid([8,6,4]);
            }
        }

        // Hole for threaded insert
        move([0,0,-1]) zcyl(h=9, d=4);
    }
}

// Back screw mounts are 97mm apart, 7mm in diameter
module back_screw_mounts()
{
    move([0,56,5]) {
        move([(97/2),0,0]) back_screw_mount();
        xflip() move([(97/2),0,0]) back_screw_mount();
    }
}

module back_screw_mounts_mask()
{
    move([0,56,5]) {
        move([(97/2),0,0]) move([0,0,-1]) zcyl(h=9, d=4);
        xflip() move([(97/2),0,0]) move([0,0,-1]) zcyl(h=9, d=4);
    }
}

module shell_base()
{
    difference() {
        
        union() {
            // Render the dodecahedron and slice the lower part to create the base
            difference() {
                move([0,0.5,106]) zrot(360/20) shell_body();
                move([0,0,-129 + 104]) cuboid([180,180,50]);
            }

            // Add a pentagon around the base of the shell
            zrot((360/20) * 3) move([0,0,2.5]) pentagon_bottom(5, 6);

            // Render the wheel arches
            shell_wheel_arches();
        }
    
        // Gap for the head
        move([0,-80,-1]) prismoid(size1=[45,50], size2=[25,50], h=19);

        // Slice the base behind the wheel arches
        move([0,25.25 + 0.125,2]) cuboid([180,64.5 + 0.25,10]);

        // Mask for the back screw mounts
        back_screw_mounts_mask();

        // Mask for the front screw mounts
        front_screw_mount_mask();
    }

    back_screw_mounts();
    front_screw_mount();
}

module render_shell(toPrint) {
    if (!toPrint) {
        color([0.0,0.8,0.0,1]) shell_base();
    } else {
        shell_base();
    }
}

module render_shell_screws(toPrint)
{
    if (!toPrint) {
        move([48.5,56,-3]) xrot(180) m3x10_screw();
        move([-48.5,56,-3]) xrot(180) m3x10_screw();
    }
}
