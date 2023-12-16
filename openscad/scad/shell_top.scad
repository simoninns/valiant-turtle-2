/************************************************************************

    shell_top.scad
    
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

module pentagonTop()
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

module shellTop()
{
    move([0,1.5,105]) yrot(180) {
        // Centre
        pentagonTop();

        for ( i = [0:1:4]) {
            zrot((360/5) * i) {
                zrot(360/10) move([0,70,36.75]) xrot(55.5) irrPentagonTop();
            }
        }
    }
}

module joinerLine()
{
    hull() {
        zrot(360/10) move([0,70,36.75]) xrot(55.5) {
            zrot((360/5) * 0) move([0,(103/2),0]) staggered_sphere(d=2, $fn=16);
            zrot((360/5) * 1) move([0,(123/2),0]) staggered_sphere(d=2, $fn=16);
        }
    }

    hull() {
        zrot(360/10) move([0,70,36.75]) xrot(55.5) {
            zrot((360/5) * 0) move([0,(103/2),0]) staggered_sphere(d=2, $fn=16);
            zrot((360/5) * 4) move([0,(123/2),0]) staggered_sphere(d=2, $fn=16);
        }
    }
}

module joiner()
{
    move([0,1.5,104]) yrot(180) {
        for ( i = [0:1:4]) {
            zrot((360/5) * i) joinerLine();
        }
    }
}

module render_shell_top(crend, toPrint)
{
    if (!toPrint) {
        color([0,0.8,0,1]) shellTop();
        color([0,0.8,0,1]) joiner();
    } else {  
        move([0,0,106]) xrot(180) {
            shellTop();
            joiner();
        }
    }
}