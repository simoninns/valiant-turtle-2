#************************************************************************ 
#
#   vt2_battest.py
#
#   Automatic battery testing
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
import time
import csv
from commands_tx import CommandsTx
import sys

def battery_discharge_test(commands_tx: CommandsTx):
    """
    Runs a battery discharge test on the robot. The robot will move forward and backward in 50cm increments
    until the battery is exhausted. The test will record the battery voltage, current and power every 100cm in
    a CSV file."""
    distance = 0

    # Open CSV file to store the output
    csv_file = open('vt2_batttest.csv', mode='w', newline='')
    csv_writer = csv.writer(csv_file)

    # Motors on
    commands_tx.motors(True)

    while True:
        _, mv, ma, mw = commands_tx.get_power()
        current_time_str = time.strftime("%H%M%S", time.localtime()) + f"{int(time.time() * 1000) % 1000:03d}"
        print(f"{current_time_str}, {mv}, {ma}, {mw}, {distance}")
        csv_writer.writerow([current_time_str, mv, ma, mw, distance])
        csv_file.flush()

        commands_tx.forward(500)
        distance += 5
        commands_tx.backward(500)
        distance += 5

def main():
    # Configure the logging module
    log_format = "[%(asctime)s %(filename)s::%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, filename="vt2_batttest.log")

    commands_tx = CommandsTx()

    # Wait for BLE connection
    commands_tx.connect()
    logging.info("Waiting for BLE connection...")
    while not commands_tx.connected:
        time.sleep(1)
    logging.info("Connected to BLE")

    battery_discharge_test(commands_tx)
    logging.info("Command tests completed. Exiting program.")
    commands_tx.disconnect()
    logging.info("Disconnected from BLE")

    sys.exit(0)

if __name__ == "__main__":
    main()