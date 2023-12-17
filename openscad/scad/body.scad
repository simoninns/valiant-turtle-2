/************************************************************************

    body.scad
    
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

include <motor_bay.scad>
include <threaded_inserts.scad>

module body_profile(loc)
{
    move(loc) {
        move([0,0,-1.5]) cyl(h=3,d=3,chamfer2=1);
    }
}

// Internal back profile
module body_profile_intbk(loc)
{
    move(loc) {
        move([0,0,-1.5]) cuboid([3,3,3], chamfer=1, edges=EDGE_TOP_BK);
    }
}

// Internal front profile
module body_profile_intfr(loc)
{
    move(loc) {
        move([0,0,-1.5]) cuboid([3,3,3], chamfer=1, edges=EDGE_TOP_FR);
    }
}

module body_lip_profile(loc1, loc2)
{
    hull() {
        move(loc1) {
            move([0,0,-6.5]) cyl(h=7,d=3);
        }

        move(loc2) {
            move([0,0,-6.5]) cyl(h=7,d=3);
        }
    }
}

module body_lip_profile_int(loc1, loc2)
{
    hull() {
        move(loc1) {
            move([0,0,-6.5]) cuboid([3,3,7]);
        }

        move(loc2) {
            move([0,0,-6.5]) cuboid([3,3,7]);
        }
    }
}

module body_platform()
{
    pointA = [1.5, 67.5 - 4, 0];
    pointB = [53, 67.5 - 4, 0];
    pointC = [74.5, 98 - 2, 0];
    pointD = [120.5, 72.5, 0];
    pointE = [120.5,-20,0];
    pointF = [72.5,-24.5,0];

    pointG = [52.5, -39, 0];
    pointH = [120.5, -71.5, 0];
    pointI = [120.5, -101, 0];
    pointJ = [73, -111.5, 0];
    pointK = [15, -64, 0];
    pointL = [1.5, -64, 0];

    // Body top surface -----------------------------------
    // Middle of body
    hull() {
        body_profile(pointB);
        body_profile(pointF);
        body_profile(pointG);
        body_profile(pointK);
        body_profile_intfr(pointL);
        body_profile_intbk(pointA);
    }

    // Rear flipper
    hull() {
        body_profile(pointB);
        body_profile(pointC);
        body_profile(pointD);
        body_profile(pointE);
        body_profile(pointF);
    }

    // Front flipper
    hull() {
        body_profile(pointG);
        body_profile(pointH);
        body_profile(pointI);
        body_profile(pointJ);
        body_profile(pointK);
    }

    // Edge lip -------------------------------------------
    body_lip_profile(pointA, pointB);
    body_lip_profile(pointB, pointC);
    body_lip_profile(pointC, pointD);
    body_lip_profile(pointD, pointE);
    body_lip_profile(pointE, pointF);
    body_lip_profile(pointF, pointG);
    body_lip_profile(pointG, pointH);
    body_lip_profile(pointH, pointI);
    body_lip_profile(pointI, pointJ);
    body_lip_profile(pointJ, pointK);
    body_lip_profile(pointK, pointL);
    body_lip_profile_int(pointL, pointA);

    // Reenforcements -------------------------------------
    //move([19,12,-6.5]) cuboid([4,100,7]); // Back
    move([26.5,-39,-6.5]) cuboid([53,4,7]); // Front cross
    move([26,-56,-6.5]) cuboid([4,33.5,7]); // Front

    // Wheel bay reenforcements
    move([88,68.5,-4]) cuboid([65,2,4]);
    move([88,-15.5,-4]) cuboid([66,2,4], chamfer=0.5, edges=EDGES_Z_ALL);
}

module body_joiners_left()
{
    difference() {
        move([6, 44,-6]) cuboid([10,8,8]);
        move([4, 44,-6]) xcyl(h=9,d=5);
    }
}

module body_joiners_left_clearance()
{
    move([0, 44,-6]) xcyl(h=9,d=5);

    // Holes for right screws
    move([0,-33,-6]) xcyl(h=9,d=3.5);
    move([0,10,-6]) xcyl(h=9,d=3.5);

    // Additional screw head clearance against body
    move([-9,-33,-6]) xcyl(h=12,d=7);
    move([-9,10,-6]) xcyl(h=12,d=7);
}

module body_joiners_left_inserts()
{
    move([0, 44,-6]) yrot(90) insertM3x57();
}

module body_joiners_right()
{
    difference() {
        move([6,-33,-6]) cuboid([10,8,8]);
        move([4,-33,-6]) xcyl(h=8,d=5);
    }

    difference() {
        move([6,10,-6]) cuboid([10,8,8]);
        move([4,10,-6]) xcyl(h=8,d=5);
    }
}

module body_joiners_right_clearance()
{
    move([4,-33,-6]) xcyl(h=9,d=5);
    move([4,10,-6]) xcyl(h=9,d=5);

    // Hole for left screw
    move([4, 44,-6]) xcyl(h=9,d=3.5);

    // Additional screw head clearance against body
    move([9, 44,-6]) xcyl(h=12,d=7);
}

module body_joiners_right_inserts()
{
    move([0,-33,-6]) yrot(-90) insertM3x57();
    move([0,10,-6]) yrot(-90) insertM3x57();
}

module head_clearance()
{
    // Clear head attachment area
    move([0,-70,-8.01]) cuboid([43,45,10]);
}

module wheel_cutout()
{
    move([+88,25.75,-4]) cuboid([62,58.5,18]);
    move([+89,53.5,-4]) cuboid([49+2,11,18], chamfer=4);

    // Back of motor
    move([51.5,29,-6]) cuboid([13,44,50]);

    // Additional wheel clearance
    move([113,51.5,-4]) cuboid([12,11,18]);
}

module wheel_cutout_holes()
{
    move([0,0,5]) {
        move([59.5 + 2.5,-7.5,-7]) xrot(180) cyl(h=8,d=3.5);
        move([116.5 - 2.5,-7.5,-7]) xrot(180) cyl(h=8,d=3.5);

        // Back
        move([59.5 + 2.5,62,-7]) xrot(180) cyl(h=8,d=3.5);
        move([116.5 - 2.5,62,-7]) xrot(180) cyl(h=8,d=3.5);   
    }

    move([0,0,9 - 1.5]) {
        move([59.5 + 2.5,-7.5,-8]) xrot(180) cyl(h=4,d=7);
        move([116.5 - 2.5,-7.5,-8]) xrot(180) cyl(h=4,d=7);

        // Back
        move([59.5 + 2.5,62,-8]) xrot(180) cyl(h=4,d=7);
        move([116.5 - 2.5,62,-8]) xrot(180) cyl(h=4,d=7);   
    }
}

module wheel_cutout_supports()
{
    move([0,0,9 - 1.5]) {
        move([59.5 + 2.5,-7.5,-10]) xrot(180) cyl(h=4,d=8);
        move([116.5 - 2.5,-7.5,-10]) xrot(180) cyl(h=4,d=8);

        // Back
        move([59.5 + 2.5,62,-10]) xrot(180) cyl(h=4,d=8);
        move([116.5 - 2.5,62,-10]) xrot(180) cyl(h=4,d=8);   
    }
}

module shell_mounts()
{
    // M3 screw holes back
    move([(97/2),65 - 9,-5]) zcyl(h=20, d=3.5);
    move([-(97/2),65 - 9,-5]) zcyl(h=20, d=3.5);
}

module head_mounts()
{
     // M3 screw holes
    move([12,-58,-5]) zcyl(h=20, d=3.1);
    move([-12,-58,-5]) zcyl(h=20, d=3.1);
}

module pen_hole()
{
    // Hole for pen
    move([0,29,20]) zcyl(h=80, d=16);
    move([0,29,3.5]) cyl(h=10, d=16+4, chamfer1=2);
}

module pen_hole_lip()
{
    // Lip around the pen hole
    difference() {
        move([0,29,-5]) zcyl(h=10, d=16+5);
        move([0,29,20]) zcyl(h=80, d=16);
        move([-9,29,-5]) cuboid([22,22,12]);
    }
}

module pcb_mount_holes()
{
    move([0,0,0]) {
        // Front
        move([60,-20,0]) cyl(h=10, d=3.5);
        move([-60,-20,0]) cyl(h=10, d=3.5);
        
        // Back
        move([7,52,0]) cyl(h=10, d=3.5);
        move([-7,52,0]) cyl(h=10, d=3.5);
    }
}

module body_right()
{
    // Right side (viewed from front)
    difference() {
        union() {
            body_platform();
            motor_bay_side_panels();
            pen_hole_lip();
            body_joiners_right();
            wheel_cutout_supports();
        }

        head_clearance();
        wheel_cutout();
        wheel_cutout_holes();
        shell_mounts();
        head_mounts();
        pen_hole();
        pcb_mount_holes();

        body_joiners_right_clearance();
    }
    body_joiners_right_inserts();
}

module body_left()
{
    // Left side (viewed from front)
    difference() {
        union() xflip() {
            body_platform();
            motor_bay_side_panels();
            pen_hole_lip();
            body_joiners_left();
            wheel_cutout_supports();
        }

        head_clearance();
        wheel_cutout();
        xflip() wheel_cutout_holes();
        xflip() wheel_cutout();
        shell_mounts();
        head_mounts();
        pen_hole();
        pcb_mount_holes();

        body_joiners_left_clearance();
    }
    body_joiners_left_inserts();
}

module render_body_right(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            body_right();
        }
    } else {
        xrot(180) zrot(-90) body_right();
    }
}

module render_body_left(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            body_left();
        }
    } else {
        xrot(180) zrot(90) body_left();
    }
}

module body_left_screws()
{
    move([-3,-33,-6]) yrot(-90) m3x10_screw();
    move([-3,10,-6]) yrot(-90) m3x10_screw();
}

module render_body_left_screws(crend, toPrint)
{
    if (!toPrint) {
        body_left_screws();
    }
}

module body_right_screws()
{
    move([3,44,-6]) yrot(90) m3x10_screw();
}

module render_body_right_screws(crend, toPrint)
{
    if (!toPrint) {
        body_right_screws();
    }
}