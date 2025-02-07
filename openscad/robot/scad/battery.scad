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
    move([0,-2,0]) {
        move([19,10.25,1]) battery18650();
        move([19,-10.25,-1]) xrot(180) battery18650();

        move([-5.5,10.25,-1]) xrot(180) battery18650();
        move([-5.5,-10.25,1]) battery18650();
    }
}

module bullet_4mm_female()
{
    //original is 12.25
    //length is made of base-indent-ridge-tip
    female_bullet_inner_diameter = 3.5;
    female_bullet_length = 11.8;
    female_bullet_outer_diameter = 4.25;
    female_bullet_base_diameter = 4.75;
    female_bullet_base_height = 3;
    female_bullet_indent_height = 1;
    
    

    move([0,0,female_bullet_length/2]) difference() {
        union() {
            move([0,0,0]) cyl(h=female_bullet_length, d=female_bullet_outer_diameter);
            //half of the 12- base height-9, minus half the other bit
            
            //move([0,0,-4.5-0.125]) cyl(h=female_bullet_base_height, d=female_bullet_base_diameter);

            move([0,0,-((female_bullet_length-female_bullet_base_height)/2)]) cyl(h=female_bullet_base_height, d=female_bullet_base_diameter);
            
            //move([0,0,-2.5 - 0.125 + 0.75 - 0.125]) cyl(h=0.75, d=female_bullet_base_diameter);
            move([0,0,-2.5 - 0.125 + 0.75 - 0.125]) cyl(h=0.75, d=female_bullet_base_diameter);
            
        }

        move([0,0,9.5 - 6]) cyl(h=7, d=3.5);
        move([0,0,-9.5+4]) cyl(h=7, d=3.5);
    }
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

// BMS PCB mock-up
module battery_pack_bms_pcb()
{
    move([0,-12.5,-8.5-8]) yrot(180) bms_pcb();
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
    //move([0,0,9]) cyl(h=9,d=4.5);
    //move([0,0,-0.5]) cyl(h=1,d=4);
    //move([0,0,2.25]) cyl(h=5,d=5.5);
    move([0,0,9]) cyl(h=9,d=4.8);
    move([0,0,-0.5]) cyl(h=1,d=4);
    move([0,0,1.75]) cyl(h=3.8,d=5.3);
    //slopes in
    move([0,0,4.35]) cyl (h=1.4, r1=2.65, r2=2.4);
}


module battery_pack_screw_columns()
{
    // Screw columns
    move([45.5,18,-4]) {
        difference() {
            hull() {
                cyl(h=52,d=8);
                move([-4,0,0]) cuboid([1,8,52]); 
            }

            // Threaded insert
            cyl(h=64,d=3.25);
            move([0,0,+(34 - 10)]) cyl(h=8,d=4);
            move([0,0,-(34 - 10)]) cyl(h=8,d=4);
        }
    }

    move([45.5,-18,-4]) {
        difference() {
            hull() {
                cyl(h=52,d=8);
                move([-4,0,0]) cuboid([1,8,52]); 
            }

            // Threaded insert
            cyl(h=64,d=3.25);
            move([0,0,+(34 - 10)]) cyl(h=8,d=4);
            move([0,0,-(34 - 10)]) cyl(h=8,d=4);
        }
    }

    move([-45.5,18,-4]) {
        difference() {
            hull() {
                cyl(h=52,d=8);
                move([+4,0,0]) cuboid([1,8,52]); 
            }

            // Threaded insert
            cyl(h=64,d=3.25);
            move([0,0,+(34 - 10)]) cyl(h=8,d=4);
            move([0,0,-(34 - 10)]) cyl(h=8,d=4);
        }
    }

    move([-45.5,-18,-4]) {
        difference() {
            hull() {
                cyl(h=52,d=8);
                move([+4,0,0]) cuboid([1,8,52]); 
            }

            // Threaded insert
            cyl(h=64,d=3.25);
            move([0,0,+(34 - 10)]) cyl(h=8,d=4);
            move([0,0,-(34 - 10)]) cyl(h=8,d=4);
        }
    }
}

module battery_pack()
{
    difference() {
        move([0,-12.5,10]) {
            difference() {
                union() {
                    cuboid([86-0.5,49-0.5,60 -16], chamfer=1, edges=EDGES_Z_ALL);
                    move([0,0,-21.5]) cuboid([88,49-0.5,17], chamfer=1, edges=EDGES_Z_ALL);

                    // Battery connector
                    move([-23.5,27,-20.5]) move([0,-0.5,2.25]) cuboid([14,5,23.5]);
                }
                cuboid([81,44,64], chamfer=1, edges=EDGES_Z_ALL);

                
                // Battery connector
                // Move z coordinate up to move the bullet connector down. 
                move([-23.5 - 3,29,-22 + 3 +0.5]) bullet_connector_female_mask();
                move([-23.5 + 3,29,-22 + 3 +0.5]) bullet_connector_female_mask();

                // Cable gap
                move([-23.5 - 3,25,-27 + 0]) cuboid([4,10,8]);
                move([-23.5 + 3,25,-27 + 0]) cuboid([4,10,8]);
                
                // Increase cable gap cylinder height as moved the connector mask.
                move([-23.5 - 3,29,-24.5 + 3]) cyl(h=6,d=4);
                move([-23.5 + 3,29,-24.5 + 3]) cyl(h=6,d=4);

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

            battery_pack_clip();
            xflip() battery_pack_clip();

            battery_pack_screw_columns();
        }

        // Recess for cover lock
        move([-23.5,9.75,-4.5]) cuboid([18.25,2,14.5]);
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

            //move z coordinate up to drop the mask further down in the cover.
            
            move([-23.5 - 3,27,10.3]) bullet_connector_female_mask();
            move([-23.5 + 3,27,10.3]) bullet_connector_female_mask();
            move([-23.5 - 3,23.75,4.5]) cuboid([4,10,6]);
            move([-23.5 + 3,23.75,4.5]) cuboid([4,10,6]);
            move([-23.5 - 3,27,7]) cyl(h=6,d=4);
            move([-23.5 + 3,27,7]) cyl(h=6,d=4);
            
            // Positive symbol
            move([-20.5,32.25,19]) {
                cuboid([3,1,1]);
                cuboid([1,1,3]);
            }
        }

        // Clips
        
        move([-33.5,0,0]) { 
            move([0.5,25.9,11.25]) {
            //middle number plus 1
                cuboid([1,12.2,21.5]);
                //5.5 to 6
                move([-0.75,-5.9,0]) cuboid([0.5, 1, 21.5]);
                move([-1.5,-5.9,0]) xrot(90) yrot(-90) right_triangle([1, 21.5, 1], center=true);
            }

            move([19.5,25.9,11.25]) {
                cuboid([1,12.2,21.5]);
                move([0.75,-5.9,0]) cuboid([0.5, 1, 21.5]);
                move([1.5,-5.9,0]) xrot(90) right_triangle([1, 21.5, 1], center=true);
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
            move([+45.5,18,0 - 1]) cyl(h=3,d=5.5);

            move([+45.5,-18,0]) cyl(h=6,d=3.5);
            move([+45.5,-18,0 - 1]) cyl(h=3,d=5.5);

            move([-45.5,18,0]) cyl(h=6,d=3.5);
            move([-45.5,18,0 - 1]) cyl(h=3,d=5.5);

            move([-45.5,-18,0]) cyl(h=6,d=3.5);
            move([-45.5,-18,0 - 1]) cyl(h=3,d=5.5);
        }
    }
}

module battery_pack_bms_bracket()
{
    move([0,-12.5,-51 - 8]) {
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

        difference() {
            // Pillars to mount battery holders on
            union() {
                move([30,0,-22.5]) cuboid([13,5,47], chamfer = 0.5);
                move([-30,0,-22.5]) cuboid([13,5,47], chamfer = 0.5);

                // Orientation tabs
                move([36.25,-2.5,-41.75]) ycyl(h=1.1,d1=1.5, d2=2.5);
                move([-36.25,2.5,-41.75]) ycyl(h=1.1,d1=2.5, d2=1.5);
            }

            // Slice orientation tabs
            move([-37.5,2.5,-41.75]) cuboid([2,2,4]);
            move([37.5,-2.5,-41.75]) cuboid([2,2,4]);

            // Screw holes
            move([27.75,0,-24.5]) ycyl(h=10,d=3.25);
            move([-27.75,0,-24.5]) ycyl(h=10,d=3.25);

            // BMS mounting slots
            move([0,0,-40]) {
                move([+30,0,-4.5]) cuboid([10,2,4], chamfer = 0.5);
                move([-30,0,-4.5]) cuboid([10,2,4], chamfer = 0.5);
            }

            // Clearance for contact solder tags
            move([40.5,0,-34.75]) cuboid([10,10,7.5], chamfer = 1);
            move([40.5,0,-14.25]) cuboid([10,10,7.5], chamfer = 1);

            move([-40.5,0,-34.75]) cuboid([10,10,7.5], chamfer = 1);
            move([-40.5,0,-14.25]) cuboid([10,10,7.5], chamfer = 1);
        }
    }
}

module battery_pack_connector_lock()
{
    move([-23.5,10.125,-4.5]) {
        cuboid([18.25,1,14]);

        move([8.5,3,0]) cuboid([1.25,6,14]);
        move([-8.5,3,0]) cuboid([1.25,6,14]);
    }
}

module battery_pack_cover_supports()
{
    move([0,0,2]) {
        move([45.5,18.5,0]) cyl(h=4,d=8);
        move([45.5,-17.5,0]) cyl(h=4,d=8);
        move([-45.5,18.5,0]) cyl(h=4,d=8);
        move([-45.5,-17.5,0]) cyl(h=4,d=8);
    }
}

module render_battery_pack_bms_bracket(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) battery_pack_bms_bracket();
    } else {
        move([0,12.5,15.5]) battery_pack_bms_bracket();
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
        move([0,-12,43 -8]) xrot(180) battery_pack_upper_cover();
    }
}

module render_battery_pack_connector_cover(toPrint)
{
    if (!toPrint) {
        color([0.2,0.2,0.2,1]) battery_pack_connector_cover();
    } else {
        move([23.5,-15,18]) battery_pack_connector_cover();
    }
}

module render_battery_pack_connector_lock(toPrint)
{
    if (!toPrint) {
        color([0.6,0.6,0.6,1]) battery_pack_connector_lock();
    } else {
        move([23.5,-4.5,-9.5 - 0.125]) xrot(90) battery_pack_connector_lock();
    }
}

module render_female_bullet_connectors(toPrint)
{
    if (!toPrint) {
        move([-23.5,16.5,-12+3]) {
            move([-3,0,0]) bullet_4mm_female();
            move([+3,0,0]) bullet_4mm_female();
        }
    }
}

module render_batteries(toPrint)
{
    if (!toPrint) {
        // 4 Batteries
        color([0.3,0.8,0.5]) {
            move([0,-19,11]) {
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
        move([45.5,-30.5,41.5 - 8]) m3x10_screw();
        move([45.5,5.5,41.5 - 8])  m3x10_screw();
        move([-45.5,-30.5,41.5 - 8])  m3x10_screw();
        move([-45.5,5.5,41.5 - 8])  m3x10_screw();
    }
}

module render_battery_pack_bms_pcb(toPrint)
{
    if (!toPrint) {
        battery_pack_bms_pcb();
    }
}

module render_battery_pack_lower_cover_supports(toPrint)
{
    if (toPrint) {
        battery_pack_cover_supports();
    }
}

module render_battery_pack_upper_cover_supports(toPrint)
{
    if (toPrint) {
        battery_pack_cover_supports();
    }
}