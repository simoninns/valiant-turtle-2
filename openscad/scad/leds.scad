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

module render_5mm_led()
{
    yrot(90) {
        color([1,0,0,1]) {
            staggered_sphere(d=5, $fn=16);
            move([0,0,2 - 7]) cyl(h=1,d=6);
            move([0,0,-2.5]) cyl(h=5,d=5);
        }

        color([0.7,0.7,0.7,1]) {
            move([-1,0,-5]) cyl(h=8,d=0.5);
            move([1,0,-5]) cyl(h=8,d=0.5);
        }
    }
}

module render_5mm_led_holder()
{
    yrot(90) {
        color([0.2,0.2,0.2,1]) difference() {
            union() {
                cyl(h=1,d=10, chamfer2=0.5);
                move([0,0,-2]) cyl(h=5,d=8);
            }
            move([0,0,-2]) cyl(h=10,d=5);
        }
    }
}

module led_and_holder_5mm()
{
    move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([16.5,0,0]) {
        render_5mm_led();
        render_5mm_led_holder();
    }
}

module render_leds(crend, toPrint)
{
    if(!toPrint) {
        led_and_holder_5mm();
        xflip() led_and_holder_5mm();
    }
}