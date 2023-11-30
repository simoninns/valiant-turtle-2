/************************************************************************

    shell.scad
    
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

module pentagon()
{
    hull() {
        zrot((360/5) * 0) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 1) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 2) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 3) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 4) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
    }
}

module irrPentagonTop()
{
    hull() {
        zrot((360/5) * 0) move([0,103/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 1) move([0,123/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 2) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 3) move([0,110/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 4) move([0,123/2,0]) staggered_sphere(d=2, $fn=16);
    }
}

module irrPentagonBottom()
{
    hull() {
        zrot((360/5) * 0) move([0,104/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 1) move([0,122/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 2) move([0,107/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 3) move([0,107/2,0]) staggered_sphere(d=2, $fn=16);
        zrot((360/5) * 4) move([0,122/2,0]) staggered_sphere(d=2, $fn=16);
    }
}

module shellTop()
{
    yrot(180) {
        // Centre
        pentagon();

        for ( i = [0:1:4]) {
            zrot((360/5) * i) {
                zrot(360/10) move([0,70,36.75]) xrot(55.5) irrPentagonTop();
            }
        }
    }
}

module shellBottom()
{
    zrot(360/10) for ( i = [0:1:4]) {
        zrot((360/5) * i) {
            zrot(360/10) move([0,69,36.25]) xrot(54) irrPentagonBottom();
        }
    }
}

// Note: Borrowed from the body code and made a little wider
module headCutout(dpt)
{
    hull() {
        move([0,119.5 - 210,0]) {
            cuboid([44,65,dpt]);
            move([0,-32.5,-(dpt/2)]) xrot(90) right_triangle([21.5,dpt,21.5]);
            yrot(180) move([0,-32.5,-(dpt/2)]) xrot(90) right_triangle([21.5,dpt,21.5]);
        }

        move([0,119.5 - 210,15]) {
            cuboid([23,65,20]);
            move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
            yrot(180) move([0,-32.5,-(20/2)]) xrot(90) right_triangle([21.5/2,20,21.5/2]);
        }
    }
}

module wheelCoverBase()
{
    move([84.25 ,25,1.5]) {
        difference() {
            cuboid([75.5,80,3], fillet=1, edges=EDGES_Z_ALL, $fn=16);
            cuboid([75.5-4,80-4,6]);
            move([-26,0,0]) cuboid([30,76,6]);
            move([-29.5,-32,0]) yrot(26) cuboid([30,20,20]);
        }
    }
}

module wheelCover()
{
    move([0,25,1]) {

        outer_x = 121;
        backinner_x = 47.5;
        frontinner_x = 73;

        backmid_x = backinner_x + 24;
        frontmid_x = outer_x - 26;

        front_y = -39;
        back_y = 39;
        middle_y = front_y + 46.5;

        frontmid_z = 23;
        fronttop_z = 23 + 10;
        frontbottom_z = 12.5 + 1;
        base_z = 2;

        // Side
        hull() {
            move([outer_x,back_y,base_z]) staggered_sphere(d=2, $fn=16); // A
            move([outer_x,front_y,base_z]) staggered_sphere(d=2, $fn=16); // B
            move([outer_x,middle_y,frontmid_z]) staggered_sphere(d=2, $fn=16); // C
        }

        // Back
        hull() {
            move([outer_x,back_y,base_z]) staggered_sphere(d=2, $fn=16); // A
            move([backinner_x,back_y,base_z]) staggered_sphere(d=2, $fn=16); // D
            move([backmid_x,back_y,frontmid_z]) staggered_sphere(d=2, $fn=16); // E
        }

        // Middle
        hull() {
            move([outer_x,middle_y,frontmid_z]) staggered_sphere(d=2, $fn=16); // C
            move([frontmid_x,middle_y,fronttop_z+1]) staggered_sphere(d=2, $fn=16); // F
            move([backmid_x,back_y,frontmid_z]) staggered_sphere(d=2, $fn=16); // E
            move([outer_x,back_y,base_z]) staggered_sphere(d=2, $fn=16); // A
        }

        // Front
        hull() {
            move([outer_x,front_y,base_z]) staggered_sphere(d=2, $fn=16); // B
            move([frontmid_x-0.5,front_y,frontbottom_z]) staggered_sphere(d=2, $fn=16); // G
            move([frontinner_x,front_y,base_z]) staggered_sphere(d=2, $fn=16); // H
        }

        // Front Top
        hull() {
            move([frontmid_x-0.5,front_y,frontbottom_z]) staggered_sphere(d=2, $fn=16); // G
            move([frontmid_x,middle_y,fronttop_z+1]) staggered_sphere(d=2, $fn=16); // F

            move([outer_x,front_y,base_z]) staggered_sphere(d=2, $fn=16); // B
            move([outer_x,middle_y,frontmid_z]) staggered_sphere(d=2, $fn=16); // C
        }

        // Back upper
        hull() {
            move([backinner_x,back_y,base_z]) staggered_sphere(d=2, $fn=16); // D
            move([backmid_x,back_y,frontmid_z]) staggered_sphere(d=2, $fn=16); // E
            move([backmid_x,back_y,fronttop_z]) staggered_sphere(d=2, $fn=16); // I
        }

        // Front upper
        hull() {
            move([frontmid_x-0.5,front_y,frontbottom_z]) staggered_sphere(d=2, $fn=16); // G
            move([frontmid_x-0.5,front_y,frontbottom_z + 16.5]) staggered_sphere(d=2, $fn=16); // J
            move([frontinner_x,front_y,base_z]) staggered_sphere(d=2, $fn=16); // H
        }

        // Front side upper
        hull() {
            move([frontmid_x-0.5,front_y,frontbottom_z]) staggered_sphere(d=2, $fn=16); // G
            move([frontmid_x-0.5,front_y,frontbottom_z + 16.5]) staggered_sphere(d=2, $fn=16); // J
            move([frontmid_x,middle_y,fronttop_z + 1]) staggered_sphere(d=2, $fn=16); // F

            move([frontmid_x,middle_y,fronttop_z+17]) staggered_sphere(d=2, $fn=16); // K (F+15.5)
        }

        // Back side upper
        hull() {
            move([backmid_x,back_y,frontmid_z]) staggered_sphere(d=2, $fn=16); // E
            move([backmid_x,back_y,fronttop_z]) staggered_sphere(d=2, $fn=16); // I
            move([frontmid_x,middle_y,fronttop_z+1]) staggered_sphere(d=2, $fn=16); // F

            move([frontmid_x,middle_y,fronttop_z+17]) staggered_sphere(d=2, $fn=16); // K
        }
    }
}

module wheelCutout()
{
    move([2,0,0]) hull() {
        move([51 ,25,14]) cuboid([40,76,40]);
        move([73.5 ,10,14]) cuboid([40,46,34]);
        move([121-26 - 1.25, -39 + 46.5 + 24.75,23+10+18]) staggered_sphere(d=0.5, $fn=16);
    }
}

module shell()
{
    difference() {
        union() {
            difference() {
                union() {
                    move([0,1.5,104]) shellTop();
                    move([0,1.5,-27]) shellBottom();
                }
                move([0,0,-20]) cuboid([200,200,40]);

                // Head cutout
                move([0,0,-5]) headCutout(10);

                // Wheel cutouts
                wheelCutout();
                xflip() wheelCutout();

                // Clean the back edge
                move([0,62.5,1]) cuboid([100,1,3]);
            }
            
            wheelCoverBase();
            wheelCover();
            
            xflip() {
                wheelCoverBase();
                wheelCover();
            }

            // Make the back edge filled
            move([0,64.5,1]) cuboid([100,1,2]);

            
        }        
    }   

    
}

module render_shell(crend, toPrint)
{
    color([0,0.8,0,1]) shell();
}