/************************************************************************

    battery.scad
    
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

// Non-printable parts ------------------------------------------------------------------

module battery18650_protected()
{
    // 18650 Battery with protection circuit
    difference() {
        cyl(h=69, d=18.5);
        move([0,0,(69/2)]) cyl(h=0.5, d=13);
        move([0,0,-(69/2)]) cyl(h=0.5, d=13);
    }
    
    move([0,0,(69/2)+0.25]) cyl(h=1, d=5);
}

module battery18650()
{
    // 18650 Battery without protection circuit
    difference() {
        cyl(h=65, d=18.5);
        move([0,0,(65/2)]) cyl(h=0.5, d=13);
        move([0,0,-(65/2)]) cyl(h=0.5, d=13);
    }
    
    move([0,0,(65/2)+0.25]) cyl(h=1, d=5);
}

module batteries()
{
    move([0,0,0]) {
        move([19,9.5,0]) battery18650();
        move([19,-9.5,0]) xrot(180) battery18650();

        move([-5.5,9.5,0]) xrot(180) battery18650();
        move([-5.5,-9.5,0]) battery18650();
    }
}

module bullet_4mm_female()
{
    move([0,0,12.25/2]) difference() {
        union() {
            move([0,0,0]) cyl(h=12.25, d=4.25);
            move([0,0,-4.5-0.125]) cyl(h=3, d=4.75);
            move([0,0,-2.5 - 0.125 + 0.75 - 0.125]) cyl(h=0.75, d=4.75);
        }

        move([0,0,9.5 - 6]) cyl(h=7, d=3.5);
        move([0,0,-9.5+4]) cyl(h=7, d=3.5);
    }
}

module battery_18650_holder()
{
    difference() {
        union() {
            move([0,0,3.5]) cuboid([39,78,7]);
            move([0,+37.25,7]) prismoid(size1=[39,3.5], size2=[36,3.5], h=7.5);
            move([0,-37.25,7]) prismoid(size1=[39,3.5], size2=[36,3.5], h=7.5);
        }

        move([-9.5,0,8]) ycyl(h=71,d=18);
        move([+9.5,0,8]) ycyl(h=71,d=18);

        // Screw recesses
        move([0,-(55.5/2),5]) cuboid([6,6,8]);
        move([0,+(55.5/2),5]) cuboid([6,6,8]);

        // Screw holes
        move([0,-(55.5/2),0]) cyl(h=8,d=3);
        move([0,+(55.5/2),0]) cyl(h=8,d=3);

        // Positive markers
        move([9.5,39,4]) {
            cuboid([5,1,1]);
            cuboid([1,1,5]);
        }

        move([-9.5,-39,4]) {
            cuboid([5,1,1]);
            cuboid([1,1,5]);
        }

        // Negative markers
        move([-9.5,39,4]) {
            cuboid([5,1,1]);
        }

        move([+9.5,-39,4]) {
            cuboid([5,1,1]);
        }
    }

    // Tabs
    // move([-9.5,+41,0.2]) cuboid([6.5,4.5,0.4]);
    // move([+9.5,+41,0.2]) cuboid([6.5,4.5,0.4]);
    // move([-9.5,-41,0.2]) cuboid([6.5,4.5,0.4]);
    // move([+9.5,-41,0.2]) cuboid([6.5,4.5,0.4]);

    // Orientation tab
    move([-18.75 + 1.5,-38.25 + 2,-0.5]) cyl(h=1,d=1.5);
}

module bms_pcb()
{
    difference() {
        union() {
            color([0,0.6,0,1]) cuboid([34,34,1.25], fillet=5, edges=EDGES_Z_ALL);

            // Pads
            color([0.8,0.8,0.0,1]) move([0,0,1]) {
                move([0,-15.5,0]) {
                    move([-9,0,0]) cuboid([6,3,1]); // B1
                    move([0,0,0]) cuboid([6,3,1]);  // B2
                    move([+9,0,0]) cuboid([6,3,1]);  // B3
                }

                move([-15.5,0,0]) cuboid([3,6,1]); // B-
                move([+15.5,0,0]) cuboid([3,6,1]); // B+

                move([0,14,-0.25]) {
                    move([-1.5 - 1.5,0,0]) cuboid([3,6,0.5], fillet=1.5, edges=EDGES_Z_ALL); // B1
                    move([+1.5 + 1.5,0,0]) cuboid([3,6,0.5], fillet=1.5, edges=EDGES_Z_ALL);  // B3
                }
            }
        }

        // Wire holes
        move([0,14,0]) {
            move([-1.5 - 1.5,0,0]) cyl(h=4,d=1);
            move([+1.5 + 1.5,0,0]) cyl(h=4,d=1);
        }
    }
}

// Battery holders and BMS PCB mock-up
module battery_pack_internal()
{
    move([0,0,0]) {
        move([0,-12.5,18]) {
            move([0,-2.5,0]) yrot(90) xrot(90) zrot(180) battery_18650_holder();
            move([0,+2.5,0]) yrot(90) xrot(-90) zrot(180) battery_18650_holder();
        }

        move([0,-12.5,-6.5]) yrot(180) bms_pcb();
    }
}

// Printable parts ----------------------------------------------------------------------

module battery_pack_clip()
{
    move([41.5,0,-15]) { 
        difference() {
            union() {
                move([3.5,0,+2.5]) cuboid([9, 24,35]);
                move([-1,-12,20]) right_triangle([9, 24, 9]);

                // Tab
                move([8.5,0,-13]) cuboid([3,18,4], chamfer=1, edges=EDGES_Z_ALL+EDGES_RIGHT);

                // Clip
                move([8,-9,6]) {
                    difference() {
                        right_triangle([3, 18, 3]);
                        move([4,9,0]) cuboid([3.5,20,3]);
                    }
                }
            }

            move([-2,0,-2]) union() {
                move([3.5,0,+2.5]) cuboid([9, 18+2,37.1]);
                move([-1,-10,21]) right_triangle([9, 18+2, 9]);
            }

            // Cut-outs to form side protectors
            move([+4,-9.5,9]) cuboid([24, 1,50]);
            move([+4,+9.5,9]) cuboid([24, 1,50]);
        }
    }
}

module bullet_connector_female_mask()
{
    move([0,0,9]) cyl(h=9,d=4.5);
    move([0,0,-0.5]) cyl(h=1,d=4);
    move([0,0,2.25]) cyl(h=5,d=5.5);
}

module battery_pack_screw_columns()
{
    // Screw columns
    move([45.5,18,0]) {
        difference() {
            hull() {
                cyl(h=60,d=8);
                move([-4,0,0]) cuboid([1,8,60]); 
            }

            // Threaded insert
            cyl(h=64,d=3.25);
            move([0,0,+(34 - 6)]) cyl(h=8,d=4);
            move([0,0,-(34 - 6)]) cyl(h=8,d=4);
        }
    }

    move([45.5,-18,0]) {
        difference() {
            hull() {
                cyl(h=60,d=8);
                move([-4,0,0]) cuboid([1,8,60]); 
            }

            // Threaded insert
            cyl(h=64,d=3.25);
            move([0,0,+(34 - 6)]) cyl(h=8,d=4);
            move([0,0,-(34 - 6)]) cyl(h=8,d=4);
        }
    }

    move([-45.5,18,0]) {
        difference() {
            hull() {
                cyl(h=60,d=8);
                move([+4,0,0]) cuboid([1,8,60]); 
            }

            // Threaded insert
            cyl(h=64,d=3.25);
            move([0,0,+(34 - 6)]) cyl(h=8,d=4);
            move([0,0,-(34 - 6)]) cyl(h=8,d=4);
        }
    }

    move([-45.5,-18,0]) {
        difference() {
            hull() {
                cyl(h=60,d=8);
                move([+4,0,0]) cuboid([1,8,60]); 
            }

            // Threaded insert
            cyl(h=64,d=3.25);
            move([0,0,+(34 - 6)]) cyl(h=8,d=4);
            move([0,0,-(34 - 6)]) cyl(h=8,d=4);
        }
    }
}

module battery_pack()
{
    difference() {
        move([0,-12.5,10]) {
            difference() {
                union() {
                    cuboid([86-0.5,49-0.5,60], chamfer=1, edges=EDGES_Z_ALL);
                    //move([0,0,-8]) cuboid([86-0.5,49-0.5,10], chamfer=1, edges=EDGES_Z_ALL); // TEMP
                    move([0,0,-21.5]) cuboid([88,49-0.5,17], chamfer=1, edges=EDGES_Z_ALL);

                    // Battery connector
                    move([-23.5,27,-20.5]) move([0,-0.5,2.25]) cuboid([14,5,23.5]);
                }
                cuboid([81,44,64], chamfer=1, edges=EDGES_Z_ALL);

                // Battery connector
                move([-23.5 - 3,29,-22 + 3]) bullet_connector_female_mask();
                move([-23.5 + 3,29,-22 + 3]) bullet_connector_female_mask();

                // Cable gap
                move([-23.5 - 3,25,-27 + 0]) cuboid([4,10,8]);
                move([-23.5 + 3,25,-27 + 0]) cuboid([4,10,8]);
                move([-23.5 - 3,29,-24.5 + 3]) cyl(h=4,d=4);
                move([-23.5 + 3,29,-24.5 + 3]) cyl(h=4,d=4);

                // Clip slots
                move([-33.5,0,-17.25]) { 
                    move([1,23,0]) cuboid([2.5,9,21.5]);
                    move([19,23,0]) cuboid([2.5,9,21.5]);

                    // Angle the top of the slots for better printing
                    move([1,23,10.75]) yrot(45) cuboid([1.75,9,1.75]);
                    move([19,23,10.75]) yrot(45) cuboid([1.75,9,1.75]);
                    move([0.25 + 0.125,21,10.75]) yrot(45) cuboid([2.75 - 0.125,4,2.75 - 0.125]);
                    move([19.25 + 0.25 + 0.125,21,10.75]) yrot(45) cuboid([2.75 - 0.125,4,2.75 - 0.125]);

                    // Clip recess
                    move([-0.5,22,0]) cuboid([2,2,21.5]);
                    move([20.5,22,0]) cuboid([2,2,21.5]);
                }

                // Lower screw clearance
                move([45.5,18,-(34 - 6)]) cyl(h=8,d=4);
                move([-45.5,18,-(34 - 6)]) cyl(h=8,d=4);
                move([45.5,-18,-(34 - 6)]) cyl(h=8,d=4);
                move([-45.5,-18,-(34 - 6)]) cyl(h=8,d=4);
            }

            // Clip base
            move([-23.5,28,-29]) cuboid([20,12,2]);

            // Shelf for fastener
            move([-23.5,21.5,-22]) zrot(90) yrot(180) right_triangle([1, 15, 1], center=true);

            battery_pack_clip();
            xflip() battery_pack_clip();

            battery_pack_screw_columns();
        }
    }
}

module battery_pack_supports()
{
    move([+50.5,-12.5,-7]) cuboid([6,18,26]);
    move([-50.5,-12.5,-7]) cuboid([6,18,26]);
}

module battery_pack_connector_cover()
{
    move([0,-10.5,-21.5+3]) {
        // Battery connector
        difference() {
            difference() {
                move([-23.5,27.25,11.25]) cuboid([18,9.5,17.5 + 4]);
                move([-23.5,26.75 - 4,10]) cuboid([20,8.5,25]);
            }

            move([-23.5 - 3,27,9.0]) bullet_connector_female_mask();
            move([-23.5 + 3,27,9.0]) bullet_connector_female_mask();
            move([-23.5 - 3,23.75,4.5]) cuboid([4,10,6]);
            move([-23.5 + 3,23.75,4.5]) cuboid([4,10,6]);
            move([-23.5 - 3,27,6.5]) cyl(h=4,d=4);
            move([-23.5 + 3,27,6.5]) cyl(h=4,d=4);
        }

        // Clips
        move([-33.5,0,0]) { 
            move([0.5,26,11.25]) {
                cuboid([1,12,21.5]);
                move([-0.75,-5.5,0]) cuboid([0.5, 1, 21.5]);
                move([-1.5,-5.5,0]) xrot(90) yrot(-90) right_triangle([1, 21.5, 1], center=true);
            }

            move([19.5,26,11.25]) {
                cuboid([1,12,21.5]);
                move([0.75,-5.5,0]) cuboid([0.5, 1, 21.5]);
                move([1.5,-5.5,0]) xrot(90) right_triangle([1, 21.5, 1], center=true);
            }
        }
    }
}

module battery_pack_lower_cover()
{
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
            move([+45.5,18,0 - 1]) cyl(h=3,d=6.5);

            move([+45.5,-18,0]) cyl(h=6,d=3.5);
            move([+45.5,-18,0 - 1]) cyl(h=3,d=6.5);

            move([-45.5,18,0]) cyl(h=6,d=3.5);
            move([-45.5,18,0 - 1]) cyl(h=3,d=6.5);

            move([-45.5,-18,0]) cyl(h=6,d=3.5);
            move([-45.5,-18,0 - 1]) cyl(h=3,d=6.5);
        }
    }
}

module battery_pack_bms_bracket()
{
    move([0,-12.5,-49]) {
        // BMS mounting bracket
        move([0,0,45]) {
            cuboid([73,5,3], chamfer = 0.5);
            cuboid([26,26,3], chamfer = 0.5);

            move([+30,0,2.5]) cuboid([10,2,3], chamfer = 0.5);
            move([-30,0,2.5]) cuboid([10,2,3], chamfer = 0.5);
        }
    }
}

module battery_pack_upper_cover()
{
    move([0,-12.5,41.5]) {
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
            move([+45.5,18,0 + 1]) cyl(h=3,d=6.5);

            move([+45.5,-18,0]) cyl(h=6,d=3.5);
            move([+45.5,-18,0 + 1]) cyl(h=3,d=6.5);

            move([-45.5,18,0]) cyl(h=6,d=3.5);
            move([-45.5,18,0 + 1]) cyl(h=3,d=6.5);

            move([-45.5,-18,0]) cyl(h=6,d=3.5);
            move([-45.5,-18,0 + 1]) cyl(h=3,d=6.5);
        }

        difference() {
            // Pillars to mount battery holders on
            union() {
                move([30,0,-22]) cuboid([13,5,44], chamfer = 0.5);
                move([-30,0,-22]) cuboid([13,5,44], chamfer = 0.5);
            }

            // Screw holes
            move([27.75,0,-23.5]) ycyl(h=10,d=3.25);
            move([-27.75,0,-23.5]) ycyl(h=10,d=3.25);

            // Orientation holes
            move([36.25,-3,-40.75]) ycyl(h=4,d=1.75);
            move([-36.25,6,-40.75]) ycyl(h=10,d=1.5);


            // BMS mounting slots
            move([0,0,-40]) {
                move([+30,0,-2.5]) cuboid([10,2,4], chamfer = 0.5);
                move([-30,0,-2.5]) cuboid([10,2,4], chamfer = 0.5);
            }
        }
    }
}

module battery_pack_connector_lock()
{
    move([-23.5,9,-4.5]) {
        cuboid([18,1,14]);

        move([8.5,3,0]) cuboid([1.25,7,14]);
        move([-8.5,3,0]) cuboid([1.25,7,14]);
    }
}

module render_battery_pack_bms_bracket(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) battery_pack_bms_bracket();
    } else {
        move([0,12.5,5.5]) battery_pack_bms_bracket();
    }
}

module render_battery_pack(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) battery_pack();
    } else {
        move([0,13,20]) battery_pack();
    }
}

module render_battery_pack_supports(toPrint)
{
    if (!toPrint) {
        // Nothing for display model
    } else {
        move([0,13,20]) battery_pack_supports();
    }
}

module render_battery_pack_lower_cover(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) battery_pack_lower_cover();
    } else {
        move([0,13,23]) battery_pack_lower_cover();
    }
}

module render_battery_pack_upper_cover(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) battery_pack_upper_cover();
    } else {
        move([0,-12,43]) xrot(180) battery_pack_upper_cover();
    }
}

module render_battery_pack_connector_cover(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) battery_pack_connector_cover();

        color([0.8,0.8,0.0,1]) move([-23.5,16.5,-12+3]) {
            move([-3,0,0]) bullet_4mm_female();
            move([+3,0,0]) bullet_4mm_female();
        }
    } else {
        move([23.5,-15,18]) battery_pack_connector_cover();
    }
}

module render_battery_pack_connector_lock(toPrint)
{
    if (!toPrint) {
        color([0.6,0.6,0.6,1]) battery_pack_connector_lock();
    } else {
        move([23.5,-4.5,-8.5]) xrot(90) battery_pack_connector_lock();
    }
}

module render_batteries(toPrint)
{
    if (!toPrint) {
        // 4 Batteries
        color([0.3,0.8,0.5]) {
            move([0,-19,19]) {
                xrot(90) yrot(90) batteries();
            }
        }
    }
}

module render_battery_screws(toPrint)
{
    if (!toPrint) {
        // Lower screws
        move([45.5,-30.5,-21.5]) xrot(180) m3x10_screw();
        move([45.5,5.5,-21.5]) xrot(180) m3x10_screw();
        move([-45.5,-30.5,-21.5]) xrot(180) m3x10_screw();
        move([-45.5,5.5,-21.5]) xrot(180) m3x10_screw();

        // Upper screws
        move([45.5,-30.5,41.5]) m3x10_screw();
        move([45.5,5.5,41.5])  m3x10_screw();
        move([-45.5,-30.5,41.5])  m3x10_screw();
        move([-45.5,5.5,41.5])  m3x10_screw();
    }
}

module render_battery_pack_internal(toPrint)
{
    if (!toPrint) {
        battery_pack_internal();
    }
}