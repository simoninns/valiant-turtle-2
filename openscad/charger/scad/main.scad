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

// Other project includes
include <../../robot/scad/battery.scad>

// Local includes
include <base.scad>
include <lid.scad>
include <connector.scad>
include <pcb.scad>
include <light_pipe.scad>

// Rendering resolution
$fn=100;

/* [Rendering Parameters] */
// Select Display for viewing the model or Printing to orientate parts for STL generation
for_printing = "Display"; // [Display, Printing]

/* [Printable Parts] */
display_charger_base = "No"; // [Yes, No]
display_charger_lid = "No"; // [Yes, No]
display_connector_front = "No"; // [Yes, No]
display_connector_back = "No"; // [Yes, No]
display_light_pipe = "No"; // [Yes, No]

/* [Support Enforcers] */
display_charger_lid_support_enforcers = "No"; // [Yes, No]

/* [Non-Printable Parts] */
display_battery = "No"; // [Yes, No]
display_pcb = "No"; // [Yes, No]

/* [Screws] */
display_charger_lid_screws = "No"; // [Yes, No]

// Render the required items
module main() {
    // Rendering parameters
    toPrint = (for_printing == "Printing") ? true:false;

    // Printable parts
    d_charger_base = (display_charger_base == "Yes") ? true:false;
    d_charger_lid = (display_charger_lid == "Yes") ? true:false;
    d_connector_front = (display_connector_front == "Yes") ? true:false;
    d_connector_back = (display_connector_back == "Yes") ? true:false;
    d_light_pipe = (display_light_pipe == "Yes") ? true:false;

    // Support enforcers
    d_charger_lid_support_enforcers = (display_charger_lid_support_enforcers == "Yes") ? true:false;

    // Non-printable parts
    d_battery = (display_battery == "Yes") ? true:false;
    d_pcb = (display_pcb == "Yes") ? true:false;

    // Screws
    d_charger_lid_screws = (display_charger_lid_screws == "Yes") ? true:false;

    // Render the printable parts
    if (d_charger_base) render_charger_base(toPrint);
    if (d_charger_lid) render_charger_lid(toPrint);
    if (d_connector_front) render_connector_front(toPrint);
    if (d_connector_back) render_connector_back(toPrint);
    if (d_light_pipe) render_light_pipe(toPrint);

    // Render the support enforcers
    if (d_charger_lid_support_enforcers) render_charger_lid_support_enforcers(toPrint);

    // Render the non-printable parts
    if (d_battery) {
        if (!toPrint) {
            move([0,-12 + 8,46]) xrot(180) {
                render_battery_pack(false);
                render_battery_pack_lower_cover(false);
                render_battery_pack_upper_cover(false);
                render_battery_pack_connector_cover(false);
            }
        }
    }

    if (d_pcb) render_pcb(toPrint);

    // Render screws
    if (d_charger_lid_screws) render_charger_lid_screws(toPrint);
}

main();