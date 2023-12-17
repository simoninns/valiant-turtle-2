/************************************************************************

    wheels.scad
    
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
use <BOSL/nema_steppers.scad>

include <threaded_inserts.scad>

module wheel_body()
{
    // Main wheel body
    owd = 52;
    iwd = 47;

    move([0,0,0]) yrot(-90) cyl(h=0.5, d=owd);
    move([1,0,0]) yrot(-90) cyl(h=1.5, d2=owd, d1=iwd);

    move([2.25,0,0]) xcyl(h=3.5, d=owd - 4);
    move([3,0,0]) yrot(-90) cyl(h=1.5, d1=owd, d2=iwd);
    move([0.5 + 3.5,0,0]) xcyl(h=0.5, d=owd);
}

module wheel_hub()
{
    difference() {
        union() {
            move([7,0,0]) yrot(-90) cyl(h=7.5,d=22, chamfer=0.5);
            move([7.25,0,0]) cuboid([6,7,22], chamfer=0.5);
        }

        // Setting screw hole
        move([7.25,0,6]) xrot(180) cyl(h=12,d=3.25);

        // Threaded insert slot
        move([7.25,0,7.1]) xrot(180) cyl(h=8,d=5);
    }

    // Add in the screw insert
    difference() {
        move([7.25,0,11]) insertM3x57();
        
        // Setting screw hole
        move([7.25,0,6]) xrot(180) cyl(h=12,d=3.25);
    }
}

module wheel_hub_decoration()
{
    for (rot = [0:360/12: 360-1]) {
        xrot(rot) hull() {
            move([2,0,14]) yrot(-90) cyl(h=10,d=3, $fn=16);
            move([2,0,21.5]) yrot(-90) cyl(h=10,d=3, $fn=16);
        }

        xrot(rot) hull() {
            move([5.25,0,14]) yrot(-90) cyl(h=4,d=5, chamfer=1, $fn=16);
            move([5.25,0,21.5]) yrot(-90) cyl(h=4,d=5, chamfer=1, $fn=16);
        }

        move([-6.5,0,0]) xrot(rot) hull() {
            move([5.25,0,14]) yrot(-90) cyl(h=4,d=5, chamfer=1, $fn=16);
            move([5.25,0,21.5]) yrot(-90) cyl(h=4,d=5, chamfer=1, $fn=16);
        }
    }
}

module tire()
{
    // O-ring Tire - R31 - AS 568 225 - ID=47.22, OD=54.28, section=3.53
    move([3,0,0]) yrot(90) torus(id=47.22, od=54.28);
}

module wheel()
{
    zrot(180) move([-5,0,0]) difference() {
        union() {
            wheel_body();
            wheel_hub();
        }

        // Hub (shaft should be 5mm, but we use 5.5 to make an easy fit)
        move([5,0,0]) yrot(-90) cyl(h=20,d=5.5);

        wheel_hub_decoration();
    }
}

module render_wheels(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) {
            move([107,64-35,-6]) wheel();
            xflip() move([107,64-35,-6]) wheel();
        }
    } else {
        move([0,0,5.25]) yrot(90) wheel();
    }
}

module render_turning_circle(crend, toPrint)
{
    if (!toPrint) {
        // Render the turning circle
        move([0,64-35,-34]) tube(h=1,od=223.5, id=221.5-5, $fn=100);
        move([0,64-35,-34]) tube(h=1,od=280, id=280-3);

        // Show the rotational axis across the pen
        move([0,64-35,-34]) cuboid([300,1,1]);
    }
}

module render_tires(crend, toPrint)
{
    if (!toPrint) {
        color([0.4,0.4,0.4,1]) {
            move([107,64-35,-6]) tire();
            xflip() move([107,64-35,-6]) tire();
        }
    }
}