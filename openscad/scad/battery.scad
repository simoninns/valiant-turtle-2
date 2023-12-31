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

module battery18650_holder_single()
{
    length=83;

    move([0,-1,0]) difference() {
        move([-10,-8,-(length/2)]) cuboid([20,20,length], chamfer=1, center=false);
        move([0,0,0]) cyl(h=length-4, d=19.5);

        move([0,-9,0]) cuboid([22,22,length-4],chamfer=1);

        // Central cross-section
        move([0,-3,0]) cuboid([22,22,30],chamfer=1);

        // Base cut-out
        move([0,2,0]) cuboid([20-14,22,length-18], chamfer=1);

        // Slots for battery tabs
        hull() {
            move([0,4.5,-(length/2)+1]) cuboid([1.5,1,4]);
            move([0,11.51,-(length/2)+1]) cuboid([2,1,4]);
        }

        hull() {
            move([0,4.5,(length/2)-1]) cuboid([1.5,1,4]);
            move([0,11.51,(length/2)-1]) cuboid([2,1,4]);
        }

        // Battery tab clearance
        move([0,6.5,(length/2)-2.25-0.125]) cuboid([7,9,0.75]);
        move([0,6.5,-(length/2)+2.25+0.125]) cuboid([7,9,0.75]);
    }
    
    // Battery tab holders
    move([0,5,(length/2)-2.5]) difference() {
        cuboid([9,8,2.5]);
        cuboid([5,9,3]);
        move([0,0,1]) cuboid([7,9,2.5]);
    }

    move([0,5,-(length/2)+2.5]) difference() {
        cuboid([9,8,2.5]);
        cuboid([5,9,3]);
        move([0,0,-1]) cuboid([7,9,2.5]);
    }
}

module battery_tab_slot(length)
{
    hull() {
        move([0,4.5,-(length/2)+1]) cuboid([1.5,1,4]);
        move([0,11.51,-(length/2)+1]) cuboid([2,1,4]);
    }

    hull() {
        move([0,4.5,(length/2)-1]) cuboid([1.5,1,4]);
        move([0,11.51,(length/2)-1]) cuboid([2,1,4]);
    }

    // Battery tab clearance
    move([0,6.5,(length/2)-2.25-0.125]) cuboid([7,9,0.75]);
    move([0,6.5,-(length/2)+2.25+0.125]) cuboid([7,9,0.75]);
}

module battery_tab_holder(length)
{
    move([0,5,(length/2)-2.5]) difference() {
        cuboid([9,8,2.5]);
        cuboid([5,9,3]);
        move([0,0,1]) cuboid([7,9,2.5]);
    }

    move([0,5,-(length/2)+2.5]) difference() {
        cuboid([9,8,2.5]);
        cuboid([5,9,3]);
        move([0,0,-1]) cuboid([7,9,2.5]);
    }
}

module battery18650_holder_double()
{
    length=83;

    move([0,-1,0]) difference() {
        move([-20,-8,-(length/2)]) cuboid([40,20,length], chamfer=1, center=false);
        move([-9.5,0,0]) cyl(h=length-4, d=19.5);
        move([9.5,0,0]) cyl(h=length-4, d=19.5);

        move([0,-12,0]) cuboid([44,18,length-4],chamfer=1);

        // Centre clearance
        move([0,-1,0]) cuboid([10,18,length-4],chamfer=1);

        // Central cross-section
        move([0,-3,0]) cuboid([44,22,30],chamfer=1);

        // Base cut-out
        move([0,2,0]) cuboid([20-14,22,length-18], chamfer=1);

        // Slots for battery tabs
        move([-9.5,0,0]) battery_tab_slot(length);
        move([9.5,0,0]) battery_tab_slot(length);
    }

    
    
    // Battery tab holders
    move([-9.5,0,0]) battery_tab_holder(length);
    move([9.5,0,0]) battery_tab_holder(length);
}

module render_battery_holder(crend, toPrint)
{
    if (!toPrint) {
        //color([0.4,0.4,0.5]) battery18650_holder_single();
        color([0.4,0.4,0.5]) battery18650_holder_double();
    } else {
        //move([0,0,11]) xrot(-90) battery18650_single();
        move([0,0,11]) xrot(-90) battery18650_holder_double();
    }
}

module render_battery(crend, toPrint)
{
    if (!toPrint) {
        // 1 Battery
        //color([0.3,0.8,0.5]) battery18650();

        // 2 Batteries
        color([0.3,0.8,0.5]) {
            move([9.5,0,0]) battery18650();
            move([-9.5,0,0]) battery18650();
        }
    }
}