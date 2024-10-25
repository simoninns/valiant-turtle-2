/************************************************************************ 

    logging.h

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

#ifndef LOGGING_H_
#define LOGGING_H_

#include <sstream>

// Enumeration of logging levels
enum log_level_e {
    log_error,
    log_warning,
    log_info,
    log_debug};

class Logging
{
public:
    Logging(log_level_e _log_level);
    ~Logging();

    template <typename T>
    Logging & operator<<(T const & value)
    {
        _buffer << value;
        return *this;
    }

private:
    std::ostringstream _buffer;
};

extern log_level_e log_level;

#define log(level) \
if (level > log_level) ; \
else Logging(level)

#endif /* LOGGING_H_ */