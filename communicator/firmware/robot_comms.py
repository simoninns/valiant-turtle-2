#************************************************************************ 
#
#   robot_comms.py
#
#   Classes for robot communications
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

class PowerMonitor:
    def __init__(self, voltage_mV: float = 0, current_mA: float = 0, power_mW: float = 0):
        """Class to store power monitor status information"""
        self._voltage_mV = voltage_mV
        self._current_mA = current_mA
        self._power_mW = power_mW

    @property
    def voltage_mV(self):
        """Get the power monitor voltage in mV"""
        return  self._voltage_mV
    
    @property
    def voltage_mV_fstring(self) -> str:
        """Get the power monitor voltage as a formatted string"""
        return "{:.2f} mV".format(self._voltage_mV)
    
    @property
    def voltage_V_fstring(self) -> str:
        """Get the power monitor voltage as a formatted string"""
        return "{:.2f} V".format(self._voltage_mV/1000)
    
    @property
    def current_mA(self):
        """Get the power monitor current in mA"""
        return  self._current_mA
    
    @property
    def current_mA_fstring(self) -> str:
        """Get the power monitor current as a formatted string"""
        return "{:.2f} mA".format(self._current_mA)
    
    @property
    def power_mW(self):
        """Get the power monitor power in mW"""
        return  self._power_mW
    
    @property
    def power_mW_fstring(self) -> str:
        """Get the power monitor power as a formatted string"""
        return "{:.2f} mW".format(self._power_mW)

    @voltage_mV.setter
    def voltage_mV(self, value):
        """Set the power monitor voltage in mV"""
        self._voltage_mV = value

    @current_mA.setter
    def current_mA(self, value):
        """Set the power monitor current in mA"""
        self._current_mA = value

    @power_mW.setter
    def voltage_mV(self, value):
        """Set the power monitor power in mW"""
        self._power_mW = value

    @property
    def status(self):
        """Get the power monitor status as a tuple containing voltage, current and power (mV, mA, mW)"""
        return (self._voltage_mV, self._current_mA, self._power_mW)

    @status.setter
    def status(self, values):
        """Set the power monitor status as a tuple containing voltage, current and power (mV, mA, mW)"""
        self._voltage_mV, self._current_mA, self._power_mW = values


class StatusBitFlag:
    def __init__(self):
        """
        Initializes the status bit flag object with all flags set to 0.
        Flags:
            Bit 0: Result of last command (1 = success, 0 = failure)
            Bit 1: Left Motor Busy
            Bit 2: Right Motor Busy
            Bit 3: Left Motor Direction (1 = Forward, 0 = Reverse)
            Bit 4: Right Motor Direction (1 = Forward, 0 = Reverse)
            Bit 5: Motor Power Enabled
            Bit 6: Pen Servo On/Off (1 = On, 0 = Off)
            Bit 7: Pen Servo Up/Down (1 = Up, 0 = Down)

        Bits 8-31 are reserved for future use.
        """
        self._flags = 0

    @property
    def result(self) -> bool:
        """Result of last command (True = success, False = failure)"""
        return self.__is_bit_flag_set(0)
    
    @result.setter
    def result(self, value: bool):
        """Set the result of last command (True = success, False = failure)"""
        self.__change_bit_flag(0, value)
    
    @property
    def left_motor_busy(self) -> bool:
        """Left motor busy flag (True = busy, False = not busy)"""
        return self.__is_bit_flag_set(1)
    
    @left_motor_busy.setter
    def left_motor_busy(self, value: bool):
        """Set the left motor busy flag (True = busy, False = not busy)"""
        self.__change_bit_flag(1, value)
    
    @property
    def right_motor_busy(self) -> bool:
        """Right motor busy flag (True = busy, False = not busy)"""
        return self.__is_bit_flag_set(2)
    
    @right_motor_busy.setter
    def right_motor_busy(self, value: bool):
        """Set the right motor busy flag (True = busy, False = not busy)"""
        self.__change_bit_flag(2, value)

    @property
    def left_motor_direction(self) -> bool:
        """Left motor direction (True = forward, False = reverse)"""
        return self.__is_bit_flag_set(3)
    
    @left_motor_direction.setter
    def left_motor_direction(self, value: bool):
        """Set the left motor direction (True = forward, False = reverse)"""
        self.__change_bit_flag(3, value)

    @property
    def right_motor_direction(self) -> bool:
        """Right motor direction (True = forward, False = reverse)"""
        return self.__is_bit_flag_set(4)
    
    @right_motor_direction.setter
    def right_motor_direction(self, value: bool):
        """Set the right motor direction (True = forward, False = reverse)"""
        self.__change_bit_flag(4, value)

    @property
    def motor_power_enabled(self) -> bool:
        """Motor power enabled (True = enabled, False = disabled"""
        return self.__is_bit_flag_set(5)
    
    @motor_power_enabled.setter
    def motor_power_enabled(self, value: bool):
        """Set the motor power enabled (True = enabled, False = disabled)"""
        self.__change_bit_flag(5, value)

    @property
    def pen_servo_on(self) -> bool:
        """Pen servo on/off (True = on, False = off)"""
        return self.__is_bit_flag_set(6)
    
    @pen_servo_on.setter
    def pen_servo_on(self, value: bool):
        """Set the pen servo on/off (True = on, False = off)"""
        self.__change_bit_flag(6, value)

    @property
    def pen_servo_up(self) -> bool:
        """Pen servo up/down (True = up, False = down)"""
        return self.__is_bit_flag_set(7)
    
    @pen_servo_up.setter
    def pen_servo_up(self, value: bool):
        """Set the pen servo up/down (True = up, False = down)"""
        self.__change_bit_flag(7, value)

    @property
    def flags(self) -> int:
        """Get all flags as an integer."""
        return self._flags
    
    @flags.setter
    def flags(self, value: int):
        """Set all flags from an integer."""
        self._flags = value

    def __change_bit_flag(self, position: int, value: bool):
        """
        Change the bit flag at the specified position.
        Args:
            position (int): The position of the bit to change (must be between 0 and 31).
            value (bool): The value to set the bit to (True to set the bit, False to clear the bit).
        Raises:
            ValueError: If the position is not between 0 and 31.
        """

        if 0 <= position < 32:
            if value:
                self._flags |= (1 << position)
            else:
                self._flags &= ~(1 << position)
        else:
            raise ValueError("Position must be between 0 and 31")

    def __is_bit_flag_set(self, position: int):
        """
        Check if the bit flag at the specified position is set.
        Args:
            position (int): The position of the bit flag to check (0-31).
        Returns:
            bool: True if the bit flag at the specified position is set, False otherwise.
        Raises:
            ValueError: If the position is not between 0 and 31.
        """

        if 0 <= position < 32:
            return (self._flags & (1 << position)) != 0
        else:
            raise ValueError("Position must be between 0 and 31")
    
    def display_flags(self) -> str:
        """
        Returns a string representation of the status flags in a 32-bit binary format.
        Returns:
            str: A 32-bit binary string representing the status flags.
        """
        
        return f'{self._flags:032b}'

if __name__ == "__main__":
    from main import main
    main()