/************************************************************************

    shell_top.scad
    
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

// Shell lid ----------------------------------------------------------------------------------------------------------
module shell_lid_top()
{
    difference() {
        union() {
            difference() {
                union() {
                    // Copy of the top part of the shell
                    move([0,1.5,104]) yrot(180) {
                        for ( i = [0:1:4]) {
                            zrot((360/5) * i) {
                                zrot(360/10) move([0,70,36.75]) xrot(55.5) irrPentagonTop();
                            }
                        }
                    }

                    // Top pentagon
                    move([0,1.5,104]) yrot(180) {
                        hull() {
                            zrot((360/5) * 0) move([0,110/2,0]) staggered_sphere(d=2, $fn=6);
                            zrot((360/5) * 1) move([0,110/2,0]) staggered_sphere(d=2, $fn=6);
                            zrot((360/5) * 2) move([0,110/2,0]) staggered_sphere(d=2, $fn=6);
                            zrot((360/5) * 3) move([0,110/2,0]) staggered_sphere(d=2, $fn=6);
                            zrot((360/5) * 4) move([0,110/2,0]) staggered_sphere(d=2, $fn=6);
                        }
                    }
                }

                // Slice the bottom of the lid
                move([0,0,34.01-2]) cuboid([220,220,143]);        
            }

            // Add some thickness back in
            move([0,1.5,104]) yrot(180) {
                hull() {
                    zrot((360/5) * 0) move([0,(110/2)-2,0]) staggered_sphere(d=2, $fn=6);
                    zrot((360/5) * 1) move([0,(110/2)-2,0]) staggered_sphere(d=2, $fn=6);
                    zrot((360/5) * 2) move([0,(110/2)-2,0]) staggered_sphere(d=2, $fn=6);
                    zrot((360/5) * 3) move([0,(110/2)-2,0]) staggered_sphere(d=2, $fn=6);
                    zrot((360/5) * 4) move([0,(110/2)-2,0]) staggered_sphere(d=2, $fn=6);
                }
            }
        }

        // Add a gap for the lid dot
        move([0,-44 + 25,104]) {
            difference() {
                cyl(h=4, d=8);
                move([0,-5,0]) cuboid([10,10,4]);
            }
        }
    }
}

module shell_lid_lip()
{
    width2 = 106.5;

    move([0,1.5,102.25]) yrot(180) {
        difference() {
            union() {
                hull() {
                    zrot((360/5) * 0) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                    zrot((360/5) * 1) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                }

                hull() {
                    zrot((360/5) * 1) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                    zrot((360/5) * 2) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                }

                hull() {
                    zrot((360/5) * 2) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                    zrot((360/5) * 2) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                }

                hull() {
                    zrot((360/5) * 2) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                    zrot((360/5) * 3) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                }

                hull() {
                    zrot((360/5) * 3) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                    zrot((360/5) * 4) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                }

                hull() {
                    zrot((360/5) * 4) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                    zrot((360/5) * 0) move([0,width2/2,0]) xrot(45) cuboid([2,2,2]); // cyl(d=2, h=2, $fn=6);
                }
            }

            move([0,0,2.5]) cuboid([110,110,4]);
        }
    }
}

module shell_lid()
{
    shell_lid_top();
    shell_lid_lip();
}

// Top half of shell --------------------------------------------------------------------------------------------------

module irrPentagonTop()
{
    hull() {
        zrot((360/5) * 0) move([0,103/2,0]) staggered_sphere(d=2, $fn=6);
        zrot((360/5) * 1) move([0,123/2,0]) staggered_sphere(d=2, $fn=6);
        zrot((360/5) * 2) move([0,110/2,0]) staggered_sphere(d=2, $fn=6);
        zrot((360/5) * 3) move([0,110/2,0]) staggered_sphere(d=2, $fn=6);
        zrot((360/5) * 4) move([0,123/2,0]) staggered_sphere(d=2, $fn=6);
    }
}

module shellTop()
{
    difference() {
        move([0,1.5,104]) yrot(180) {
            for ( i = [0:1:4]) {
                zrot((360/5) * i) {
                    zrot(360/10) move([0,70,36.75]) xrot(55.5) irrPentagonTop();
                }
            }
        }

        // Slice the top to make space for the lid
        move([0,0,104.5]) cuboid([140,140,2]);
    }
}

module front_screw_mount()
{
    move([0,-93 + 6,23]) {
        difference() {
            hull() {
                move([0,-2,0]) zcyl(h=10, d=7);
                move([0,-2,0]) zrot(54) cyl(h=10,d=14,$fn=5);
            }

            // Hole for threaded insert
            move([0,-2,0]) zcyl(h=12, d=4);

            move([6,-6,-2]) xrot(45) zrot(28) cuboid([15,4,14]);
        xflip() move([6,-6,-2]) xrot(45) zrot(28) cuboid([15,4,14]);
        }
    }
}

// Cut a slot in the bottom shell front for the body's head
module headCutout()
{
    move([0,-1,-14]) {
        hull() {
            move([0,119.5 - 210,0]) {
                cuboid([43.5+1,65,10]);
                move([0,-32.5,-(10/2)]) xrot(90) right_triangle([21.5,10,21.5]);
                yrot(180) move([0,-32.5,-(10/2)]) xrot(90) right_triangle([21.5,10,21.5]);
            }

            move([0,119.5 - 210,13]) {
                cuboid([22.5+2,65,20]);
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

                    // Reenforce the lower edge
                    zrot((360/5) * 3) move([-12.5,62,-8.25]) cuboid([66,2,1.5], chamfer=0.5);
                    xflip() zrot((360/5) * 3) move([-12.5,62,-8.25]) cuboid([66,2,1.5], chamfer=0.5);

                    // Reenforce the head cutout
                    move([15.75+0.5,-73 - 1.5,12 - 9]) yrot(-29) xrot(48.5) cuboid([2,1.75,39], chamfer=0.5);
                    xflip() move([15.75+0.5,-73 - 1.5,12 - 9]) yrot(-29) xrot(48.5) cuboid([2,1.75,39], chamfer=0.5);
                }

                // Hole for threaded insert
                move([0,-93 + 4 - 1.5,23 - 9]) zcyl(h=12, d=4);
                
                // Head cutout
                headCutout();
            }
        }

        // Slice the bottom of the shell to make it flush with the body
        move([0,0,-29]) cuboid([200,200,40]);
    }

    front_screw_mount();
}

// Shell lower part ---------------------------------------------------------------------------------------------------

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
                zrot((360/5) * 0) move([0,104/2,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 1) move([0,122/2,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 2) move([0,107/2,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 3) move([0,107/2,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 4) move([0,122/2,0]) staggered_sphere(d=2, $fn=6);
            }
        }
    }
}

module irrPentagonBottom_topedge(pos)
{
    zrot((360/5) * pos) {
        move([0,69,0]) xrot(54) { // 36.25
            hull() {
                zrot((360/5) * 0) move([0,104/2,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 1) move([0,122/2,0]) staggered_sphere(d=2, $fn=6);
            }

            hull() {
                zrot((360/5) * 0) move([0,104/2,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 4) move([0,122/2,0]) staggered_sphere(d=2, $fn=6);
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
                zrot((360/5) * 0) move([0,(104/2)+4,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 1) move([0,(122/2)+4,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 2) move([0,(107/2)+4,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 3) move([0,(107/2)+4,0]) staggered_sphere(d=2, $fn=6);
                zrot((360/5) * 4) move([0,(122/2)+4,0]) staggered_sphere(d=2, $fn=6);
            }
        }
    }
}

module wheelArchBase()
{
    hull() {
        move([71,-15,-7.5]) zcyl(h=3,d=2,$fn=6);
        move([120.5,-15,-7.5]) zcyl(h=3,d=2,$fn=6);
    }

    hull() {
        move([46.5,62.5,-7.5]) zcyl(h=3,d=2,$fn=6);
        move([120.5,62.5,-7.5]) zcyl(h=3,d=2,$fn=6);
    }

    hull() {
        move([120.5,-15,-7.5]) zcyl(h=3,d=2,$fn=6);
        move([120.5,62.5,-7.5]) zcyl(h=3,d=2,$fn=6);
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
                move([80-2,23.75,20]) cuboid([82,75.5,60]);

                yrot(37.5) move([61,-13,62]) zrot(45) cuboid([4,3,48]);
                xflip() yrot(37.5) move([61,-13,62]) zrot(45) cuboid([4,3,48]);
            }
            
            // Add the top edge of the pentagon back in
            irrPentagonBottom_topedge(4);

            // Render the wheelcover
            wheelCover();
        }

        // Smooth the inside of the wheel arch
        move([-0.5,0,2.5]) irrPentagonBottom2(4);

        yrot(37.5) move([61,-13,52]) zrot(45) cuboid([4,3,36]);
        xflip() yrot(37.5) move([61,-13,52]) zrot(45) cuboid([4,3,36]);
    }
    
    yrot(37.5) move([63,-16,54]) zrot(45) cuboid([2,1,36.5], chamfer=0.5, edges=EDGES_TOP);
    xflip() yrot(37.5) move([63,-16,54]) zrot(45) cuboid([2,1,36.5], chamfer=0.5, edges=EDGES_TOP);
}

module wheelCover()
{
    move([0,23.5,-8]) {
        // Point cloud for the wheel arch (see doc/wheel_arch_points.jpg)
        pointA = [73.5,-38.5,2];
        pointB = [120.5,-38.5,2 + 6];
        pointC = [120.5,39,2];
        pointD = [120.5,-38.5,2];
        pointE = [120.5,7.5,22.5 + 7.5];
        pointF = [94,-38.5,13.5 + 4];
        pointG = [94,7.5,33.5 + 6];
        pointH = [94,-38.5,29];
        pointI = [94,7.5,49.5];
        pointJ = [70.5,39.0,31.5];
        pointK = [70.5,39.0,23 - 3];
        pointL = [48,39.0,2];

        // ADBF
        hull() {
            move(pointA) staggered_sphere(d=2, $fn=6);
            move(pointB) staggered_sphere(d=2, $fn=6);
            move(pointD) staggered_sphere(d=2, $fn=6);
            move(pointF) staggered_sphere(d=2, $fn=6);
        }

        // AFH (note: same plane as ABF)
        hull() {
            move(pointA) staggered_sphere(d=2, $fn=6);
            move(pointF) staggered_sphere(d=2, $fn=6);
            move(pointH) staggered_sphere(d=2, $fn=6);
        }

        // BCDE
        hull() {
            move(pointC) staggered_sphere(d=2, $fn=6);
            move(pointB) staggered_sphere(d=2, $fn=6);
            move(pointD) staggered_sphere(d=2, $fn=6);
            move(pointE) staggered_sphere(d=2, $fn=6);
        }

        // CLK (note: same plane as KLJ)
        hull() {
            move(pointC) staggered_sphere(d=2, $fn=6);
            move(pointL) staggered_sphere(d=2, $fn=6);
            move(pointK) staggered_sphere(d=2, $fn=6);
        }

        // KLJ (note: same plane as CLK)
        hull() {
            move(pointL) staggered_sphere(d=2, $fn=6);
            move(pointK) staggered_sphere(d=2, $fn=6);
            move(pointJ) staggered_sphere(d=2, $fn=6);
        }

        // FHIG
        hull() {
            move(pointF) staggered_sphere(d=2, $fn=6);
            move(pointH) staggered_sphere(d=2, $fn=6);
            move(pointI) staggered_sphere(d=2, $fn=6);
            move(pointG) staggered_sphere(d=2, $fn=6);
        }

        // IJKG
        hull() {
            move(pointI) staggered_sphere(d=2, $fn=6);
            move(pointJ) staggered_sphere(d=2, $fn=6);
            move(pointK) staggered_sphere(d=2, $fn=6);
            move(pointG) staggered_sphere(d=2, $fn=6);
        }

        // CEGK
        hull() {
            move(pointC) staggered_sphere(d=2, $fn=6);
            move(pointE) staggered_sphere(d=2, $fn=6);
            move(pointG) staggered_sphere(d=2, $fn=6);
            move(pointK) staggered_sphere(d=2, $fn=6);
        }

        // FGEB
        hull() {
            move(pointF) staggered_sphere(d=2, $fn=6);
            move(pointG) staggered_sphere(d=2, $fn=6);
            move(pointE) staggered_sphere(d=2, $fn=6);
            move(pointB) staggered_sphere(d=2, $fn=6);
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

module shellBottom()
{
    move([0,1.5,9]) difference() {
        union() {
            // Back lower edge reenforcement
            hull() {
                move([0,62.25,-7.5]) cuboid([95,2.5,3]);
                move([0,67.5,-2]) cuboid([98,0.5,1]);
            }   
        }

        // Slice the bottom of the shell to make it flush with the body
        move([0,0,-29]) cuboid([200,200,40]);
    }
    
    // Render back screw mounts
    back_screw_mounts();
}

module shell_dot()
{
    move([0,0,0.5]) cyl(h=1, d=15, chamfer1=0.5);

    move([0,0,2]) {
        difference() {
            cyl(h=3, d=8, chamfer2=0.5);
            move([0,5,0]) cuboid([10,10,4]);
        }
    }
}

module render_shell(toPrint)
{
    if (!toPrint) {
        color([0,0.8,0,1]) {
            move([0,0,0]) {
                // Top
                shellTop();
                front_panels();

                // Bottom
                shellBottom();
                shellBottomArches();
            }
        }
    } else {  
        // Top
        shellTop();
        front_panels();

        // Bottom
        shellBottom();
        shellBottomArches();
    }
}

module render_shell_lid(toPrint)
{
    if (!toPrint) {
        color([0.0,0.8,0.0,1]) shell_lid();
    } else {
        move([0,0,105]) xrot(180) shell_lid();
    }
}

module render_shell_dot(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) move([0,-44 + 25,105.5]) xrot(180) shell_dot();
    } else {
        shell_dot();
    }
}

module render_shell_supports(toPrint)
{
    if (toPrint) {
        move([0,-83,9.5]) cuboid([23,20,19]);
    }
}

module render_shell_screws(toPrint)
{
    if (!toPrint) {
        move([48.5,56,-3]) xrot(180) m3x10_screw();
        move([-48.5,56,-3]) xrot(180) m3x10_screw();
    }
}