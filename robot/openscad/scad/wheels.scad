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

include <threaded_inserts.scad>

module wheel_body()
{
    // Main wheel body
    owd = 52;
    iwd = 47;

    move([0.5,0,0]) {
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
            move([7,0,0]) yrot(-90) cyl(h=8,d=22, chamfer=0.5);
            move([8,0,1]) cuboid([6,7,20], chamfer=0.5);
        }

        // Setting screw hole
        move([8,0,6]) xrot(180) cyl(h=12,d=3.25);

        // Threaded insert slot
        move([8,0,7.1]) xrot(180) cyl(h=8,d=5);
    }

    // Add in the screw insert
    difference() {
        move([8,0,11]) insertM3x57();
        
        // Setting screw hole
        move([8,0,6]) xrot(180) cyl(h=12,d=3.25);
    }
}

module wheel_hub_decoration()
{
    for (rot = [0:360/12: 360-1]) {
        xrot(rot) hull() {
            move([2,0,14]) yrot(-90) cyl(h=10,d=3, $fn=16);
            move([2,0,21.5]) yrot(-90) cyl(h=10,d=3, $fn=16);
        }

        move([-0.0,0,0]) xrot(rot) hull() {
            move([5.25,0,14]) yrot(-90) cyl(h=4,d=5, chamfer=1, $fn=16);
            move([5.25,0,21.5]) yrot(-90) cyl(h=4,d=5, chamfer=1, $fn=16);
        }
    }
}

module tire()
{
    // O-ring Tire - R31 - AS 568 225 - ID=47.22, OD=54.28, section=3.53
    move([3.5,0,0]) yrot(90) torus(id=47.22, od=54.28);
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
                move([5,0,0]) yrot(-90) cyl(h=20,d=5);
                move([5,0,3.25 - 0.75]) yrot(-90) cuboid([1,6,20]);
            }

            wheel_hub_decoration();
        }
    }
}

module render_wheels(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) {
            move([106.5,64-35,-6]) xrot(90) wheel();
            xflip() move([106.5,64-35,-6]) xrot(90) wheel();
        }
    } else {
        move([0,0,6.25]) yrot(90) wheel();
    }
}

module render_turning_circle(toPrint)
{
    if (!toPrint) {
        // Render the turning circle
        move([0,64-35,-34]) tube(h=1,od=223.5, id=221.5-5, $fn=100);
        move([0,64-35,-34]) tube(h=1,od=280, id=280-3);

        // Show the rotational axis across the pen
        move([0,64-35,-33]) cuboid([300,1,0.25]);
    }
}

module render_tires(toPrint)
{
    if (!toPrint) {
        color([0.4,0.4,0.4,1]) {
            move([106.5,64-35,-6]) tire();
            xflip() move([106.5,64-35,-6]) tire();
        }
    }
}