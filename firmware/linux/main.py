#************************************************************************ 
#
#   main.py
#
#   Valiant Turtle 2 - Communicator Linux Firmware
#   Copyright (C) 2024 Simon Inns
#
#   This file is part of Valiant Turtle 2
#
#   This is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Email: simon.inns@gmail.com
#
#************************************************************************

import library.picolog as picolog
from vt2_mode import Vt2Mode

def main():
    """
    Main entry point for the Valiant Turtle 2 Communicator Linux Firmware.
    """
    # Configure the picolog module
    picolog.basicConfig(level=picolog.DEBUG)

    # Run in VT2 mode
    vt2_mode = Vt2Mode()

    while True:
        vt2_mode.process()

if __name__ == "__main__":
    main()