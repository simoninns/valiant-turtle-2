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
    move([0,-120,0]) {
        move([-1,0,1.5]) zrot(-45) yrot(-22) move([10,0,0]) yrot(90) {
            move([0,0,4.5]) {
                // Eyeball
                hull() {
                    move([0,0,(8.6/2) - (4.9/2)]) staggered_sphere(d=4.9, $fn=16);
                    move([0,0,-0.4]) cyl(h=4, d=4.9);
                }
            }
        }

        hull() {
            move([-1,0,-3.5 + 5]) zrot(-45) yrot(-22) move([10,0,0]) yrot(90) {
                move([0,0,2]) cyl(h=0.25, d=4.9);
            }
            move([6,-4.5 + 2,5.5]) cuboid([8,1,6]);
        }

        move([0,2,0]) {
            // WS2812 Clips
            move([0,-3,-2.5]) {
                // Top
                move([6,9.5,4]) cuboid([8,1,4]);
                move([6,9,2]) cuboid([8,2,1], chamfer=0.5, edges=EDGES_X_ALL);

                // Bottom
                move([6,-1.5,4]) cuboid([8,1,4]);
                move([6,-1,2]) cuboid([8,2,1], chamfer=0.5, edges=EDGES_X_ALL);
            }

            // Slot for 5050 WS2812 LED
            difference() {
                move([6,1,3.5+2]) cuboid([8,12,6], chamfer=3, edges=EDGE_TOP_BK);
                move([6,1,2]) cuboid([5.25+2,5.25+2,2], chamfer=1);

                move([6,-3.5,2]) cuboid([9,1,2], chamfer=0.5);
                move([6,5.5,3]) cuboid([9,1,3], chamfer=0.5);
            }
        }
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
    color([0,0.6,0,1]) zrot(360/16) cyl(h=1.2, d=10, $fn=8);

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

        move([-2.25,-2,0]) cuboid([2.5,1,1]);
        move([+2.25,-2,0]) cuboid([2.5,1,1]);

        move([-2.25,+2,0]) cuboid([2.5,1,1]);
        move([+2.25,+2,0]) cuboid([2.5,1,1]);
    }
}

// This is either a single custom PCB or 2xWS2812 5050 modules
// from Amazon or such-like
module eye_pcb()
{
    move([0,-117,1.5]) {
        move([-6,0,0]) ws2812_5050_module();
        move([+6,0,0]) ws2812_5050_module();
    }
}

module eye_pcb_jig_rest()
{
    // Cable rest
    move([0,0,0]) {
        difference() {
            move([0,0,0]) cuboid([10,10,4], chamfer=1, edges=EDGES_Z_ALL);

            move([0,0,1]) xcyl(h=12,d=1.5);
            move([0,2,1]) xcyl(h=12,d=1.5);
            move([0,-2,1]) xcyl(h=12,d=1.5);

            move([0,0,1.5]) cuboid([12,1.5,1.5]);
            move([0,2,1.5]) cuboid([12,1.5,1.5]);
            move([0,-2,1.5]) cuboid([12,1.5,1.5]);
        }
    }
}

// This jig isn't required for the robot.  It is to assist
// when solding the 5050 LEDs together to make the robot's eyes
module eye_pcb_jig()
{
    move([0,0,3.5]) {
        // Edges
        move([0,6,-1]) cuboid([24,2,4]);
        move([0,-6,-1]) cuboid([24,2,4]);

        // Base
        difference() {
            union() {
                move([4,0,-2.5]) cuboid([36,16,2], chamfer=1, edges=EDGES_Z_ALL+EDGES_TOP);
                move([0,12,-2.5]) cuboid([24,30,2], chamfer=1, edges=EDGES_TOP);
            }

            move([0,17,-2.5]) cuboid([24-8,20-8,4]);

            move([6,0,-1.5]) cuboid([5.25,5.25,2]);
            move([-6,0,-1.5]) cuboid([5.25,5.25,2]);
        }

        // Slot for joining pin header
        difference() {
            union() {
                move([0,5.25,0]) cuboid([4,3.75,4]);
                move([0,-5.25,0]) cuboid([4,3.75,4]);
            }
            cuboid([2.75,10,6]);
        }

        // Cable rests
        move([16,0,0]) eye_pcb_jig_rest();

        // End stop
        move([-12,0,0]) cuboid([2,14,3]);
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

module render_eye_pcb_jig(toPrint)
{
    if(!toPrint) {
        move([-6,0,3.5]) xrot(180) ws2812_5050_module();
        move([+6,0,3.5]) xrot(180) ws2812_5050_module();
        eye_pcb_jig();
    } else {
        eye_pcb_jig();
    }
}