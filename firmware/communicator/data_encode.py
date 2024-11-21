#************************************************************************ 
#
#   data_encode.py
#
#   Data type encoding and decoding functions
#   Valiant Turtle 2 - Communicator firmware
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

import struct

# signed short integer (2 bytes)
def to_int16(value):
    return struct.pack("<h", int(value))

def from_int16(data) -> int:
    return struct.unpack("<h", data)[0]

# unsigned short integer (2 bytes)
def to_uint16(value):
    return struct.pack("<H", int(value))

def from_uint16(data) -> int:
    return struct.unpack("<H", data)[0]

# signed long integer (4 bytes)
def to_int32(value):
    return struct.pack("<l", int(value))

def from_int32(data) -> int:
    return struct.unpack("<l", data)[0]

# unsigned long integer (4 bytes)
def to_uint32(value):
    return struct.pack("<L", int(value))

def from_uint32(data) -> int:
    return struct.unpack("<L", data)[0]

# float (4 bytes)
def to_float(value):
    return struct.pack("<f", float(value))

def from_float(data) -> float:
    return struct.unpack("<f", data)[0]

if __name__ == "__main__":
    from main import main
    main()