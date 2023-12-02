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

// Cut a slot in the bottom shell front for the body's head
module headCutout()
{
    move([0,-1,-14]) {
        hull() {
            move([0,119.5 - 210,0]) {
                cuboid([44,65,10]);
                move([0,-32.5,-(10/2)]) xrot(90) right_triangle([21.5,10,21.5]);
                yrot(180) move([0,-32.5,-(10/2)]) xrot(90) right_triangle([21.5,10,21.5]);
            }

            move([0,119.5 - 210,15]) {
                cuboid([23,65,20]);
                move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
                yrot(180) move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
            }
        }
    }
}

module wheelArchBase()
{
    // Wheel arch base is 3mm wide (rest of shell is 2mm)
    difference() {
        hull() {
            move([71,-15,-7.5]) zcyl(h=3,d=3,$fn=16);
            move([120.5,-15,-7.5]) zcyl(h=3,d=3,$fn=16);
        }

        // Trim the end to make it flush with the shell
        move([65,-15,-7.5]) yrot(40) cuboid([10,10,20]);
    }

    hull() {
        move([0,62,-7.5]) zcyl(h=3,d=3,$fn=16);
        move([120.5,62,-7.5]) zcyl(h=3,d=3,$fn=16);
    }

    hull() {
        move([120.5,-15,-7.5]) zcyl(h=3,d=3,$fn=16);
        move([120.5,62,-7.5]) zcyl(h=3,d=3,$fn=16);
    }
}

module wheelArch()
{
    // Plot the side of the shell and cutout the wheel arch space
    difference() {
        union() {
            irrPentagonBottom(4);
            wheelArchBase();
        }

        // Cut space for the wheel arch
        move([80,23.5,20]) cuboid([78 - 0,80 - 6,60]);
    }

    // Render the wheelcover and use the pentagon to clip the inside edge
    difference() {
        wheelCover();
        move([-1,0,2]) irrPentagonBottom(4);
    }

    // Render some lips to help alignment with the body
    // Note: This is just for test printing and isn't correct
    move([119.5,10,-11]) cuboid([1,20,4]); 
    move([119.5,10+30,-11]) cuboid([1,20,4]);
    move([100,-14,-11]) cuboid([20,1,4]); 
    move([100,61,-11]) cuboid([20,1,4]); 
}

module wheelCover()
{
    move([0,23.5,-8]) {
        // Point cloud for the wheel arch (see doc/wheel_arch_points.jpg)
        pointA = [73.5,-38.5,2];
        pointB = [120.5,-38.5,2];
        pointC = [120.5,38.5,2];
        // pointD unused
        pointE = [120.5,7.5,22.5];
        pointF = [94,-38.5,13.5];
        pointG = [94,7.5,33.5];
        pointH = [94,-38.5,29.5];
        pointI = [94,7.5,49.5];
        pointJ = [71.0,38.5,32.5];
        pointK = [71.0,38.5,23];
        pointL = [48,38.5,2];

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
                zcyl(h=10, d=7);
                move([-3,6.5,-3.5]) cuboid([12,1,3]);
            }
        }

        // M3 screw hole
        zcyl(h=12, d=2.5);
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

module front_screw_mount()
{
    move([0,-93 + 3,25]) {
        difference() {
            hull() {
                zcyl(h=10, d=7);
                move([0,5,-3.5]) cuboid([26.5,1,3]);
            }

            // M3 screw hole
            zcyl(h=12, d=2.5);
        }
    }
}

module shellBottom()
{
    move([0,1.5,9]) difference() {
        union() {
            irrPentagonBottom(0);
            
            difference() {
                union() {
                    irrPentagonBottom(2);
                    irrPentagonBottom(3);
                }
                
                // Head cutout
                headCutout();
            }

            // Wheel arches
            wheelArch();
            xflip() wheelArch();
        }

        // Slice the bottom of the shell to make it flush with the body
        move([0,0,-29]) cuboid([200,200,40]);
    }

    // Render front and back screw mounts
    front_screw_mount();
    back_screw_mounts();          
}

// Note: From edge to edge of the wheel covers, the shell is 244mm wide
// The plastic is 3mm thick around the base of the wheel covers but the rest
// of the shell is 2mm thick
module render_shell_bottom(crend, toPrint)
{
    color([0,0.8,0,1]) shellBottom();
}
