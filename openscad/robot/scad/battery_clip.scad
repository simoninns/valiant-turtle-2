/************************************************************************

    battery_clip.scad
    
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

// Battery contact (basic shape)
module battery_contact()
{
    difference() {
        union() {
            // Main body round lower part
            difference() {
                cyl(h=0.3, d=18.5);
                move([0,18.5/2,0]) cuboid([18.5+1,18.5, 1]);
            }

            // Main box rectangular upper part
            move([0,0+7/2,0]) cuboid([18.5,7, 0.3]);

            // Clips
            move([(8.25 - 0.5),6 - 5,0 +0.6]) zrot(180) right_triangle(size=[2,2,1.5], orient=ORIENT_X, center=true);
            move([-(8.25 - 0.5),6 - 5,0 +0.6]) zrot(180) right_triangle(size=[2,2,1.5], orient=ORIENT_X, center=true);

            // Soldering tag
            move([0,-14,0]) cuboid([5,1, 0.3]);
            move([0,-13.75+0.1,-0.5]) cuboid([5,0.3, 1.25]);

            move([0,-16.75,-1.25]) cuboid([5,6.5, 0.3]);
            move([0,-3,-1.25]) cyl(h=0.3, d=5);
        }

        move([0,-3,-1.25]) cyl(h=2, d=2.25);
    }
}

module battery_contact_negative()
{
    difference() {
        battery_contact();
        move([0,-1,0]) cyl(h=1,d=3);
    }
    
    // Spring 12mm high, 6mm,
    move([0,-1,6]) cyl(h=12, d=6); 

}

module battery_contact_positive()
{
    difference() {
        battery_contact();
        move([0,-1,0]) cyl(h=1,d=10);
    }

    move([0,-1,0]) {
        difference() {
            hull() {
                move([0,0,2]) cyl(h=0.3, d=6);
                move([0,0,0]) cyl(h=0.3,d=10);
            }

            move([0,0,-0.3]) hull() {
                move([0,0,2]) cyl(h=0.3, d=6);
                move([0,0,0]) cyl(h=0.3,d=10);
            }
        }
    }
}


module battery_contact_mask()
{
    cuboid([19,16,0.5]);

    // Centre clearance
    move([0,1,-2]) cuboid([11.5,14,4]);

    // Back centre clearance
    move([0,-3,2]) cuboid([5.5,10,4]);
    move([0,2,2]) zrot(45) cuboid([4,4,4]);
    move([0,-6,2]) cuboid([5.5,14,2]);

    // Tab clearance
    move([0,-10,0]) cuboid([5.5,16,0.5]);

    // Fastening clip channels
    move([(8.25 - 0.5),0.75,-0.75]) cuboid([2.5,3,1.25]);
    move([-(8.25 - 0.5),0.75,-0.75]) cuboid([2.5,3,1.25]);

    move([(8.25 - 0.5),5,-0.5]) cuboid([2.5,6,0.75]);
    move([-(8.25 - 0.5),5,-0.5]) cuboid([2.5,6,0.75]);
}


// 18650 x2 Battery clip
module battery_clip_body()
{
    difference() {
        union() {
            move([0,0,3.5+3]) cuboid([43,76,13], chamfer=0.5);
            move([0,+36.25,7+4]) cuboid([43,3.5,12], chamfer=0.5);
            move([0,-36.25,7+4]) cuboid([43,3.5,12], chamfer=0.5);
        }

        // Battery recesses
        move([-10.25,0,8.5]) ycyl(h=69,d=19);
        move([+10.25,0,8.5]) ycyl(h=69,d=19);

        // Screw recesses
        move([0,-(55.5/2),7.5]) cyl(h=13,d1=8, d2=12);
        move([0,+(55.5/2),7.5]) cyl(h=13,d1=8, d2=12);

        // Screw holes
        move([0,-(55.5/2),0]) cyl(h=8,d=3.5);
        move([0,+(55.5/2),0]) cyl(h=8,d=3.5);

        // Positive markers
        move([17,38.25,8]) {
            cuboid([5,1,1]);
            cuboid([1,1,5]);
        }

        move([-17,-38.25,8]) {
            cuboid([5,1,1]);
            cuboid([1,1,5]);
        }

        // Negative markers
        move([-17,38.25,8]) {
            cuboid([5,1,1]);
        }

        move([+17,-38.25,8]) {
            cuboid([5,1,1]);
        }

        // Orientation tab
        move([-18.75 + 1.5,-38.25 + 2,0]) cyl(h=1.1,d1=3, d2=2);

        // Side cut-outs to help get the batteries in and out
        move([0,18,11]) cuboid([48,22,9], chamfer=2);
        move([0,-18,11]) cuboid([48,22,9], chamfer=2);

        // Wiring gully
        move([0,39.5,6.5]) cuboid([20,4,4], chamfer=1);
        move([0,-39.5,6.5]) cuboid([20,4,4], chamfer=1);
    }
}

module battery_clip()
{
    difference() {
        battery_clip_body();

        xrot(90) {
            move([10.25,9.01,36.25]) battery_contact_mask();
            move([-10.25,9.01,36.25]) battery_contact_mask();
        }

        xrot(90) {
            move([10.25,9.01,-36.25]) yrot(180) battery_contact_mask();
            move([-10.25,9.01,-36.25]) yrot(180) battery_contact_mask();
        }
    }
}

module battery_clips()
{
    move([-1,0,0]) {
        xrot(-90) zrot(180) {
            move([10.25,9,-36.25]) battery_contact_positive();
            move([-10.25,9,-36.25]) battery_contact_negative();
        }

        xrot(90) zrot(0) {
            move([10.25,9,-36.25]) battery_contact_positive();
            move([-10.25,9,-36.25]) battery_contact_negative();
        }
    }
}

module render_battery_clip(toPrint)
{
    if (!toPrint) {
        color([0.2, 0.2, 0.2]) move([0,-12.5,9]) {
            move([0,-2.5,0]) yrot(90) xrot(90) zrot(180) battery_clip();
            move([0,+2.5,0]) yrot(90) xrot(-90) zrot(180) battery_clip();
        }
    } else {
        battery_clip();
    }
}

module render_battery_clip_contacts(toPrint)
{
    if (!toPrint) {
        color([0.8, 0.8, 0.8]) move([0,-12.5,10]) {
            move([0,-2.5,0]) yrot(90) xrot(90) zrot(180) battery_clips();
            move([0,+2.5,0]) yrot(90) xrot(-90) zrot(180) battery_clips();
        }
    }
}