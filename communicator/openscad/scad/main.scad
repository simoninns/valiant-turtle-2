/************************************************************************

    main.scad
    
    Valiant Turtle Communicator 2
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
include <case.scad>
include <ircover.scad>
include <panel.scad>
include <label.scad>
include <logotype.scad>

// Rendering resolution
$fn=100;

// Select rendering parameters
for_printing = "Display"; // [Display, Printing]

// Choose what to display
display_case_base = "Yes"; // [Yes, No]
display_case_top = "Yes"; // [Yes, No]
display_ircover = "Yes"; // [Yes, No]
display_panel_left = "Yes"; // [Yes, No]
display_panel_right = "Yes"; // [Yes, No]
display_panel_back = "Yes"; // [Yes, No]
display_panel_front = "Yes"; // [Yes, No]
display_label = "Yes"; // [Yes, No]
display_logo = "Yes"; // [Yes, No]

display_case_screws = "Yes"; // [Yes, No]
display_pcb_screws = "Yes"; // [Yes, No]

// Render the required items
module main() {
    // Main options
    toPrint = (for_printing == "Printing") ? true:false;

    // Display selections
    d_case_base = (display_case_base == "Yes") ? true:false;
    d_case_top = (display_case_top == "Yes") ? true:false;
    d_ircover = (display_ircover == "Yes") ? true:false;
    d_panel_left = (display_panel_left == "Yes") ? true:false;
    d_panel_right = (display_panel_right == "Yes") ? true:false;
    d_panel_back = (display_panel_back == "Yes") ? true:false;
    d_panel_front = (display_panel_front == "Yes") ? true:false;
    d_label = (display_label == "Yes") ? true:false;
    d_logo = (display_logo == "Yes") ? true:false;

    d_case_screws = (display_case_screws == "Yes") ? true:false;
    d_pcb_screws = (display_pcb_screws == "Yes") ? true:false;

    if (d_case_base) render_case_base(toPrint);
    if (d_case_top) render_case_top(toPrint);
    if (d_ircover) render_ircover(toPrint);
    if (d_panel_left) render_panel_left(toPrint);
    if (d_panel_right) render_panel_right(toPrint);
    if (d_panel_back) render_panel_back(toPrint);
    if (d_panel_front) render_panel_front(toPrint);
    if (d_label) render_label(toPrint);
    if (d_logo) render_logotype(toPrint);

    if (d_case_screws) render_case_screws(toPrint);
    if (d_pcb_screws) render_pcb_screws(toPrint);
}

main();