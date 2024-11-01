#************************************************************************ 
#
#   byte_fifo.py
#
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

# This needs some sort of run-time limit on size?
class Byte_fifo:
    def __init__(self):
        self._buf = bytearray()

    # Put data into the FIFO
    def put(self, data):
        self._buf.extend(data)

    # Remove data from the FIFO
    def get(self, size):
        data = self._buf[:size]
        # The fast delete syntax
        self._buf[:size] = b''
        return data

    # Get data from the FIFO without removing it
    def peek(self, size):
        return self._buf[:size]

    # Get data from the FIFO without removing it
    def get_value(self):
        # peek with no copy
        return self._buf

    # Return the current buffer size
    def any(self):
        return len(self._buf)