/************************************************************************

    main.scad
    
    Valiant Turtle Parallel to Acorn BBC User-port adapter
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

module case_top()
{
    difference() {
        move([0,0,18]) {
            difference() {
                union() {
                    difference() {
                        move([0,3,-1]) cuboid([44, 44, 4], chamfer=1, edges=EDGES_ALL-EDGES_BOTTOM);

                        move ([33/2,0,0]) cyl(h=8,d=3.25);
                        move ([-(33/2),0,0]) cyl(h=8,d=3.25);

                        move([0,-19,-1]) cuboid([40, 4, 6]);
                    }

                    difference() {
                        move([0,1,-3]) cuboid([40, 44, 4]);
                        move([0,1,-4]) cuboid([36, 40, 8]);

                        move([0,-20,-1]) cuboid([40.01, 4, 10]);

                        move ([33/2,0,0]) cyl(h=18,d=3.25);
                        move ([-(33/2),0,0]) cyl(h=18,d=3.25);
                    }
                }

                move([0,-16.5,-1]) cuboid([40.01, 5, 10]);
                move([0,4,-6]) cuboid([36, 40, 10]);
                
                // Screw head recesses
                move ([-(33/2),0,0]) cyl(h=4,d=5.25);
                move ([+(33/2),0,0]) cyl(h=4,d=5.25);
            }

            difference() {
                union() {
                    move ([+(33/2),0,-6.25]) cyl(h=12,d=6);
                    move ([-(33/2),0,-6.25]) cyl(h=12,d=6);
                }

                // Screw head recesses
                move ([-(33/2),0,0]) cyl(h=4,d=5.25);
                move ([+(33/2),0,0]) cyl(h=4,d=5.25);

                // Screw holes
                move ([-(33/2),0,-6.25]) cyl(h=14,d=3.25);
                move ([+(33/2),0,-6.25]) cyl(h=14,d=3.25);
            }

            // Front DSUB lip
            move([0,-14.5,0.5]) cuboid([40, 1, 1]);       
        }

        move([0,0,20]) case_grips();
    }
}

module case_bottom()
{
    difference() {
        move([0,0,11]) {
            difference() {
                move([0,3,-3.5]) cuboid([44, 44, 15], chamfer=1, edges=EDGES_ALL-EDGES_TOP);
                move([0,1,0]) cuboid([40, 44, 18]);

                move ([33/2,0,-8]) cyl(h=8,d=3.25);
                move ([-(33/2),0,-8]) cyl(h=8,d=3.25);
                move([0,20,15.5 - 11]) cuboid([30, 20, 6]);

                // Bolt recesses
                move([0,0,-6.75 + 3.5]) {
                    move ([+(33/2),0,-6.25]) cyl(h=4,d=6.25, $fn=6);
                    move ([-(33/2),0,-6.25]) cyl(h=4,d=6.25, $fn=6);
                }
            }

            move ([33/2,0,-8]) {
                difference() {
                    union() {
                        move([0,0,-0.5]) cyl(h=1,d=8);
                        move([0,0,0.5]) cyl(h=1,d=6);
                    }
                    cyl(h=8,d=3.25);
                }
            }
            move ([-(33/2),0,-8]) {
                difference() {
                    union() {
                        move([0,0,-0.5]) cyl(h=1,d=8);
                        move([0,0,0.5]) cyl(h=1,d=6);
                    }
                    cyl(h=8,d=3.25);
                }
            }

            move([0,-17,-8]) cuboid([40,4,2]);
            move([0,+12 ,-8]) cuboid([40,4,2]);
        }

        move([0,0,-1]) case_grips();
    }
}

module case_grips()
{
    move([0,-2,0]) {
        move([0,20,0]) cuboid([20,2,4], chamfer=1);
        move([0,16,0]) cuboid([24,2,4], chamfer=1);
        move([0,12,0]) cuboid([26,2,4], chamfer=1);
        move([0,08,0]) cuboid([26,2,4], chamfer=1);
        move([0,04,0]) cuboid([26,2,4], chamfer=1);
        move([0,00,0]) cuboid([24,2,4], chamfer=1);
        move([0,-4,0]) cuboid([20,2,4], chamfer=1);
    }
}

// M3x16mm DIN912 head screw (hex bolt)
module m3x16_screw()
{
    // Generic quick screw render (the BOSL version was really slow)
    color([0.8, 0.8, 0.8]) difference() {
        union() {
            move([0,0,1]) cyl(h=3,d=5.5, chamfer2=0.125);
            move([0,0,-8.5]) cyl(h=16,d=3);
        }

        move([0,0,2]) cyl(h=2,d=2.5, $fn=6);
    }
}

module render_case_screws(toPrint)
{
    if (!toPrint) {
        color([0.6,0.6,0.6,1]) {
            move([0,0,19.5 - 3]) {
                move([+(33/2),0,0]) m3x16_screw();
                move([-(33/2),0,0]) m3x16_screw();
            }
        }
    }
}

module render_case_bottom(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) case_bottom();
    } else {
        case_bottom();
    }
}

module render_case_top(toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) case_top();
    } else {
        move([0,0,19]) xrot(180) case_top();
    }
}

module render_support_enforcers(toPrint)
{
    if (toPrint) {
        move([+(33/2),0,2]) cyl(h=4, d=6);
        move([-(33/2),0,2]) cyl(h=4, d=6);
    }
}