#************************************************************************ 
#
#   robot_comms.py
#
#   Classes for robot communications over BLE
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

import struct

class PowerMonitor:
    def __init__(self, voltage_mV: float = 0, current_mA: float = 0, power_mW: float = 0):
        """Class to store power monitor status information"""
        self._voltage_mV = voltage_mV
        self._current_mA = current_mA
        self._power_mW = power_mW

    @property
    def voltage_mV(self):
        """Get the power monitor voltage in millivolts (mV)"""
        return  self._voltage_mV
    
    @property
    def voltage_mV_fstring(self) -> str:
        """Get the power monitor voltage as a formatted string in millivolts (mV)"""
        return "{:.2f} mV".format(self._voltage_mV)
    
    @property
    def voltage_V_fstring(self) -> str:
        """Get the power monitor voltage as a formatted string in volts (V)"""
        return "{:.2f} V".format(self._voltage_mV/1000)
    
    @property
    def current_mA(self):
        """Get the power monitor current in milliamps (mA)"""
        return  self._current_mA
    
    @current_mA.setter
    def current_mA(self, value):
        """Set the power monitor current in milliamps (mA)"""
        self._current_mA = value
    
    @property
    def current_mA_fstring(self) -> str:
        """Get the power monitor current as a formatted string in milliamps (mA)"""
        return "{:.2f} mA".format(self._current_mA)
    
    @property
    def power_mW(self):
        """Get the power monitor power in mW"""
        return self._power_mW
    
    @power_mW.setter
    def power_mW(self, value):
        """Set the power monitor power in milliwatts (mW)"""
        self._power_mW = value
    
    @property
    def power_mW_fstring(self) -> str:
        """Get the power monitor power as a formatted string in milliwatts (mW)"""
        return "{:.2f} mW".format(self._power_mW)

    @property
    def status(self):
        """Get the power monitor status as a tuple containing voltage, current and power (mV, mA, mW)"""
        return (self._voltage_mV, self._current_mA, self._power_mW)

    @status.setter
    def status(self, values):
        """Set the power monitor status as a tuple containing voltage, current and power (mV, mA, mW)"""
        self._voltage_mV, self._current_mA, self._power_mW = values

    def __str__(self):
        """Return a string representation of the power monitor status"""
        return f"Voltage: {self.voltage_mV_fstring}, Current: {self.current_mA_fstring}, Power: {self.power_mW_fstring}"


class StatusBitFlag:
    def __init__(self):
        """
        Initializes the status bit flag object with all flags set to 0.
        Flags:
            Bit 0: Left Motor Busy
            Bit 1: Right Motor Busy
            Bit 2: Left Motor Direction (1 = Forward, 0 = Reverse)
            Bit 3: Right Motor Direction (1 = Forward, 0 = Reverse)
            Bit 4: Motor Power Enabled
            Bit 5: Pen Servo On/Off (1 = On, 0 = Off)
            Bit 6: Pen Servo Up/Down (1 = Up, 0 = Down)

        Bits 7-31 are reserved for future use.
        """
        self._flags = 0
    
    @property
    def left_motor_busy(self) -> bool:
        """Left motor busy flag (True = busy, False = not busy)"""
        return self.__is_bit_flag_set(0)
    
    @left_motor_busy.setter
    def left_motor_busy(self, value: bool):
        """Set the left motor busy flag (True = busy, False = not busy)"""
        self.__change_bit_flag(0, value)
    
    @property
    def right_motor_busy(self) -> bool:
        """Right motor busy flag (True = busy, False = not busy)"""
        return self.__is_bit_flag_set(1)
    
    @right_motor_busy.setter
    def right_motor_busy(self, value: bool):
        """Set the right motor busy flag (True = busy, False = not busy)"""
        self.__change_bit_flag(1, value)

    @property
    def left_motor_direction(self) -> bool:
        """Left motor direction (True = forward, False = reverse)"""
        return self.__is_bit_flag_set(2)
    
    @left_motor_direction.setter
    def left_motor_direction(self, value: bool):
        """Set the left motor direction (True = forward, False = reverse)"""
        self.__change_bit_flag(2, value)

    @property
    def right_motor_direction(self) -> bool:
        """Right motor direction (True = forward, False = reverse)"""
        return self.__is_bit_flag_set(3)
    
    @right_motor_direction.setter
    def right_motor_direction(self, value: bool):
        """Set the right motor direction (True = forward, False = reverse)"""
        self.__change_bit_flag(3, value)

    @property
    def motor_power_enabled(self) -> bool:
        """Motor power enabled (True = enabled, False = disabled"""
        return self.__is_bit_flag_set(4)
    
    @motor_power_enabled.setter
    def motor_power_enabled(self, value: bool):
        """Set the motor power enabled (True = enabled, False = disabled)"""
        self.__change_bit_flag(4, value)

    @property
    def pen_servo_on(self) -> bool:
        """Pen servo on/off (True = on, False = off)"""
        return self.__is_bit_flag_set(5)
    
    @pen_servo_on.setter
    def pen_servo_on(self, value: bool):
        """Set the pen servo on/off (True = on, False = off)"""
        self.__change_bit_flag(5, value)

    @property
    def pen_servo_up(self) -> bool:
        """Pen servo up/down (True = up, False = down)"""
        return self.__is_bit_flag_set(6)
    
    @pen_servo_up.setter
    def pen_servo_up(self, value: bool):
        """Set the pen servo up/down (True = up, False = down)"""
        self.__change_bit_flag(6, value)

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
    
    def __str__(self):
        """Return a string representation of the status flags."""
        status_str = f"Status flags [{self.display_flags()}]:\r\n"

        if self.left_motor_busy:
            status_str += "             Left motor: Busy\r\n"
        else:
            status_str += "             Left motor: Idle\r\n"

        if self.right_motor_busy:
            status_str += "            Right motor: Busy\r\n"
        else:
            status_str += "            Right motor: Idle\r\n"

        if self.left_motor_direction:
            status_str += "   Left motor direction: Forward\r\n"
        else:
            status_str += "   Left motor direction: Backward\r\n"

        if self.right_motor_direction:
            status_str += "  Right motor direction: Forward\r\n"
        else:
            status_str += "  Right motor direction: Backward\r\n"

        if self.motor_power_enabled:
            status_str += "            Motor power: Enabled\r\n"
        else:
            status_str += "            Motor power: Disabled\r\n"

        if self.pen_servo_on:
            if self.pen_servo_up:
                status_str += "              Pen servo: Up\r\n"
            else:
                status_str += "              Pen servo: Down\r\n"
        else: status_str += "              Pen servo: Off\r\n"

        return status_str

class RobotCommand:
    """
    The RobotCommand class represents a command that can be sent to a robot. Each command has a unique ID and a set of parameters.
    Attributes:
        _command_dictionary (dict): A dictionary containing command details. Each command is mapped to a tuple containing:
            - Unique ID (int)
            - Number of parameters (int)
            - Minimum values for parameters (tuple)
            - Maximum values for parameters (tuple)
            - Descriptions for parameters (tuple)
            - Help text (str)
    Methods:
        __init__(command: str = "nop", parameters: list = []):
        command() -> str:
            Get the command name.
        command_id() -> int:
            Get the command ID.
        _pack_command() -> bytes:
        get_packed_bytes() -> bytes:
        _id_to_command(command_id: int) -> str:
        from_packed_bytes(byte_array: bytes):
        num_parameters(command: str) -> int:
        parameter_range(command: str, param_num: int) -> tuple:
        is_command_valid(command: str) -> bool:
        help_text() -> str:
        __str__() -> str:
    """

    # Command parameters: name (unique ID, number of parameters)
    # Note: The maximum number of parameters supported is 4
    _command_dictionary = {
        # Dictionary of commands:
        # Command: "name" (unique ID, number of parameters, (param1_min, ...), (param1_max, ...), (param1_desc, ...), "help_text")
        "nop":        ( 0, 0, (0, 0, 0, 0), (0, 0, 0, 0), ("" , "", "", ""), "No operation"),
        "motors-on":  ( 1, 0, (0, 0, 0, 0), (0, 0, 0, 0), ("" , "", "", ""), "Motors on"),
        "motors-off": ( 2, 0, (0, 0, 0, 0), (0, 0, 0, 0), ("" , "", "", ""), "Motors off"),
        "forward":    ( 3, 1, (0, 0, 0, 0), (100000, 0, 0, 0), ("Distance (mm)", "", "", ""), "Move forward"),
        "backward":   ( 4, 1, (0, 0, 0, 0), (100000, 0, 0, 0), ("Distance (mm)", "", "", ""), "Move backward"),
        "left":       ( 5, 1, (0, 0, 0, 0), (100000, 0, 0, 0), ("Degrees", "", "", ""), "Turn left"),
        "right":      ( 6, 1, (0, 0, 0, 0), (100000, 0, 0, 0), ("Degrees", "", "", ""), "Turn right"),
        "velocity":   ( 7, 3, (1, 1, 1, 0), (100000, 100000, 100000, 0), ("Acceleration in mmPSPS", "Min mmPS", "Max mmPS", ""), "Set the velocity profile (in mm per second)"),
        "penup":      ( 8, 0, (0, 0, 0, 0), (0, 0, 0, 0), ("" , "", "", ""), "Lift the pen up"),
        "pendown":    ( 9, 0, (0, 0, 0, 0), (0, 0, 0, 0), ("" , "", "", ""), "Lower the pen down"),
        "left-eye":   (10, 3, (0, 0, 0, 0), (255, 255, 255, 0), ("Red", "Green", "Blue", ""), "Set the colour of the left eye"),
        "right-eye":  (11, 3, (0, 0, 0, 0), (255, 255, 255, 0), ("Red", "Green", "Blue", ""), "Set the colour of the right eye"),
    }

    def __init__(self, command: str = "nop", parameters: list = []):
        """
        Initialize a RobotCommand instance.
        
        Args:
            command (str): The command name.
            parameters (list): A list of parameters for the command (must be a maximum of 4 x 32-bit integers).
        
        Raises:
            ValueError: If the command is not recognized or any parameter is not a 32-bit integer.
        """
        if command not in self._command_dictionary:
            raise ValueError(f"Command '{command}' is not recognized")
        
        if len(parameters) != self._command_dictionary[command][1]:
            raise ValueError(f"Command '{command}' requires {self._command_dictionary[command][1]} parameters")
        
        self._command = command
        self._parameters = parameters

        self._command_id = self._command_dictionary[command][0]
        self._num_parameters = self._command_dictionary[command][1]
        self._parameter_minimums = self._command_dictionary[command][2]
        self._parameter_maximums = self._command_dictionary[command][3]

        # Ensure all parameters are 32-bit integers
        for param in self._parameters:
            if not (0 <= param < 2**32):
                raise ValueError(f"Parameter {param} is not a 32-bit integer")      

        # Range check the parameters according to the dictionary
        for i in range(self._num_parameters):
            if not (self._parameter_minimums[i] <= self._parameters[i] <= self._parameter_maximums[i]):
                raise ValueError(f"Parameter {self._parameters[i]} is out of range for command '{command}'")
        
        self._byte_array = self._pack_command()

    @property
    def command(self) -> str:
        """Get the command name."""
        return self._command
    
    @property
    def command_id(self) -> int:
        """Get the command ID."""
        return self._command_id
    
    @property
    def parameters(self) -> list:
        """Get the parameters for the command."""
        return self._parameters

    def _pack_command(self) -> bytes:
        """
        Pack the command ID and parameters into a fixed-length byte array.
        
        Returns:
            bytes: The packed byte array.
        """
        packed_data = struct.pack('>I4I', self._command_id, *self._parameters)
        return packed_data

    def get_packed_bytes(self) -> bytes:
        """
        Get the packed 20 byte array.
        
        Returns:
            bytes: The packed 20 byte array.
        """
        return self._byte_array
    
    @classmethod
    def _id_to_command(cls, command_id: int) -> str:
        """
        Get the command name from the command ID.
        
        Args:
            command_id (int): The command ID.
        
        Returns:
            str: The command name corresponding to the command ID.
        
        Raises:
            ValueError: If the command ID is not recognized.
        """
        for command, (id, _, _, _, _, _) in cls._command_dictionary.items():
            if id == command_id:
                return command
        raise ValueError(f"Command ID '{command_id}' is not recognized")

    @classmethod
    def from_packed_bytes(cls, byte_array: bytes):
        """
        Create a RobotCommand instance from a packed 20 byte array.
        
        Args:
            byte_array (bytes): The packed 20 byte array.
        
        Returns:
            RobotCommand: The unpacked RobotCommand instance.
        
        Raises:
            ValueError: If the byte array is not the correct length.
        """
        if len(byte_array) != 20:  # 4 bytes for command ID + 4 * 4 bytes for parameters
            raise ValueError("Byte array length is incorrect")
        
        unpacked_data = struct.unpack('>I4I', byte_array)
        command_id, param1, param2, param3, param4 = unpacked_data
        
        command = cls._id_to_command(command_id)
        num_params = cls._command_dictionary[command][1]
        if num_params == 0:
            return cls(command, [])
        elif num_params == 1:
            return cls(command, [param1])
        elif num_params == 2:
            return cls(command, [param1, param2])
        elif num_params == 3:
            return cls(command, [param1, param2, param3])
        
        return cls(command, [param1, param2, param3, param4])

    @classmethod
    def num_parameters(cls, command: str) -> int:
        """
        Get the number of parameters for the given command.
        
        Args:
            command (str): The command name.
        
        Returns:
            int: The number of parameters for the command.
        
        Raises:
            ValueError: If the command is not recognized.
        """
        if command not in cls._command_dictionary:
            raise ValueError(f"Command '{command}' is not recognized")
        return cls._command_dictionary[command][1]
    
    @classmethod
    def parameter_range(cls, command: str, param_num: int) -> tuple:
        """
        Get the range of values for the given parameter of the command.
        
        Args:
            command (str): The command name.
            param_num (int): The parameter number (0-3).
        
        Returns:
            tuple: A tuple containing the minimum and maximum values for the parameter.
        
        Raises:
            ValueError: If the command is not recognized or the parameter number is not between 1 and 4.
        """
        if command not in cls._command_dictionary:
            raise ValueError(f"Command '{command}' is not recognized")
        if not (0 <= param_num <= 3):
            raise ValueError("Parameter number must be between 0 and 3")
        return cls._command_dictionary[command][2][param_num], cls._command_dictionary[command][3][param_num]

    @classmethod
    def is_command_valid(cls, command: str) -> bool:
        """
        Check if the given command is valid.
        
        Args:
            command (str): The command name.
        
        Returns:
            bool: True if the command is valid, False otherwise.
        """
        return command in cls._command_dictionary
    
    @classmethod
    def help_text(cls) -> str:
        """
        Return a list of all available commands with their number of parameters and descriptions.
        
        Returns:
            str: A string containing the list of all available commands.
        """
        sorted_commands = sorted(cls._command_dictionary.items(), key=lambda item: item[1][0])
        help_str = ""
        for command, (_, num_params, _, _, _, help_text) in sorted_commands:
            if num_params > 0:
                param_desc = " ".join(f"[{desc}]" for desc in cls._command_dictionary[command][4][:num_params])
                help_str += f"    {command} {param_desc} - {help_text}\r\n"
            else:
                help_str += f"    {command} - {help_text}\r\n"
        return help_str
    
    def __str__(self):
        """
        Return a string representation of the RobotCommand instance.
        
        Returns:
            str: A string representation of the RobotCommand instance.
        """
        if self._num_parameters == 0:
            return f"Command = \"{self._command}\" with no parameters"
        return f"Command = \"{self._command}\" with parameters = {self._parameters}"
