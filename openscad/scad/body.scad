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

include <logotype.scad>

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
    move([0,-44,-6]) xcyl(h=9,d=3.5);
    move([0,13,-6]) xcyl(h=9,d=3.5);

    // Make a channel for the screwdriver
    move([-16,-44,-10]) xcyl(h=26,d=5);
}

module body_joiners_left_inserts()
{
    move([0, 44,-6]) yrot(90) insertM3x57();
}

module body_joiners_right()
{
    difference() {
        move([6,-44,-6]) cuboid([10,8,8]);
        move([4,-44,-6]) xcyl(h=8,d=5);
    }

    difference() {
        move([6,13,-6]) cuboid([10,8,8]);
        move([4,13,-6]) xcyl(h=8,d=5);
    }
}

module body_joiners_right_clearance()
{
    move([4,-44,-6]) xcyl(h=9,d=5);
    move([4,13,-6]) xcyl(h=9,d=5);

    // Hole for left screw
    move([4, 44,-6]) xcyl(h=9,d=3.5);
}

module body_joiners_right_inserts()
{
    move([0,-44,-6]) yrot(-90) insertM3x57();
    move([0,13,-6]) yrot(-90) insertM3x57();
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
    move([0,29,20]) cyl(h=80, d=16, $fn=8);
    move([0,29,3.5]) cyl(h=10, d=16+4, chamfer1=2, $fn=8);
}

module pen_hole_lip()
{
    // Lip around the pen hole
    difference() {
        move([0,29,-5]) cyl(h=10, d=16+5, $fn=8);
        move([0,29,20]) cyl(h=80, d=16, $fn=8);
        move([-9,29,-5]) cuboid([22,22,12]);
    }
}

module pen_hole_key()
{
    move([2.5/2,29 + 8,-5.75]) cuboid([5/2,2,8.5]);
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

module pen_servo_mount_holes()
{
    // M3 screw holes
    move([38.5,49.5,-3.75]) cyl(h=8,d=5);
    move([38.5,16.5,-3.75]) cyl(h=8,d=5);
}

module pen_servo_mount_material()
{
    move([38.5,49.5,-5]) cyl(h=10,d=8, $fn=8);
    move([38.5,16.5,-5]) cyl(h=10,d=8, $fn=8);
}

module pen_servo_mount_inserts()
{
    move([38.5,49.5,0]) insertM3x57_th();
    move([38.5,16.5,0]) insertM3x57_th();
}

module battery_access_hole()
{
    move([0,-19,0]) cuboid([79+2,36,22], chamfer=1, edges=EDGES_Z_ALL);
    move([0,-1,0]) cuboid([30,20,22], chamfer=1, edges=EDGES_Z_ALL);

    // M3 Mounting screw holes
    move([44.5,-19,-2]) cyl(h=8,d=3.5);
    move([-44.5,-19,-2]) cyl(h=8,d=3.5);

    // Battery cover lip
    move([0,-37,-2]) xrot(45) cuboid([60+1,2,2]);
    move([0,-37.5,-0.75]) cuboid([60+1,2,2.5]);
}

module control_panel_hole()
{
    move([-23.5,29,-2]) cuboid([21,30,12], chamfer=1, edges=EDGES_Z_ALL);
}

module control_panel_surround()
{
    move([-23.5,29,-4]) {
        difference() {
            cuboid([21+2,30+2,2], chamfer=1, edges=EDGES_Z_ALL);
            cuboid([21,30,14], chamfer=1, edges=EDGES_Z_ALL);
        }
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
            pen_servo_mount_material();
        }

        head_clearance();
        wheel_cutout();
        wheel_cutout_holes();
        shell_mounts();
        head_mounts();
        pen_hole();
        pcb_mount_holes();
        pen_servo_mount_holes();
        body_joiners_right_clearance();
        battery_access_hole();
    }

    body_joiners_right_inserts();
    pen_servo_mount_inserts();
    pen_hole_key();
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
            pen_servo_mount_material();
        }

        head_clearance();
        wheel_cutout();
        xflip() wheel_cutout_holes();
        xflip() wheel_cutout();
        shell_mounts();
        head_mounts();
        pen_hole();
        pcb_mount_holes();
        xflip() pen_servo_mount_holes();
        move([-70,-75,-2.501]) zrot(39) logotype();
        body_joiners_left_clearance();
        battery_access_hole();
        control_panel_hole();
    }
    body_joiners_left_inserts();
    xflip() pen_servo_mount_inserts();
    xflip() pen_hole_key();
    control_panel_surround();
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
    move([-3,-44,-6]) yrot(-90) m3x10_screw();
    move([-3,13,-6]) yrot(-90) m3x10_screw();
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