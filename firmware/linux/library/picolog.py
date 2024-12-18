#************************************************************************ 
#
#   picolog.py
#
#   Fake logging module for running on the PC
#   Valiant Turtle 2 - Library class
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
import logging as logging

DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

_level = INFO
_uart = None

def basicConfig(level=INFO, uart=None):
    global _level, _uart
    _level = level
    _uart = uart

    # Configure the logging module
    logging.basicConfig(level=logging.INFO, filename="vt2comm.log")

def debug(msg, *args):
    if _level <= DEBUG:
        logging.info("[DEBUG] " + msg.format(*args) + "\n")

def info(msg, *args):
    if _level <= INFO:
        logging.info("[INFO] " + msg.format(*args) + "\n")

def warning(msg, *args):
    if _level <= WARNING:
        logging.info("[WARNING] " + msg.format(*args) + "\n")

def error(msg, *args):
    if _level <= ERROR:
        logging.info("[ERROR] " + msg.format(*args) + "\n")

def critical(msg, *args):
    if _level <= CRITICAL:
        logging.info("[CRITICAL] " + msg.format(*args) + "\n")
