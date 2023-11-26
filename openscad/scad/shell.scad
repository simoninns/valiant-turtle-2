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

// Render a pentagon with a radius = pr
module pentagon(pr)
{
    hull() {
        for ( i = [0:1:5]) {
            zrot((360/5) * i) move([0,pr,0]) staggered_sphere(d=2, $fn=18);
        }
    }
}

module half_shell()
{
    // Centre
    pentagon(110/2);

    for ( i = [0:1:5]) {
        zrot((360/5) * i) {
            zrot(360/10) move([0,128.75/2,79.75/2]) xrot(63.5) pentagon(110/2);
        }
    }
}

module render_shell()
{
    move([0,0,110]) {
        // Top shell
        yrot(180) half_shell();

        // Bottom shell
        move([0,0,-105]) difference() {
            move([0,0,-39.5]) zrot(360/10) half_shell();
            move([0,0,-55]) cuboid([200,200,100]);
        }
    }
}