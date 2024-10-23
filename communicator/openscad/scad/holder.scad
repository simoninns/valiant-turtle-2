/************************************************************************

    holder.scad
    
    Valiant Turtle Communicator 2
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

module led()
{
    move([-2.54/2,0,-10.5]) {
        move([0,0,0]) cyl(h=21,d=1);
        move([2.54,0,1]) cyl(h=19,d=1);

        move([0,0,11]) {
            move([2.54/2,0,0]) cyl(h=1, d=6);
            move([2.54/2,0,3.5]) cyl(h=6, d=5);
        }
    }
}

module four_leds()
{
    move([-2.54*4.5,0,6]) {
        move([0,0,0]) led();
        move([2.54*3,0,0]) led();
        move([2.54*6,0,0]) led();
        move([2.54*9,0,0]) led();
    }
}

module led_mask()
{
    move([-2.54/2,0,-10.5]) {
        move([0,0,0]) cuboid([1.5,1.5,21]);
        move([2.54,0,1]) cuboid([1.5,1.5,19]);

        move([0,0,11]) {
            move([2.54/2,0,0]) cyl(h=1.2, d=6.5);
            move([2.54/2,0,3.5]) cyl(h=6, d=6.5);
        }
    }
}

module four_leds_mask()
{
    move([-2.54*4.5,0,0]) {
        move([0,0,0]) led_mask();
        move([2.54*3,0,0]) led_mask();
        move([2.54*6,0,0]) led_mask();
        move([2.54*9,0,0]) led_mask();
    }
}

// Render LED holder
module holder()
{
    move([0,0,6]) difference() {
        move([0,-1.5 - 3,-1]) cuboid([33,13+6,10], chamfer=2, edges=EDGES_Z_BK+EDGES_Y_BOT+EDGE_BOT_BK);
        move([0,0,1]) four_leds_mask();

        move([0,-9.25,-3]) {
            move([-2.54*5,0,0]) {
                move([0,0,-4]) cuboid([1.5,20,8]);
                move([2.54*3,0,-4]) cuboid([1.5,20,8]);
                move([2.54*6,0,-4]) cuboid([1.5,20,8]);
                move([2.54*9,0,-4]) cuboid([1.5,20,8]);
            }

            move([-2.54*4,0,0]) {
                move([0,0,-4]) cuboid([1.5,20,8]);
                move([2.54*3,0,-4]) cuboid([1.5,20,8]);
                move([2.54*6,0,-4]) cuboid([1.5,20,8]);
                move([2.54*9,0,-4]) cuboid([1.5,20,8]);
            }
        }

        move([0,-1.5 - 3-10,4]) cuboid([33-4,13+6,10], chamfer=2, edges=EDGES_Z_BK+EDGE_BOT_BK);
    }
}

module render_holder(toPrint)
{
    if (!toPrint) {
        move([0,-45,16]) xrot(90) {
            color([0.4,0.0,0.0])four_leds();
            color([0.2,0.2,0.2]) holder();
        }
    } else {
        holder();
    }
}