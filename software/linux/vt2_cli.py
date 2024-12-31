#************************************************************************ 
#
#   vt2_cli.py
#
#   Automatic command testing
#   Valiant Turtle 2 - Communicator Linux Firmware
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

import logging
from commands_tx import CommandsTx
import sys
import time
import cmd

class ValiantTurtleCLI(cmd.Cmd):
    intro = 'Welcome to the Valiant Turtle 2 CLI. Type help or ? to list commands.\n'
    prompt = 'VT2> '

    def __init__(self, commands_tx: CommandsTx):
        super().__init__()
        self._commands_tx = commands_tx
        self._connected = False

    def emptyline(self):
        pass

    def do_connect(self, arg):
        'Connect to the BLE device: connect'
        if not self._connected:
            self._commands_tx.connect()
            logging.info("Waiting for BLE connection...")
            while not self._commands_tx.connected:
                time.sleep(1)
            self._connected = True
            print("Connected to BLE peripheral.")
            logging.info("Connected to BLE")
        else:
            print("Cannot connect as BLE is already connected.")

    def do_disconnect(self, arg):
        'Disconnect from the BLE device: disconnect'
        if self._connected:
            self._commands_tx.disconnect()
            self._connected = False
            print("Disconnected from BLE peripheral.")
            logging.info("Disconnected from BLE")
        else:
            print("Cannot disconnect as BLE is not connected.")

    def do_exit(self, arg):
        'Exit the CLI: exit'
        logging.info("Exiting CLI")
        if self._connected:
            self._commands_tx.disconnect()
            self._connected = False
        print("Goodbye!")
        sys.exit(0)

    def do_motors(self, arg):
        'Turn the motors on or off: motors [on|off]'
        if self._connected:
            if arg == "on":
                self._commands_tx.motors(True)
            elif arg == "off":
                self._commands_tx.motors(False)
            else:
                print("Invalid argument. Please enter 'on' or 'off'.")
            logging.info("CLI: Motors")
        else:
            print("Not connected to BLE device.")

    def do_forward(self, arg):
        'Move the robot forward: forward [mm]'
        if self._connected:
            try:
                distance = int(arg)
                if distance > 0:
                    success, x, y, heading = self._commands_tx.forward(distance)
                    if success:
                        print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                    else:
                        print("Failed to move forward.")
                else:
                    print("Invalid distance. Please enter a positive integer value.")
            except ValueError:
                print("Invalid distance. Please enter an integer value.")
            logging.info("CLI: Forward")
        else:
            print("Not connected to BLE device.")

    def do_backward(self, arg):
        'Move the robot backward: backward [mm]'
        if self._connected:
            try:
                distance = int(arg)
                if distance > 0:
                    success, x, y, heading = self._commands_tx.backward(distance)
                    if success:
                        print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                    else:
                        print("Failed to move backward.")
                else:
                    print("Invalid distance. Please enter a positive integer value.")
            except ValueError:
                print("Invalid distance. Please enter an integer value.")
            logging.info("CLI: Backward")
        else:
            print("Not connected to BLE device.")

    def do_left(self, arg):
        'Turn the robot left: left [degrees]'
        if self._connected:
            try:
                degrees = int(arg)
                if degrees > 0:
                    success, x, y, heading = self._commands_tx.left(degrees)
                    if success:
                        print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                    else:
                        print("Failed to turn left.")
                else:
                    print("Invalid degrees. Please enter a positive integer value.")
            except ValueError:
                print("Invalid degrees. Please enter an integer value.")
            logging.info("CLI: Left")
        else:
            print("Not connected to BLE device.")

    def do_right(self, arg):
        'Turn the robot right: right [degrees]'
        if self._connected:
            try:
                degrees = int(arg)
                if degrees > 0:
                    success, x, y, heading = self._commands_tx.right(degrees)
                    if success:
                        print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                    else:
                        print("Failed to turn right.")
                else:
                    print("Invalid degrees. Please enter a positive integer value.")
            except ValueError:
                print("Invalid degrees. Please enter an integer value.")
            logging.info("CLI: Right")
        else:
            print("Not connected to BLE device.")

    def do_circle(self, arg):
        'Move the robot in a circle: circle [radius] [extent in degrees]'
        if self._connected:
            try:
                radius, extent_degrees = map(int, arg.split())
                success, x, y, heading = self._commands_tx.circle(radius, extent_degrees)
                if success:
                    print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                else:
                    print("Failed to move in a circle.")
            except ValueError:
                print("Invalid radius or extent degrees. Please enter two integer values.")
                logging.info("CLI: Circle")
        else:
            print("Not connected to BLE device.")

    def do_heading(self, arg):
        'Set the heading of the robot: heading [degrees]'
        if self._connected:
            try:
                angle_degrees = float(arg)
                if 0 <= angle_degrees < 360:
                    self._commands_tx.heading(angle_degrees)
                else:
                    print("Invalid angle. Angle should be 0 and above, and less than 360.")
            except ValueError:
                print("Invalid angle. Please enter a float value.")
            logging.info("CLI: Heading")
        else:
            print("Not connected to BLE device.")

    def do_position_x(self, arg):
        'Set the X position of the robot: position_x [mm]'
        if self._connected:
            try:
                x_mm = float(arg)
                success, x, y, heading = self._commands_tx.position_x(x_mm)
                if success:
                    print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                else:
                    print("Failed to set X position.")
            except ValueError:
                print("Invalid position. Please enter a float value.")
            logging.info("CLI: Position X")
        else:
            print("Not connected to BLE device.")

    def do_position_y(self, arg):
        'Set the Y position of the robot: position_y [mm]'
        if self._connected:
            try:
                y_mm = float(arg)
                success, x, y, heading = self._commands_tx.position_y(y_mm)
                if success:
                    print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                else:
                    print("Failed to set Y position.")
            except ValueError:
                print("Invalid position. Please enter a float value.")
            logging.info("CLI: Position Y")
        else:
            print("Not connected to BLE device.")

    def do_position(self, arg):
        'Set the X and Y position of the robot: position [x_mm] [y_mm]'
        if self._connected:
            try:
                x_mm, y_mm = map(float, arg.split())
                success, x, y, heading = self._commands_tx.position(x_mm, y_mm)
                if success:
                    print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                else:
                    print("Failed to set position.")
            except ValueError:
                print("Invalid positions. Please enter two float values.")
            logging.info("CLI: Position")
        else:
            print("Not connected to BLE device.")

    def do_towards(self, arg):
        'Move the robot towards a position: towards [x_mm] [y_mm]'
        if self._connected:
            try:
                x_mm, y_mm = map(float, arg.split())
                success, x, y, heading = self._commands_tx.towards(x_mm, y_mm)
                if success:
                    print(f"X={x} mm, Y={y} mm, Heading={heading} degrees")
                else:
                    print("Failed to move towards position.")
            except ValueError:
                print("Invalid positions. Please enter two float values.")
            logging.info("CLI: Towards")
        else:
            print("Not connected to BLE device.")

    def do_reset_origin(self, arg):
        'Reset the origin and heading of the robot: reset_origin'
        if self._connected:
            self._commands_tx.reset_origin()
            logging.info("CLI: Reset Origin")
        else:
            print("Not connected to BLE device.")

    def do_get_heading(self, arg):
        'Get the current heading of the robot: get_heading'
        if self._connected:
            success, heading = self._commands_tx.get_heading()
            if success:
                print(f"Current heading: {heading} degrees")
            else:
                print("Failed to get heading.")
            logging.info("CLI: Get Heading")
        else:
            print("Not connected to BLE device.")

    def do_get_position(self, arg):
        'Get the current position of the robot: get_position'
        if self._connected:
            success, x, y = self._commands_tx.get_position()
            if success:
                print(f"Current position: X={x} mm, Y={y} mm")
            else:
                print("Failed to get position.")
            logging.info("CLI: Get Position")
        else:
            print("Not connected to BLE device.")

    def do_pen(self, arg):
        'Control the pen: pen [up|down]'
        if self._connected:
            if arg == "up":
                self._commands_tx.pen(True)
            elif arg == "down":
                self._commands_tx.pen(False)
            else:
                print("Invalid argument. Please enter 'up' or 'down'.")
            logging.info("CLI: Pen")
        else:
            print("Not connected to BLE device.")

    def do_eyes(self, arg):
        'Set the color of the eyes: eyes [eye_id] [red] [green] [blue]'
        if self._connected:
            try:
                eye_id, red, green, blue = map(int, arg.split())
                if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
                    print("Invalid color values. Please enter values between 0 and 255 for red, green, and blue.")
                    return
                self._commands_tx.eyes(eye_id, red, green, blue)
            except ValueError:
                print("Invalid arguments. Please enter four integer values.")
            logging.info("CLI: Eyes")
        else:
            print("Not connected to BLE device.")

    def do_get_power(self, arg):
        'Get the power status: get_power'
        if self._connected:
            success, mv, ma, mw = self._commands_tx.get_power()
            if success:
                print(f"Power status: {mv}mV, {ma}mA, {mw}mW")
            else:
                print("Failed to get power status.")
            logging.info("CLI: Get Power")
        else:
            print("Not connected to BLE device.")

    def do_get_pen(self, arg):
        'Get the pen status: get_pen'
        if self._connected:
            success, pen_up = self._commands_tx.get_pen()
            if success:
                print(f"Pen status: {'Up' if pen_up else 'Down'}")
            else:
                print("Failed to get pen status.")
            logging.info("CLI: Get Pen")
        else:
            print("Not connected to BLE device.")

    def do_set_linear_velocity(self, arg):
        'Set the linear velocity: set_linear_velocity [target_speed] [acceleration]'
        if self._connected:
            try:
                target_speed, acceleration = map(int, arg.split())
                self._commands_tx.set_linear_velocity(target_speed, acceleration)
            except ValueError:
                print("Invalid arguments. Please enter two integer values.")
            logging.info("CLI: Set Linear Velocity")
        else:
            print("Not connected to BLE device.")

    def do_set_rotational_velocity(self, arg):
        'Set the rotational velocity: set_rotational_velocity [target_speed] [acceleration]'
        if self._connected:
            try:
                target_speed, acceleration = map(int, arg.split())
                self._commands_tx.set_rotational_velocity(target_speed, acceleration)
            except ValueError:
                print("Invalid arguments. Please enter two integer values.")
            logging.info("CLI: Set Rotational Velocity")
        else:
            print("Not connected to BLE device.")

    def do_get_linear_velocity(self, arg):
        'Get the linear velocity: get_linear_velocity'
        if self._connected:
            success, speed, acceleration = self._commands_tx.get_linear_velocity()
            if success:
                print(f"Linear velocity: Speed={speed}, Acceleration={acceleration}")
            else:
                print("Failed to get linear velocity.")
            logging.info("CLI: Get Linear Velocity")
        else:
            print("Not connected to BLE device.")

    def do_get_rotational_velocity(self, arg):
        'Get the rotational velocity: get_rotational_velocity'
        if self._connected:
            success, speed, acceleration = self._commands_tx.get_rotational_velocity()
            if success:
                print(f"Rotational velocity: Speed={speed}, Acceleration={acceleration}")
            else:
                print("Failed to get rotational velocity.")
            logging.info("CLI: Get Rotational Velocity")
        else:
            print("Not connected to BLE device.")

    def do_set_wheel_diameter_calibration(self, arg):
        'Set the wheel diameter calibration: set_wheel_diameter_calibration [micrometers]'
        if self._connected:
            try:
                wheel_diameter = int(arg)
                self._commands_tx.set_wheel_diameter_calibration(wheel_diameter)
            except ValueError:
                print("Invalid diameter. Please enter an integer value.")
            logging.info("CLI: Set Wheel Diameter Calibration")
        else:
            print("Not connected to BLE device.")

    def do_set_axel_distance_calibration(self, arg):
        'Set the axel distance calibration: set_axel_distance_calibration [micrometers]'
        if self._connected:
            try:
                axel_distance = int(arg)
                self._commands_tx.set_axel_distance_calibration(axel_distance)
            except ValueError:
                print("Invalid distance. Please enter an integer value.")
            logging.info("CLI: Set Axel Distance Calibration")
        else:
            print("Not connected to BLE device.")

    def do_get_wheel_diameter_calibration(self, arg):
        'Get the wheel diameter calibration: get_wheel_diameter_calibration'
        if self._connected:
            success, diameter = self._commands_tx.get_wheel_diameter_calibration()
            if success:
                print(f"Wheel diameter calibration: {diameter} um")
            else:
                print("Failed to get wheel diameter calibration.")
            logging.info("CLI: Get Wheel Diameter Calibration")
        else:
            print("Not connected to BLE device.")

    def do_get_axel_distance_calibration(self, arg):
        'Get the axel distance calibration: get_axel_distance_calibration'
        if self._connected:
            success, distance = self._commands_tx.get_axel_distance_calibration()
            if success:
                print(f"Axel distance calibration: {distance} um")
            else:
                print("Failed to get axel distance calibration.")
            logging.info("CLI: Get Axel Distance Calibration")
        else:
            print("Not connected to BLE device.")

    def do_set_turtle_id(self, arg):
        'Set the turtle ID: set_turtle_id [id]'
        if self._connected:
            try:
                turtle_id = int(arg)
                if 0 <= turtle_id <= 7:
                    self._commands_tx.set_turtle_id(turtle_id)
                else:
                    print("Invalid ID. Please enter a value between 0 and 7.")
            except ValueError:
                print("Invalid ID. Please enter an integer value.")
            logging.info("CLI: Set Turtle ID")
        else:
            print("Not connected to BLE device.")

    def do_get_turtle_id(self, arg):
        'Get the turtle ID: get_turtle_id'
        if self._connected:
            success, turtle_id = self._commands_tx.get_turtle_id()
            if success:
                print(f"Turtle ID: {turtle_id}")
            else:
                print("Failed to get turtle ID.")
            logging.info("CLI: Get Turtle ID")
        else:
            print("Not connected to BLE device.")

    def do_load_config(self, arg):
        'Load the configuration: load_config'
        if self._connected:
            self._commands_tx.load_config()
            logging.info("CLI: Load Config")
        else:
            print("Not connected to BLE device.")

    def do_save_config(self, arg):
        'Save the configuration: save_config'
        if self._connected:
            self._commands_tx.save_config()
            logging.info("CLI: Save Config")
        else:
            print("Not connected to BLE device.")

    def do_reset_config(self, arg):
        'Reset the configuration: reset_config'
        if self._connected:
            self._commands_tx.reset_config()
            logging.info("CLI: Reset Config")
        else:
            print("Not connected to BLE device.")

def main():
    # Configure the logging module
    log_format = "[%(asctime)s %(filename)s::%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, filename="vt2_cli.log")

    commands_tx = CommandsTx()

    # # Wait for BLE connection
    # commands_tx.connect()
    # logging.info("Waiting for BLE connection...")
    # while not commands_tx.connected:
    #     time.sleep(1)
    # logging.info("Connected to BLE")

    ValiantTurtleCLI(commands_tx).cmdloop()

    sys.exit(0)

if __name__ == "__main__":
    main()