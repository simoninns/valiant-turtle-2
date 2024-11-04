#************************************************************************ 
#
#   log.py
#
#   Logging methods
#   Valiant Turtle 2 - Robot firmware
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

from machine import RTC, UART

debug_uart = None
is_logging_debug = False
is_logging_info = False
is_logging_warn = False

def log_control(debug: bool, info: bool, warn: bool):
    global is_logging_debug
    global is_logging_info
    global is_logging_warn
    is_logging_debug = debug
    is_logging_info = info
    is_logging_warn = warn

    # Output some whitespace and a header
    if (debug or info or warn):
        print("\r")
        print("\r")
        print("Valiant Turtle 2 - Communicator - Debug output\r")

def log_debug(*args, **kwargs):
    global is_logging_debug
    if is_logging_debug: print("Debug: "+" ".join(map(str,args))+"\r", **kwargs)

def log_info(*args, **kwargs):
    global is_logging_info
    if is_logging_debug: print("Info: "+" ".join(map(str,args))+"\r", **kwargs)

def log_warn(*args, **kwargs):
    global is_logging_warn
    if is_logging_debug: print("Warn: "+" ".join(map(str,args))+"\r", **kwargs)