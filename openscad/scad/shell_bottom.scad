/************************************************************************

    shell.scad
    
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
    difference() {
        union() {
            irrPentagonBottom(4);
            wheelArchBase();
        }

        // Cut space for the wheel arch
        move([80,23.5,20]) cuboid([78 - 0,80 - 6,60]);
    }

    wheelCover();
}

// Note: From edge to edge of the wheel covers, the shell is 244mm wide
// The plastic is 3mm thick around the base of the wheel covers but the rest
// of the shell is 2mm thick
module shell()
{
    shellBottom();
}

module render_shell_bottom(crend, toPrint)
{
    color([0,0.8,0,1]) shell();
}


// ---------------------------------------------------------------------------------


// module wheelCoverBase()
// {
//     move([84.25 ,25,1.5]) {
//         difference() {
//             cuboid([75.5,80,3], fillet=1, edges=EDGES_Z_ALL, $fn=16);
//             cuboid([75.5-6,80-6,6]);
//             move([-26,0,0]) cuboid([30,74,6]);
//             move([-29.5,-32,0]) yrot(26) cuboid([30,20,20]);
//         }
//     }
// }

module wheelCover()
{
    move([0,23.5,-8]) {

        outer_x = 121 - 0.5;
        
        backinner_x = 47.5 + 0.5;
        backmid_x = backinner_x + 24;
        back_y = 39 - 0.5;
        backmid_z = 23;
        backtop_z = 23 + 9.5;
        
        frontinner_x = 73 + 0.5;
        frontmid_x = outer_x - 26.5;
        front_y = -39 + 0.5;
        frontbottom_z = 12.5 + 1;
        fronttop_z = frontbottom_z + 16.0;
        fronttopinner_z = fronttop_z+4;
        frontmidtop_z = fronttop_z+20;
        
        sidemid_z = 23;
        middle_y = front_y + 46.5 - 0.5;
        base_z = 2;


        // --------------------------------
        pointA = [frontinner_x,front_y,base_z];
        pointB = [outer_x,front_y,base_z];
        pointC = [outer_x,back_y,base_z];

        pointE = [outer_x,middle_y,sidemid_z];
        pointF = [frontmid_x,front_y,frontbottom_z];
        pointG = [frontmid_x,middle_y,fronttopinner_z];
        pointH = [frontmid_x,front_y,fronttop_z];
        pointI = [frontmid_x,middle_y,frontmidtop_z];
        pointJ = [backmid_x,back_y,backtop_z];
        pointK = [backmid_x,back_y,backmid_z];
        pointL = [backinner_x,back_y,base_z];

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
