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

module eye_light_pipe()
{
    move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) yrot(90) {
        move([0,0,4.5]) {
            // Eyeball
            hull() {
                move([0,0,(8.6/2) - (4.9/2)]) staggered_sphere(d=4.9, $fn=16);
                move([0,0,-0.4]) cyl(h=4, d=4.9);
            }
        }
    }

    hull() {
        move([-1,-120,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) yrot(90) {
            move([0,0,2]) cyl(h=0.25, d=4.9);
        }
        move([4,-123,5.5]) ycyl(h=0.25,d=5);
    }

    difference() {
        hull() {
            move([4,-123,5.5]) ycyl(h=0.25,d=5);
            move([5,-118,5.5]) cuboid([7,2,12], chamfer=0.5, edges=EDGES_Y_ALL);
        }

        // Slot for 5050 WS2812 LED
        move([5,-115.5,5.5]) cuboid([5.25+2,5,5.25+2], chamfer=1);

        // Slots to make clips more flexible
        move([-1,-120.5,-3.5 + 5]) {
            move([6,4-1,9-0.5]) cuboid([9,3.5,1], chamfer=0.5);
            move([6,4-1,-1 + 0.5]) cuboid([9,3.5,1], chamfer=0.5);
        }
    }

    // WS2812 Clips
    move([-1,-120,-3.5 + 5]) {
        // Top
        move([6,4,9.5]) cuboid([7,3.5,1], chamfer=0.5, edges=EDGES_TOP-EDGES_BACK);
        move([6,5.25,9]) cuboid([7,1,2], chamfer=0.5, edges=EDGES_X_ALL+EDGES_TOP);

        // Bottom
        move([6,4,-1.5]) cuboid([7,3.5,1], chamfer=0.5, edges=EDGES_BOTTOM-EDGES_BACK);
        move([6,5.25,-1]) cuboid([7,1,2], chamfer=0.5, edges=EDGES_X_ALL+EDGES_BOTTOM);
    }

    // Surround locator tabs
    move([0,-120,0]) {
        move([8.5,-0.25,5.5]) cuboid([3.5,2,2]);
    }
}

module eye_light_pipe_left()
{
    eye_light_pipe();
}

module eye_light_pipe_right()
{
    xflip() {
        eye_light_pipe();
    }
}

module eye_light_pipe_surround()
{
    move([0,-120,0]) {
        difference() {
            move([0,2.5,5.5]) cuboid([20,7,15], chamfer=1, edges=EDGES_Y_ALL);

            move([-5,2.5,5.5]) cuboid([7,9,12], chamfer=0.5, edges=EDGES_Y_ALL);
            move([+5,2.5,5.5]) cuboid([7,9,12], chamfer=0.5, edges=EDGES_Y_ALL);

            // Cable channel
            move([0,5,5.5]) cuboid([25,4.5,8]);

            // Guide slots
            move([10,-1.5,5.5]) cuboid([10,4.75,2.25]);
            move([-10,-1.5,5.5]) cuboid([10,4.75,2.25]);
        }

        // Seperator
        move([0,-3.75,5.5]) cuboid([2,10,15]);

        move([1,-0.75,-2]) zrot(-90) right_triangle(size=[8,8,1.5], orient=ORIENT_Z);
        xflip() move([1,-0.75,-2]) zrot(-90) right_triangle(size=[8,8,1.5], orient=ORIENT_Z); 

        move([1,-0.75,11.5]) zrot(-90) right_triangle(size=[8,8,1.5], orient=ORIENT_Z);
        xflip() move([1,-0.75,11.5]) zrot(-90) right_triangle(size=[8,8,1.5], orient=ORIENT_Z);
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

module ws2812_5050_module()
{
    // PCB
    color([0,0.6,0,1]) zrot(360/16) cyl(h=1.2, d=9.5, $fn=8);

    // LED 5050 shape
    color([0.8,0.8,0.8,1]) move([0,0,(1.2/2)+(1.5/2)]) {
        difference() {
            cuboid([5,5,1.5]);
            cyl(h=2,d=4);
        }
    }

    // Centre of LED (lens)
    color([0.9,0.8,0.0,1]) move([0,0,(1.2/2)+(1.5/2)-0.25]) {
        cyl(h=1.25,d=4);
    }

    // LED legs
    color([0.4,0.4,0.4,1]) move([0,0,(1.2/2)+(0.75/2)]) {
        move([3,+1.2,0]) cuboid([1.5,0.9,0.75]);
        move([3,-1.2,0]) cuboid([1.5,0.9,0.75]);
        move([-3,+1.2,0]) cuboid([1.5,0.9,0.75]);
        move([-3,-1.2,0]) cuboid([1.5,0.9,0.75]);
    }

    // Resistor and capacitor components
    color([0.2,0.2,0.2,1]) move([0,0,(1.2/2)+(0.75/2)]) {
        move([0,+3.5,0]) cuboid([2.5,1,0.75]);
        move([0,-3.5,0]) cuboid([2.5,1,0.75]);
    }

    // Rear wire pads
    color([0.8,0.8,0.0,1]) move([0,0,-0.125]) {
        move([-2.25,0,0]) cuboid([2.5,1,1]);
        move([+2.25,0,0]) cuboid([2.5,1,1]);

        move([-2.25,-1.75,0]) cuboid([2.5,1,1]);
        move([+2.25,-1.75,0]) cuboid([2.5,1,1]);

        move([-2.25,+1.75,0]) cuboid([2.5,1,1]);
        move([+2.25,+1.75,0]) cuboid([2.5,1,1]);
    }
}

// This is either a single custom PCB or 2xWS2812 5050 modules
// from Amazon or such-like
module eye_pcb()
{
    move([0,-115.5,5.5]) {
        xrot(90) {
            move([-5,0,0]) ws2812_5050_module();
            move([+5,0,0]) ws2812_5050_module();
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
        move([-3,120,-1.5]) yrot(-90) eye_light_pipe_left();
        move([3,120,-1.5]) yrot(90) eye_light_pipe_right();
    }
}

module render_eye_light_pipe_surround(toPrint)
{
    if(!toPrint) {
        color([0.2,0.2,0.2,1]) eye_light_pipe_surround();
    } else {
        move([0,-5.5,-114]) xrot(-90) eye_light_pipe_surround();
    }
}

module render_eye_pcb(toPrint)
{
    if(!toPrint) {
        eye_pcb();
    } else {
        // This will allow you to render and export a DXF file that
        // can be used as a KiCAD PCB outline...
        move([0,106,0.5]) projection() eye_pcb();
    }
}