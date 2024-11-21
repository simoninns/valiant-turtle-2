/************************************************************************

    main.scad
    
    Valiant Turtle Parallel to Acorn BBC User-port adapter
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

// Local includes
include <case.scad>

// Rendering resolution
$fn=100;

/* [Rendering Parameters] */
// Select Display for viewing the model or Printing to orientate parts for STL generation
for_printing = "Display"; // [Display, Printing]

/* [Printable Parts] */
display_case_bottom = "No"; // [Yes, No]
display_case_top = "No"; // [Yes, No]

/* [Support Enforcers] */
display_support_enforcers = "No"; // [Yes, No]

/* [Non-Printable Parts] */

/* [Screws] */
display_case_screws = "No"; // [Yes, No]

// Render the required items
module main() {
    // Rendering parameters
    toPrint = (for_printing == "Printing") ? true:false;

    // Printable parts
    d_case_bottom = (display_case_bottom == "Yes") ? true:false;
    d_case_top = (display_case_top == "Yes") ? true:false;

    // Support enforcers
    d_support_enforcers = (display_support_enforcers == "Yes") ? true:false;

    // Non-printable parts

    // Screws
    d_case_screws = (display_case_screws == "Yes") ? true:false;

    // Render the printable parts
    if (d_case_bottom) render_case_bottom(toPrint);
    if (d_case_top) render_case_top(toPrint);

    // Render the support enforcers
    if (d_support_enforcers) render_support_enforcers(toPrint);
    // Render the non-printable parts

     // Render screws
    if (d_case_screws) render_case_screws(toPrint);
}

main();