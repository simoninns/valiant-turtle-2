/************************************************************************

    wheels.scad
    
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
use <BOSL/nema_steppers.scad>

include <screws.scad>

module wheel_body()
{
    // Main wheel body
    owd = 52;
    iwd = 47;

    move([-3,0,0]) {
        move([-1.25,0,0]) yrot(-90) cyl(h=1, d=owd);
        move([0,0,0]) yrot(-90) cyl(h=1.5, d2=owd, d1=iwd);

        move([1,0,0]) xcyl(h=3.5, d=owd - 4);
        move([2,0,0]) yrot(-90) cyl(h=1.5, d1=owd, d2=iwd);
        move([3.25,0,0]) xcyl(h=1, d=owd);
    }
}

module wheel_hub()
{
    difference() {
        union() {
            move([6,0,0]) yrot(-90) cyl(h=12,d=22, chamfer=0.5);
            move([8,0,1]) cuboid([6,7,20], chamfer=0.5);
        }

        // Setting screw hole
        move([8,0,6]) xrot(180) cyl(h=12,d=3.25);

        // Threaded insert slot
        move([8,0,7+2]) xrot(180) cyl(h=8,d=4);
    }
    
    // Spacer
    move([15.5,0,0]) {
        difference() {
            xcyl(h=9,d=8);
            xcyl(h=10,d=6);
        }
    }
}

module wheel_hub_decoration()
{
    for (rot = [0:360/12: 360-1]) {
        xrot(rot) hull() {
            move([2,0,14]) yrot(-90) cyl(h=20,d=3, $fn=16);
            move([2,0,21.5]) yrot(-90) cyl(h=30,d=3, $fn=16);
        }

        move([-0.0,0,0]) xrot(rot) hull() {
            move([5.25,0,14]) yrot(-90) cyl(h=4,d=5, chamfer=1, $fn=16);
            move([5.25,0,21.5]) yrot(-90) cyl(h=4,d=5, chamfer=1, $fn=16);
        }
    }
}

// Tires consist of 2 o-rings
module tire()
{
    // O-ring Tire - R31 - AS 568 225 - ID=47.22, OD=54.28, section=3.53
    move([8.5,0,0]) yrot(90) torus(id=47.22, od=54.28);
}

module wheel()
{
    zrot(180) move([-5,0,0]) {
        difference() {
            union() {
                wheel_body();
                wheel_hub();
            }

            // Hub for D-shaped NEMA 17 5mm shaft (with 1mm D)
            difference() {
                move([5,0,0]) yrot(-90) cyl(h=20,d=5.25);
                move([5,0,3.25 - 0.5]) yrot(-90) cuboid([1,6,20]);
            }

            wheel_hub_decoration();
        }
    }
}

module render_wheel_left(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) {
            xflip() move([106.5 + 1.5,64-35,-6]) xrot(90) wheel();
        }
    } else {
        move([0,0,9.75]) yrot(90) wheel();
    }
}

module render_wheel_right(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) {
            move([106.5 + 1.5,64-35,-6]) xrot(90) wheel();
        }
    } else {
        move([0,0,9.75]) yrot(90) wheel();
    }
}

module render_turning_circle(toPrint)
{
    if (!toPrint) {
        // The wheels are 230mm apart (centre to centre):
        axel_length = 230;
        move([0,64-35,-34]) {
            difference() {
                cyl(h=1, r=(axel_length/2) + 0.5, $fn=200);
                cyl(h=2, r=(axel_length/2) - 0.5, $fn=200);
            }
        }

        move([0,0,0]) {
            move([axel_length/2,64-35,-34]) cuboid([1,300,1]);
            move([-(axel_length/2),64-35,-34]) cuboid([1,300,1]);
        }
        
        // Ball bearing caster
        move([0,64-35,-34]) tube(h=1,od=(138*2)+1, id=(138*2)-1, $fn=200);

        // Show the rotational axis across the pen
        move([0,64-35,-33]) cuboid([300,1,0.25]);
    }
}

module render_tire_left(toPrint)
{
    if (!toPrint) {
        color([0.4,0.4,0.4,1]) {
            xflip() move([106.5,64-35,-6]) tire();
        }
    }
}

module render_tire_right(toPrint)
{
    if (!toPrint) {
        color([0.4,0.4,0.4,1]) {
            move([106.5,64-35,-6]) tire();
        }
    }
}