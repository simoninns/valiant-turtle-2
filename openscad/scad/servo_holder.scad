/************************************************************************

    servo_holder.scad
    
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

module servo_holder()
{
    move([30.5,38,8.5]) {
        difference() {
            union() {
                move([1,0,0.5]) cuboid([7,39,18], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);
                move([6.5,0,-7]) cuboid([12,39,3], chamfer=1, edges=EDGES_X_TOP+EDGES_Y_TOP+EDGES_Z_ALL);    
            }

            // Servo clearance
            move([0,0,1.5]) cuboid([30,24,13]);

            // Servo mounting holes
            move([0,14,1.5]) xcyl(h=10,d=1.5);
            move([0,-14,1.5]) xcyl(h=10,d=1.5);

            // M3 screw holes
            move([8,15,-7]) cyl(h=5,d=3);
            move([8,-15,-7]) cyl(h=5,d=3);
        }
    }
}

module render_servo_holder(crend, toPrint)
{
    if (!toPrint) {
        color([0.9,0.9,0.6,1]) servo_holder();
    } else {
        move([10,-40,-28]) yrot(-90) servo_holder();
    }
}

module render_servo_holder_screws(crend, toPrint)
{
    if (!toPrint) {
        move([30.5,38,8.5]) {
            move([8,15,-5.5]) m3x10_screw();
            move([8,-15,-5.5]) m3x10_screw();
        }
    }
}