/************************************************************************

    leds.scad
    
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

module led_5mm()
{
    move([0,0,4.5]) {
        // LED Body
        color([1,0,0,1]) {
            hull() {
            move([0,0,(8.6/2) - (4.9/2)]) staggered_sphere(d=4.9, $fn=16);
            move([0,0,-1.4]) cyl(h=8.6 - (4.9/2), d=4.9);
            }

            difference() {
                move([0,0,-4]) cyl(h=1,d=5.8);
                move([3.5,0,-4]) cuboid([2,10,2]);
            }
        }

        // LED legs
        color([0.7,0.7,0.7,1]) {
            move([-1,0,-5]) cuboid([0.5,0.5,8]);
            move([1,0,-5]) cuboid([0.5,0.5,8]);
        }
    }
}

module led_holder()
{
    difference() {
        union() {
            move([0,0,0.5]) cyl(h=1,d=10, chamfer1=0.5);
            move([0,0,3]) cyl(h=5,d=8);
        }
        move([0,0,3]) cyl(h=10,d=5);
    }
}

module render_led_holders(crend, toPrint)
{
    if(!toPrint) {
        color([0.2,0.2,0.2,1]) {
            move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([16.5,0,0]) yrot(270) led_holder();
            xflip() move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([16.5,0,0]) yrot(270) led_holder();
        }
    } else {
        led_holder();
        //move([0,0,6.4]) xrot(180) led_5mm();
    }
}

module render_leds(crend, toPrint)
{
    if(!toPrint) {
        move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) yrot(90) led_5mm();
        xflip() move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) yrot(90) led_5mm();
    }
}