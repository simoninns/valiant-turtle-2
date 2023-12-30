/************************************************************************

    battery.scad
    
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

module battery18650()
{
    // 18650 Battery with protection circuit
    difference() {
        cyl(h=69, d=18.5);
        move([0,0,(69/2)]) cyl(h=0.5, d=13);
        move([0,0,-(69/2)]) cyl(h=0.5, d=13);
    }
    
    move([0,0,(69/2)+0.25]) cyl(h=1, d=5);
}

module battery18650_holder()
{
    move([0,-1,0]) difference() {
        move([0,2,0]) cuboid([20,20,86+2], chamfer=1);
        move([0,-1,0]) cuboid([20-2,22,86-2]);
        move([0,-9,0]) cuboid([22,22,86-2],chamfer=1);
        move([0,-3,0]) cuboid([22,22,20],chamfer=1);

        move([0,2,0]) cuboid([20-10,22,86-16], chamfer=1);

        hull() {
            move([0,4.5,-43]) cuboid([1.5,1,4]);
            move([0,11.51,-43]) cuboid([2,1,4]);
        }
        move([0,-3,-43]) cyl(h=4,d=2);

        hull() {
            move([0,4.5,43]) cuboid([1.5,1,4]);
            move([0,11.51,43]) cuboid([2,1,4]);
        }
        move([0,-3,43]) cyl(h=4,d=2);
    }
   
    // Battery tab holders
    move([0,5,41]) difference() {
        cuboid([9,8,2.5]);
        cuboid([5,9,3]);
        move([0,0,1]) cuboid([7,9,2.5]);
    }

    move([0,5,-41]) difference() {
        cuboid([8,8,2]);
        cuboid([4,9,3]);
        move([0,0,-1]) cuboid([6,9,2]);
    }
}

module render_battery_holder(crend, toPrint)
{
    if (!toPrint) {
        color([0.4,0.4,0.5]) battery18650_holder();
    } else {
        move([0,0,11]) xrot(-90) battery18650_holder();
    }
}

module render_battery(crend, toPrint)
{
    if (!toPrint) {
        color([0.3,0.8,0.5]) battery18650();
    }
}