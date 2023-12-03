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

module body_profile(loc)
{
    move(loc) {
        move([0,0,-1.5]) cyl(h=3,d=3,chamfer2=1);
    }
}

module lip_profile(loc1, loc2)
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

module head()
{
    dpt=10;

    move([0,0,-5]) hull() {
        move([0,119.5 - 210,0]) {
            cuboid([43,65,dpt]);
            move([0,-32.5,-(dpt/2)]) xrot(90) right_triangle([21.5,dpt,21.5]);
            yrot(180) move([0,-32.5,-(dpt/2)]) xrot(90) right_triangle([21.5,dpt,21.5]);
        }

        move([0,119.5 - 210,15]) {
            cuboid([22,65,20]);
            move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
            yrot(180) move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
        }
    }
}

module body_platform()
{
    pointA = [0, 67.5 - 4, 0];
    pointB = [53, 67.5 - 4, 0];
    pointC = [74.5, 98, 0];
    pointD = [120, 72.5, 0];
    pointE = [120,-20,0];
    pointF = [72.5,-24.5,0];
    pointG = [52.5, -39, 0];
    pointH = [120, -71.5, 0];
    pointI = [120, -101, 0];
    pointJ = [74, -111.5, 0];
    pointK = [15, -64, 0];
    pointL = [0, -64, 0];

    // Body top surface -----------------------------------------------------------------------------------------------
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

    // Edge lip -------------------------------------------------------------------------------------------------------
    lip_profile(pointA, pointB);
    lip_profile(pointB, pointC);
    lip_profile(pointC, pointD);
    lip_profile(pointD, pointE);
    lip_profile(pointE, pointF);
    lip_profile(pointF, pointG);
    lip_profile(pointG, pointH);
    lip_profile(pointH, pointI);
    lip_profile(pointI, pointJ);
    lip_profile(pointJ, pointK);
    lip_profile(pointK, pointL);
}

module wheel_cutout()
{
    move([+90,25,-(4)]) cuboid([60,76,6*2], chamfer=2);
}

module shell_mounts()
{
    // M3 screw holes back
    move([(97/2),65 - 9,-5]) zcyl(h=20, d=2.5);
    move([-(97/2),65 - 9,-5]) zcyl(h=20, d=2.5);

    // M3 screw hole front
    move([0,-90,15]) zcyl(h=20, d=2.5);
}

module render_body(crend, toPrint)
{
    difference() {
        union() {
            body_platform();
            xflip() body_platform();
            head();
        }
        //wheel_cutout();
        // shell_mounts();
    }
}