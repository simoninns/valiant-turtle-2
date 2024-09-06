/************************************************************************

    eyes.scad
    
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

module eye_light_pipe()
{
    move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) yrot(90) {
        move([0,0,4.5]) {
            // Eyeball
            hull() {
                move([0,0,(8.6/2) - (4.9/2)]) staggered_sphere(d=4.9, $fn=16);
                move([0,0,-1.4]) cyl(h=8.6 - (4.9/2), d=4.9);
            }
        }
    }

    difference() {
        union() {
            hull() {
                move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) yrot(90) {
                    move([0,0,4.5]) {
                        move([0,0,-4]) cyl(h=1, d=4.9);
                    }
                }

                move([5,-126,5.5]) ycyl(h=0.25,d=4.9);
            }

            hull() {
                move([5,-126,5.5]) ycyl(h=0.25,d=4.9);
                move([5,-121,5.5]) cuboid([8,8,8], chamfer=1, edges=EDGES_Y_ALL);
            }
        }

        // Slot for LED
        move([5,-119.5,5.5]) ycyl(h=10,d=5.5);
    }
}

module eye_light_pipe_left()
{
    eye_light_pipe();

    // Tag to guide surround
    move([5,-122,1.5]) cuboid([1,3,2], chamfer=1, edges=EDGES_X_ALL);
}

module eye_light_pipe_right()
{
    xflip() {
        eye_light_pipe();

        // Tag to guide surround
        move([5,-122,1.5]) cuboid([1,3,2], chamfer=1, edges=EDGES_X_ALL);
    }
}

module eye_light_pipe_surround()
{
    difference() {
        union() {
            move([0,-120,5.5]) cuboid([20,5.75,10], chamfer=1, edges=EDGES_Y_ALL);
            move([0,-122,5.5]) cuboid([3,5.75,10]);

            // Standoff
            move([0,-120,10]) cuboid([10,5.75,10], chamfer=1, edges=EDGES_Y_ALL);
        }

        move([5,-120,5.5]) cuboid([8.25,10,8], chamfer=1, edges=EDGES_Y_ALL);
        move([-5,-120,5.5]) cuboid([8.25,10,8], chamfer=1, edges=EDGES_Y_ALL);

        move([5,-122,1]) cuboid([1.25,3,3]);
        move([-5,-122,1]) cuboid([1.25,3,3]);

        // Standoff slot
        move([0,-123,15.75]) cuboid([2.25,8,4]);
    }
}

module eye_surround()
{
    difference() {
        // Main body
        union() {
            difference() {
                union() {
                    move([0,0,0.5]) cyl(h=1,d=10, chamfer1=0.5);
                    move([0,0,2.25]) cyl(h=4,d=7);
                }
                move([0,0,3]) cyl(h=16,d=5);
            }
        }
    }
}

module render_eye_surround(toPrint)
{
    if(!toPrint) {
        color([0.2,0.2,0.2,1]) {
            move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([16.5,0,0]) yrot(270) {
                eye_surround();
            }
            xflip() move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([16.5,0,0]) yrot(270) {
                eye_surround();
            }
        }
    } else {
        move([0,0,0]) {
            move([0,0,0]) eye_surround();
        }
    }
}

module render_eye_light_pipe(toPrint)
{
    if(!toPrint) {
        color([0.9,0.9,0.9,1]) {
            eye_light_pipe_left();
            eye_light_pipe_right();
        }
    } else {
        move([-5 + 8,-5.5,-117]) xrot(-90) eye_light_pipe_left();
        move([+5 - 8,-5.5,-117]) xrot(-90) eye_light_pipe_right();
    }
}

module render_eye_light_pipe_surround(toPrint)
{
    if(!toPrint) {
        color([0.2,0.2,0.2,1]) eye_light_pipe_surround();
    } else {
        move([0,-5.5,-117.125]) xrot(-90) eye_light_pipe_surround();
    }
}

module render_leds(toPrint)
{
    if(!toPrint) {
        move([5,-116,5.5]) xrot(90) led_5mm();
        xflip() move([5,-116,5.5]) xrot(90)  led_5mm();
    }
}