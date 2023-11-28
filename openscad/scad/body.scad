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

module rear_flipper(dpt)
{
    move([86.5,0,0]) difference() { // Right
        move([0,83,0]) cuboid([48+23,8+27,dpt]); 
        move([-35.51,100.51,-dpt]) xrot(90) right_triangle([23,dpt*2,27+8]);
        move([+35.51,100.51,dpt]) xrot(90) zrot(180) right_triangle([48,dpt*2,27]);
    }
}

module front_flipper(dpt)
{
    move([70,-53.5 - 49,0]) {
        move([0,0,-(dpt/2)]) xrot(90) right_triangle([52,dpt,11]);
        move([26,16,0]) cuboid([52,32,dpt]);
        move([0,32,(dpt/2)]) yrot(180) xrot(90) right_triangle([55,dpt,43]);
        move([-70,32,(dpt/2)]) xrot(-90) right_triangle([122,dpt,57]);
    }
}

module head(dpt)
{
    hull() {
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

module body_platform(dpt)
{
    move([0,0,-(dpt/2)]) {
        rotate([0,0,18+180]) cyl(h=dpt, d=80*2, $fn=5); // Circumcircle radius of 79.96mm = side of 94mm
        move([0,22,0]) cuboid([244,87,dpt]);

        // Front of back leg slope to body
        move([73,-21.5,-(dpt/2)]) xrot(90) right_triangle([49,dpt,5]);
        yrot(180) move([73,-21.5,-(dpt/2)]) xrot(90) right_triangle([49,dpt,5]);

        // Front part of body/legs
        front_flipper(dpt); // Left
        yrot(180) front_flipper(dpt); // Right

        // Rear part of body/legs
        rear_flipper(dpt); // Left
        yrot(180) rear_flipper(dpt); // Right

        // Head
        head(dpt);
    }
}

module wheel_cutouts(dpt)
{
    move([+90,25.5,-(dpt/2)]) cuboid([60,76,dpt*2], chamfer=2);
    move([-90,25.5,-(dpt/2)]) cuboid([60,76,dpt*2], chamfer=2);
}

module render_body(crend, toPrint)
{
    difference() {
        body_platform(10);
        wheel_cutouts(10);
    }
}