/************************************************************************

    shell_bottom.scad
    
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

include <threaded_inserts.scad>

// 0 = Back
// 1 = Right wheel
// 2 = Right front
// 3 = Left front
// 4 = Left wheel
module irrPentagonBottom(pos)
{
    zrot((360/5) * pos) {
        move([0,69,0]) xrot(54) { // 36.25
            hull() {
                zrot((360/5) * 0) move([0,104/2,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 1) move([0,122/2,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 2) move([0,107/2,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 3) move([0,107/2,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 4) move([0,122/2,0]) staggered_sphere(d=2, $fn=16);
            }
        }
    }
}

module irrPentagonBottom_topedge(pos)
{
    zrot((360/5) * pos) {
        move([0,69,0]) xrot(54) { // 36.25
            hull() {
                zrot((360/5) * 0) move([0,104/2,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 1) move([0,122/2,0]) staggered_sphere(d=2, $fn=16);
            }

            hull() {
                zrot((360/5) * 0) move([0,104/2,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 4) move([0,122/2,0]) staggered_sphere(d=2, $fn=16);
            }
        }
    }
}

// This is a slightly deeper version of the pentagon used to remove
// any material protruding through the panels of the wheel arches
module irrPentagonBottom2(pos)
{
    zrot((360/5) * pos) {
        move([0,69,0]) xrot(54) { // 36.25
            hull() {
                zrot((360/5) * 0) move([0,(104/2)+4,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 1) move([0,(122/2)+4,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 2) move([0,(107/2)+4,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 3) move([0,(107/2)+4,0]) staggered_sphere(d=2, $fn=16);
                zrot((360/5) * 4) move([0,(122/2)+4,0]) staggered_sphere(d=2, $fn=16);
            }
        }
    }
}

module wheelArchBase()
{
    // Wheel arch base is 3mm wide (rest of shell is 2mm)
    hull() {
        move([71,-15,-7.5]) zcyl(h=3,d=3,$fn=16);
        move([120.5,-15,-7.5]) zcyl(h=3,d=3,$fn=16);
    }

    hull() {
        move([46.5,62.5,-7.5]) zcyl(h=3,d=3,$fn=16);
        move([120.5,62.5,-7.5]) zcyl(h=3,d=3,$fn=16);
    }

    hull() {
        move([120.5,-15,-7.5]) zcyl(h=3,d=3,$fn=16);
        move([120.5,62.5,-7.5]) zcyl(h=3,d=3,$fn=16);
    }
}

module wheelArch()
{
    difference() {
        union() {
            // Plot the side of the shell and cutout the wheel arch space
            difference() {
                union() {
                    irrPentagonBottom(4);
                    wheelArchBase();
                }

                // Cut space for the wheel arch
                move([80-2,23.75,20]) cuboid([82,74.5,60]);
            }
            
            // Add the top edge of the pentagon back in
            irrPentagonBottom_topedge(4);

            // Render the wheelcover
            wheelCover();
        }

        // Smooth the inside of the wheel arch
        move([-1,0,2]) irrPentagonBottom2(4);
    }
}

module wheelCover()
{
    move([0,23.5,-8]) {
        // Point cloud for the wheel arch (see doc/wheel_arch_points.jpg)
        pointA = [73.5,-38.5,2];
        pointB = [120.5,-38.5,2];
        pointC = [120.5,39,2];
        // pointD unused
        pointE = [120.5,7.5,22.5];
        pointF = [94,-38.5,13.5];
        pointG = [94,7.5,33.5];
        pointH = [94,-38.5,29];
        pointI = [94,7.5,49.5];
        pointJ = [70.5,39.0,31.5];
        pointK = [70.5,39.0,23];
        pointL = [48,39.0,2];

        // ABF (note: same plane as AFH)
        hull() {
            move(pointA) staggered_sphere(d=3, $fn=16);
            move(pointB) staggered_sphere(d=3, $fn=16);
            move(pointF) staggered_sphere(d=3, $fn=16);
        }

        // AFH (note: same plane as ABF)
        hull() {
            move(pointA) staggered_sphere(d=3, $fn=16);
            move(pointF) staggered_sphere(d=3, $fn=16);
            move(pointH) staggered_sphere(d=3, $fn=16);
        }

        // BCE
        hull() {
            move(pointC) staggered_sphere(d=3, $fn=16);
            move(pointB) staggered_sphere(d=3, $fn=16);
            move(pointE) staggered_sphere(d=3, $fn=16);
        }

        // CLK (note: same plane as KLJ)
        hull() {
            move(pointC) staggered_sphere(d=3, $fn=16);
            move(pointL) staggered_sphere(d=3, $fn=16);
            move(pointK) staggered_sphere(d=3, $fn=16);
        }

        // KLJ (note: same plane as CLK)
        hull() {
            move(pointL) staggered_sphere(d=3, $fn=16);
            move(pointK) staggered_sphere(d=3, $fn=16);
            move(pointJ) staggered_sphere(d=3, $fn=16);
        }

        // FHIG
        hull() {
            move(pointF) staggered_sphere(d=3, $fn=16);
            move(pointH) staggered_sphere(d=3, $fn=16);
            move(pointI) staggered_sphere(d=3, $fn=16);
            move(pointG) staggered_sphere(d=3, $fn=16);
        }

        // IJKG
        hull() {
            move(pointI) staggered_sphere(d=3, $fn=16);
            move(pointJ) staggered_sphere(d=3, $fn=16);
            move(pointK) staggered_sphere(d=3, $fn=16);
            move(pointG) staggered_sphere(d=3, $fn=16);
        }

        // CEGK
        hull() {
            move(pointC) staggered_sphere(d=3, $fn=16);
            move(pointE) staggered_sphere(d=3, $fn=16);
            move(pointG) staggered_sphere(d=3, $fn=16);
            move(pointK) staggered_sphere(d=3, $fn=16);
        }

        // FGEB
        hull() {
            move(pointF) staggered_sphere(d=3, $fn=16);
            move(pointG) staggered_sphere(d=3, $fn=16);
            move(pointE) staggered_sphere(d=3, $fn=16);
            move(pointB) staggered_sphere(d=3, $fn=16);
        }
    }
}

module back_screw_mount()
{
    difference() {
        union() {
            hull() {
                move([0,0,-1]) zcyl(h=8, d=10);
                move([0,5,-3]) cuboid([8,6,4]);
            }
        }

        // Hole for threaded insert
        move([0,0,-1]) zcyl(h=9, d=5);
    }

    // Threaded insert
    difference() {
        move([0,0,-5]) xrot(180) insertM3x57();
        
        // M3 Screw clearance
        move([0,0,-5]) xrot(180) zcyl(h=18, d=3.25);
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

module shellBottomArches()
{
    move([0,1.5,9]) difference() {
        union() {
            // Wheel arches
            wheelArch();
            xflip() wheelArch();

            irrPentagonBottom(0);
        }

        // Slice the bottom of the shell to make it flush with the body
        move([0,0,-29]) cuboid([200,200,40]);
    }
}

module shellBottom_attachement()
{
    difference() {
        move([0,58,0]) xrot(-36.25) move([0,0,52]) cyl(h=5, d=10, $fn=6);

        // Hole for M3x10mm screw
        move([0,58,0]) xrot(-36.25) move([0,0,53]) cyl(h=8, d=3);
        move([0,58,0]) xrot(-36.25) move([0,0,50]) cyl(h=4, d=7);
    }
}

module shellBottom()
{
    move([0,1.5,9]) difference() {
        union() {
            // Back lower edge reenforcement
            hull() {
                move([0,62.25,-7.5]) cuboid([95,2.5,4]);
                move([0,67.25,-2]) cuboid([98,1,1]);
            }   
        }

        // Slice the bottom of the shell to make it flush with the body
        move([0,0,-29]) cuboid([200,200,40]);

        // Screwdriver path (for upper shell mount)
        move([0,-1.5,-9]) move([0,58,0]) xrot(-36.25) move([0,0,4]) cyl(h=16, d=6);
    }
    
    // Render back screw mounts
    back_screw_mounts();

    // Render the attachment for attaching the upper shell
    shellBottom_attachement();
}

// Note: From edge to edge of the wheel covers, the shell is 244mm wide
// The plastic is 3mm thick around the base of the wheel covers but the rest
// of the shell is 2mm thick
module render_shell_bottom(crend, toPrint)
{
    if (!toPrint) {
        difference() {
            union() {
                color([0,0.8,0,1]) shellBottom();
                color([0,0.8,0,1]) shellBottomArches();
            }

            render_shell_top(crend, toPrint);
        }
    } else {
        move([0,0,0]) xrot(0) {
            difference() {
                union() {
                    shellBottom();
                    shellBottomArches();
                }
                render_shell_top(crend, false);
            }
        }
    }
}