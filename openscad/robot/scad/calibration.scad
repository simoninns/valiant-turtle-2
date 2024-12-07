/************************************************************************

    calibration.scad
    
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

module calibration_bracket()
{
    cuboid([237.5,14,4], chamfer = 1);

    move([-62,0,10]) cuboid([4,10,20], chamfer = 1);
    move([+62,0,10]) cuboid([4,10,20], chamfer = 1);

    move([-116.75,0,10]) cuboid([4,10,20], chamfer = 1);
    move([+116.75,0,10]) cuboid([4,10,20], chamfer = 1);

    move([-107.25,0,9]) cuboid([4,10,18], chamfer = 1);
    move([+107.25,0,9]) cuboid([4,10,18], chamfer = 1);
}

module render_calibration_bracket(toPrint)
{
    if (!toPrint) {
        move([0,64 - 35,-36]) calibration_bracket();
    } else {
        move([0,0,2]) zrot(45) calibration_bracket();
    }
}