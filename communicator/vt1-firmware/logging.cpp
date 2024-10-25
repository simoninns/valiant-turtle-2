/************************************************************************ 

    logging.c

    Valiant Turtle Communicator 2
    Copyright (C) 2024 Simon Inns

    This file is part of Valiant Turtle 2

    This is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Email: simon.inns@gmail.com

************************************************************************/

#include <cstdio>
#include <iostream>
#include <sstream>
#include "pico/stdlib.h"

#include "logging.h"

Logging::Logging(log_level_e _log_level = log_error) {
    std::string log_type = "Unknown";
    if (_log_level == log_error) log_type = "ERROR";
    if (_log_level == log_warning) log_type = "Warning";
    if (_log_level == log_info) log_type = "Info";
    if (_log_level == log_debug) log_type = "Debug";

    _buffer << log_type << ":" 
        << std::string(
            _log_level > log_debug 
            ? (_log_level - log_debug) * 4 
            : 1
            , ' ');
}

Logging::~Logging()
{
    _buffer << std::endl;
    std::cerr << _buffer.str();
}