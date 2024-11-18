#************************************************************************ 
#
#   logging.py
#
#   Simple logging module for MicroPython
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

import sys

DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

_level = INFO

def basicConfig(level=INFO, format=None):
    global _level
    _level = level

def debug(msg, *args):
    if _level <= DEBUG:
        print("[DEBUG]", msg.format(*args))

def info(msg, *args):
    if _level <= INFO:
        print("[INFO]", msg.format(*args))

def warning(msg, *args):
    if _level <= WARNING:
        print("[WARNING]", msg.format(*args))

def error(msg, *args):
    if _level <= ERROR:
        print("[ERROR]", msg.format(*args))

def critical(msg, *args):
    if _level <= CRITICAL:
        print("[CRITICAL]", msg.format(*args))