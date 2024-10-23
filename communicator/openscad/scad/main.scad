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
include <holder.scad>

// Rendering resolution
$fn=100;

/* [Rendering Parameters] */
// Select Display for viewing the model or Printing to orientate parts for STL generation
for_printing = "Display"; // [Display, Printing]

/* [Printable Parts] */
display_case_base = "No"; // [Yes, No]
display_case_top = "No"; // [Yes, No]
display_panel_front = "No"; // [Yes, No]
display_panel_back = "No"; // [Yes, No]
display_panel_left = "No"; // [Yes, No]
display_panel_right = "No"; // [Yes, No]
display_label = "No"; // [Yes, No]
display_logo = "No"; // [Yes, No]
display_led_holder = "No"; // [Yes, No]

/* [Support Enforcers] */

/* [Non-Printable Parts] */
display_ir_cover = "No"; // [Yes, No]

/* [Screws] */
display_case_screws = "No"; // [Yes, No]
display_pcb_screws = "No"; // [Yes, No]

// Render the required items
module main() {
    // Rendering parameters
    toPrint = (for_printing == "Printing") ? true:false;

    // Printable parts
    d_case_base = (display_case_base == "Yes") ? true:false;
    d_case_top = (display_case_top == "Yes") ? true:false;
    d_panel_front = (display_panel_front == "Yes") ? true:false;
    d_panel_back = (display_panel_back == "Yes") ? true:false;
    d_panel_left = (display_panel_left == "Yes") ? true:false;
    d_panel_right = (display_panel_right == "Yes") ? true:false;
    d_label = (display_label == "Yes") ? true:false;
    d_logo = (display_logo == "Yes") ? true:false;
    d_led_holder = (display_led_holder == "Yes") ? true:false;

    // Support enforcers
    // Non-printable parts
    d_ir_cover = (display_ir_cover == "Yes") ? true:false;

    // Screws
    d_case_screws = (display_case_screws == "Yes") ? true:false;
    d_pcb_screws = (display_pcb_screws == "Yes") ? true:false;

    // Render the printable parts
    if (d_case_base) render_case_base(toPrint);
    if (d_case_top) render_case_top(toPrint);
    if (d_panel_left) render_panel_left(toPrint);
    if (d_panel_right) render_panel_right(toPrint);
    if (d_panel_back) render_panel_back(toPrint);
    if (d_panel_front) render_panel_front(toPrint);
    if (d_label) render_label(toPrint);
    if (d_logo) render_logotype(toPrint);
    if (d_led_holder) render_holder(toPrint);

    // Render the support enforcers
    // Render the non-printable parts
    if (d_ir_cover) render_ircover(toPrint);

     // Render screws
    if (d_case_screws) render_case_screws(toPrint);
    if (d_pcb_screws) render_pcb_screws(toPrint);
}

main();