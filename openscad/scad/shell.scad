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
module pentagon()
{
    hull() {
        zrot((360/5) * 0) move([0,114/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 1) move([0,114/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 2) move([0,114/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 3) move([0,114/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 4) move([0,114/2,0]) staggered_sphere(d=2, $fn=18);
    }
}

// This is a bit of an odd shape... to get it right I made it 2D and printed
// it to scale and adjusted until it matched the original pretty closely.
module irrPentagonTop()
{
    hull() {
        zrot((360/5) * 0) move([0,103/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 1) move([0,123/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 2) move([0,114/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 3) move([0,114/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 4) move([0,123/2,0]) staggered_sphere(d=2, $fn=18);
    }
}

module irrPentagonBottom()
{
    hull() {
        zrot((360/5) * 0) move([0,105.5/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 1) move([0,120.5/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 2) move([0,104.5/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 3) move([0,104.5/2,0]) staggered_sphere(d=2, $fn=18);
        zrot((360/5) * 4) move([0,120.5/2,0]) staggered_sphere(d=2, $fn=18);
    }
}

module shellTop()
{
    yrot(180) {
        // Centre
        pentagon();

        for ( i = [0:1:4]) {
            zrot((360/5) * i) {
                zrot(360/10) move([0,70.5,39.25]) xrot(58.25) irrPentagonTop();
            }
        }
    }
}

module shellBottom()
{
    zrot(360/10) for ( i = [0:1:4]) {
        zrot((360/5) * i) {
            zrot(360/10) move([0,67.75,40]) xrot(53.25) irrPentagonBottom();
        }
    }
}

module shell()
{
    difference() {
        union() {
            move([0,0,110]) shellTop();
            move([0,0,-28]) shellBottom();
        }
        move([0,0,-20]) cuboid([200,200,40]);
    }
}

module render_shell(crend, toPrint)
{
    shell();
}