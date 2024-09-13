/************************************************************************

    main.scad
    
    Valiant Turtle 2 - Battery Charger
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
include <base.scad>

// Rendering resolution
$fn=100;

// Select rendering parameters
for_printing = "Display"; // [Display, Printing]

// Choose what to display
display_charger_base = "Yes"; // [Yes, No]
display_charger_screws = "Yes"; // [Yes, No]

// Render the required items
module main() {
    // Main options
    toPrint = (for_printing == "Printing") ? true:false;

    // Display selections
    d_charger_base = (display_charger_base == "Yes") ? true:false;
    d_charger_screws = (display_charger_screws == "Yes") ? true:false;

    if (d_charger_base) render_charger_base(toPrint);
    if (d_charger_screws) render_charger_screws(toPrint);
}

main();