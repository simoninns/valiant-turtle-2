/************************************************************************

    shell_top.scad
    
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

module pentagonTop()
{
    hull() {
        zrot((360/5) * 0) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 1) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 2) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 3) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 4) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
    }
}

module irrPentagonTop()
{
    hull() {
        zrot((360/5) * 0) move([0,103/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 1) move([0,123/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 2) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 3) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 4) move([0,123/2,0]) staggered_sphere(d=2, $fn=16);
    }
}

module shellTop()
{
    move([0,1.5,105]) yrot(180) {
        // Centre
        pentagonTop();

        for ( i = [0:1:4]) {
            zrot((360/5) * i) {
                zrot(360/10) move([0,70,36.75]) xrot(55.5) irrPentagonTop();
            }
        }
    }
}

module joinerLine()
{
    hull() {
        zrot(360/10) move([0,70,36.75]) xrot(55.5) {
            zrot((360/5) * 0) move([0,(103/2),0]) staggered_sphere(d=2, $fn=16);
            zrot((360/5) * 1) move([0,(123/2),0]) staggered_sphere(d=2, $fn=16);
        }
    }

    hull() {
        zrot(360/10) move([0,70,36.75]) xrot(55.5) {
            zrot((360/5) * 0) move([0,(103/2),0]) staggered_sphere(d=2, $fn=16);
            zrot((360/5) * 4) move([0,(123/2),0]) staggered_sphere(d=2, $fn=16);
        }
    }
}

module joiner()
{
    move([0,1.5,104]) yrot(180) {
        for ( i = [0:1:4]) {
            zrot((360/5) * i) joinerLine();
        }
    }
}

module front_screw_mount()
{
    move([0,-93 + 6,23]) {
        difference() {
            hull() {
                move([0,-2,-1]) zcyl(h=8, d=7);
                move([0,-5.5,11]) xrot(-34) cuboid([14,1,10]);
            }

            // Hole for threaded insert
            move([0,-2,0]) zcyl(h=12, d=5);
        }

        // Threaded insert
        move([0,-2,0]) difference() {
            move([0,0,-5]) xrot(180) insertM3x57();
            
            // M3 Screw clearance
            move([0,0,-5]) xrot(180) zcyl(h=18, d=3.25);
        }
    }
}

// Cut a slot in the bottom shell front for the body's head
module headCutout()
{
    move([0,-1,-14]) {
        hull() {
            move([0,119.5 - 210,0]) {
                cuboid([43.5,65,10]);
                move([0,-32.5,-(10/2)]) xrot(90) right_triangle([21.5,10,21.5]);
                yrot(180) move([0,-32.5,-(10/2)]) xrot(90) right_triangle([21.5,10,21.5]);
            }

            move([0,119.5 - 210,13]) {
                cuboid([22.5,65,20]);
                move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
                yrot(180) move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
            }
        }
    }
}

module front_panels()
{
    move([0,1.5,9]) difference() {
        union() {
            // Front panels
            difference() {
                union() {
                    irrPentagonBottom(2);
                    irrPentagonBottom(3);
                }

                // Hole for threaded insert
                move([0,-93 + 4 - 1.5,23 - 9]) zcyl(h=12, d=5);
                
                // Head cutout
                headCutout();
            }
        }

        // Slice the bottom of the shell to make it flush with the body
        move([0,0,-29]) cuboid([200,200,40]);
    }
    
    front_screw_mount();
}

module shellTop_attachement()
{
    difference() {
        move([0,58,0]) xrot(-36.25) move([0,0,62.5]) cyl(h=16, d=10, $fn=6);
        move([0,58,0]) xrot(-40) move([2,0,72.5]) yrot(28) cuboid([20,20,8]);
        move([0,58,0]) xrot(-40) move([2,0,74.5]) yrot(-28) cuboid([20,20,8]);
        move([0,58,-9]) xrot(-36.25) move([0,0,63.5]) cuboid([20,4,40]);
        move([0,58,0]) xrot(-36.25) move([0,0,58]) cyl(h=8, d=5);
    }

    move([0,58,0]) xrot(-36.25) move([0,0,55]) xrot(180) insertM3x57();
}

module render_shell_top(crend, toPrint)
{
    if (!toPrint) {
        color([0,0.8,0,1]) {
            shellTop();
            joiner();
            front_panels();
            shellTop_attachement();
        }
    } else {  
        move([0,0,106]) xrot(180) {
            shellTop();
            joiner();
            front_panels();
            shellTop_attachement();
        }
    }
}