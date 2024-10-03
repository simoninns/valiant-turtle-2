/************************************************************************

    stand.scad
    
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

// Marker to show where the feet should be attached
module foot_marker()
{
    difference() {
        move([0,0,0]) cuboid([13,13,1]);
        move([0,0,-1]) cuboid([11.5,11.5,3]);
    }
}

module stand()
{
    move([0,-12.5,-40]) {
        difference() {
            union() {
                // Central pillar
                difference() {
                    hull() {
                        move([0,0,7.5]) cyl(h=19, d=42);
                        move([0,41.5,7.5-5]) cyl(h=19-10, d=42);
                    }
                }

                // Spokes
                move([0,41.5,0]) for (rot = [0:360/3: 360-1]) {
                    if (rot != (360/3)*1) {
                        difference() {
                            hull() {
                                zrot(rot+(360/6)) move([0,100/2,-1]) cuboid([20,100,2], chamfer=1, edges=EDGES_Z_ALL+EDGES_TOP);
                                zrot(rot+(360/6)) move([0,20,1]) cuboid([20,2,6], chamfer=1, edges=EDGES_Z_ALL+EDGES_TOP);
                            }

                            zrot(rot+(360/6)) move([0,90,-2.25]) foot_marker();
                        }
                    }
                }
            }

            // Remove some material
            hull() {
                move([0,41.5,7.5]) cyl(h=24, d=30);
                move([0,41.5-12,7.5]) cyl(h=24, d=30);
            }

            // Threaded inserts
            for (rot = [0:360/4: 360-1]) {
                zrot(rot+(360/8)) move([0,14,21 - 6]) {
                    cyl(h=8, d=4);
                    cyl(h=16, d=3);
                }
            }

            // Central pillar hole
            move([0,0,10+2]) cyl(h=24, d=20);

            // Gap for cable
            move([0,12,3.5]) zrot(90) xrot(360/12) xcyl(h=12, d=6, $fn=6);
            move([0,59,2.5]) zrot(90) xrot(360/12) xcyl(h=12, d=6, $fn=6);

            // Front foot marker
            move([0,-10,-2.25]) foot_marker();
        }
    }
}

// Make it a little easier to guide the screw into place
module stand_screw_surround()
{
    difference() {
        union() {
            move([0,0,-0.5]) cyl(h=3,d=8);
            move([0,0,1.5]) cyl(h=1,d1=8, d2=7);
        }
        move([0,0,1]) cyl(h=4,d=5.5);
        move([0,0,0]) cyl(h=6,d=3.5);
    }
}

module stand_upper_cover()
{
    move([0,-12.5,41.5 - 8]) {
        difference() {
            union() {
                cuboid([85.5,49-0.5,3], chamfer=1, edges=EDGES_Z_ALL+EDGES_TOP);

                difference() {
                    move([0,0,-2]) cuboid([81-0.25,44-0.25,2], chamfer=1, edges=EDGES_Z_ALL);
                    move([0,0,-2]) cuboid([81-4,44-4,4], chamfer=1, edges=EDGES_Z_ALL);
                }
                
                union() {
                    hull() {
                        move([+45.5,18,0]) cyl(h=3,d=8);
                        move([-45.5,18,0]) cyl(h=3,d=8);
                    }
                    hull() {
                        move([+45.5,-18,0]) cyl(h=3,d=8);
                        move([-45.5,-18,0]) cyl(h=3,d=8);
                    }
                }
            }

            move([+45.5,18,0]) cyl(h=6,d=3.5);
            move([+45.5,18,0 + 1]) cyl(h=3,d=5.5);

            move([+45.5,-18,0]) cyl(h=6,d=3.5);
            move([+45.5,-18,0 + 1]) cyl(h=3,d=5.5);

            move([-45.5,18,0]) cyl(h=6,d=3.5);
            move([-45.5,18,0 + 1]) cyl(h=3,d=5.5);

            move([-45.5,-18,0]) cyl(h=6,d=3.5);
            move([-45.5,-18,0 + 1]) cyl(h=3,d=5.5);
        }

        // Add a little marker to make the part easy to identify
        move([0,0,-2]) cyl(h=2, d=6);
    }
}

module stand_lower_cover()
{
    difference() {
        move([0,-12.5,-21.5]) {
            difference() {
                union() {
                    cuboid([88,49-0.5,3], chamfer=1, edges=EDGES_Z_ALL+EDGES_BOTTOM);

                    difference() {
                        move([0,0,2]) cuboid([81-0.25,44-0.25,2], chamfer=1, edges=EDGES_Z_ALL);
                        move([0,0,2]) cuboid([81-4,44-4,4], chamfer=1, edges=EDGES_Z_ALL);
                    }
                    
                    union() {
                        hull() {
                            move([+45.5,18,0]) cyl(h=3,d=8);
                            move([-45.5,18,0]) cyl(h=3,d=8);
                        }
                        hull() {
                            move([+45.5,-18,0]) cyl(h=3,d=8);
                            move([-45.5,-18,0]) cyl(h=3,d=8);
                        }
                    }
                }

                move([+45.5,18,0]) cyl(h=6,d=3.5);
                move([+45.5,18,0 - 1]) cyl(h=3,d=5.5);

                move([+45.5,-18,0]) cyl(h=6,d=3.5);
                move([+45.5,-18,0 - 1]) cyl(h=3,d=5.5);

                move([-45.5,18,0]) cyl(h=6,d=3.5);
                move([-45.5,18,0 - 1]) cyl(h=3,d=5.5);

                move([-45.5,-18,0]) cyl(h=6,d=3.5);
                move([-45.5,-18,0 - 1]) cyl(h=3,d=5.5);
            }
        }

        // M3 Screw holes
        move([0,-12.5,-40]) for (rot = [0:360/4: 360-1]) {
            zrot(rot+(360/8)) move([0,14,20]) {
                cyl(h=8, d=3.5);
            }
        }

        // Central pillar hole
        move([0,-12.5,-20])cyl(h=24, d=20);
    }

    // M3 Screw surrounds
    move([0,-12.5,-40]) for (rot = [0:360/4: 360-1]) {
        zrot(rot+(360/8)) move([0,14,20]) {
            move([0,0,2]) stand_screw_surround();
        }
    }
}

module render_stand(toPrint)
{
    if (!toPrint) {
        move([0,0,0]) color([0.9,0.9,0.6,1]) stand();
    } else {  
        move([0,12,42]) stand();
    }
}

module render_stand_upper_cover(toPrint)
{
    if (!toPrint) {
        move([0,0,0]) color([0.9,0.9,0.6,1]) stand_upper_cover();
    } else {  
        move([0,-12,43 -8]) xrot(180) stand_upper_cover();
    }
}

module render_stand_lower_cover(toPrint)
{
    if (!toPrint) {
        move([0,0,0]) color([0.9,0.9,0.6,1]) stand_lower_cover();
    } else {  
        move([0,13,23]) stand_lower_cover();
    }
}