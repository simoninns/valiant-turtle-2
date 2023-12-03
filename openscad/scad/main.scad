/************************************************************************

    main.scad
    
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

// Local includes
include <body.scad>
include <head.scad>
include <shell_top.scad>
include <shell_bottom.scad>

// Rendering resolution
$fn=50;

// Select rendering parameters
use_colour = "Colour"; // [Colour, No colour]
for_printing = "Display"; // [Display, Printing]

display_body = "Yes"; // [Yes, No]
display_head = "Yes"; // [Yes, No]
display_shell_top = "Yes"; // [Yes, No]
display_shell_bottom = "Yes"; // [Yes, No]

module main() {
    crend = (use_colour == "Colour") ? true:false;
    toPrint = (for_printing == "Printing") ? true:false;

    d_body = (display_body == "Yes") ? true:false;
    d_head = (display_head == "Yes") ? true:false;
    d_shell_top = (display_shell_top == "Yes") ? true:false;
    d_shell_bottom = (display_shell_bottom == "Yes") ? true:false;

    // Render the required items
    if (d_body) render_body(crend, toPrint);
    if (d_head) render_head(crend, toPrint);
    if (d_shell_top) render_shell_top(crend, toPrint);
    if (d_shell_bottom) render_shell_bottom(crend, toPrint);
}

main();