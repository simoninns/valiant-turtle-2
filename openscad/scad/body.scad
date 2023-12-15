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

module body_profile(loc)
{
    move(loc) {
        move([0,0,-1.5]) cyl(h=3,d=3,chamfer2=1);
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

module body_platform()
{
    pointA = [0, 67.5 - 4, 0];
    pointB = [53, 67.5 - 4, 0];
    pointC = [74.5, 98 - 2, 0];
    pointD = [120.5, 72.5, 0];
    pointE = [120.5,-20,0];
    pointF = [72.5,-24.5,0];

    pointG = [52.5, -39, 0];
    pointH = [120.5, -71.5 + 3, 0];
    pointI = [120.5, -101 + 3, 0];
    pointJ = [74, -111.5 + 5, 0];
    pointK = [15, -64, 0];
    pointL = [0, -64, 0];

    // Body top surface -----------------------------------
    // Middle of body
    hull() {
        body_profile(pointB);
        body_profile(pointF);
        body_profile(pointG);
        body_profile(pointK);
        body_profile(pointL);
        body_profile(pointA);
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

    // Reenforcements -------------------------------------
    move([19,12,-6.5]) cuboid([4,100,7]);
    move([19,-39,-6.5]) cuboid([70,4,7]);
    move([26,-56,-6.5]) cuboid([4,31,7]);
}

module head_clearance()
{
    // Clear head attachment area
    move([0,-70,-8.01]) cuboid([43,40,10]);
}

module wheel_cutout()
{
    move([+88,25.75,-4]) cuboid([62,58.5,18]);
    move([+89,53.5,-4]) cuboid([49,11,18], chamfer=4);
    
}

module wheel_cutout_holes()
{
    move([0,0,5]) {
        move([59.5 + 2.5,-7.5,-7]) xrot(180) cyl(h=8,d=3.5);
        move([116.5 - 2.5,-7.5,-7]) xrot(180) cyl(h=8,d=3.5);

        // Back
        move([59.5 + 2.5,59,-7]) xrot(180) cyl(h=8,d=3.5);
        move([116.5 - 2.5,59,-7]) xrot(180) cyl(h=8,d=3.5);   
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
    move([0,29,20]) zcyl(h=80, d=14);
}

module pcb_mount_holes()
{
    move([0,0,0]) {
        move([60,-20,0]) cyl(h=10, d=3.5);
        move([-60,-20,0]) cyl(h=10, d=3.5);
        move([0,52,0]) cyl(h=10, d=3.5);
    }
}

module body()
{
    difference() {
        union() {
            body_platform();
            xflip() body_platform();
        }

        head_clearance();
        wheel_cutout();
        wheel_cutout_holes();
        xflip() wheel_cutout();
        shell_mounts();
        head_mounts();
        pen_hole();
        pcb_mount_holes();
    }

    motor_bay_shape1();
    xflip() motor_bay_shape1();
}

module render_body(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            body();
        }
    } else {
        xrot(180) body();
    }
}