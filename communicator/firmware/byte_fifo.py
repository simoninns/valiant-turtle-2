#************************************************************************ 
#
#   byte_fifo.py
#
#   Byte FIFO for use with communication ISRs
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

class Byte_fifo:
    def __init__(self, size):
        self.data = bytearray(size)
        self.size = size
        self.index_put = 0
        self.index_get = 0
        
    def write(self, value):
        next_index = (self.index_put + 1) % self.size
        # check for overflow
        if self.index_get != next_index: 
            self.data[self.index_put] = value
            self.index_put = next_index
            return value
        else:
            return None
        
    def read(self):
        if self.index_get == self.index_put:
            return None  # Buffer empty
        else:
            value = self.data[self.index_get]
            self.index_get = (self.index_get + 1) % self.size
            return value
        
    # Returns False if FIFO is empty
    def any(self) -> bool:
        if self.index_get == self.index_put:
            return False
        return True