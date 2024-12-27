#************************************************************************ 
#
#   main.py
#
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
import asyncio
from ble_central import BleCentral
from commands_tx import CommandsTx

async def demo(ble_central: BleCentral, commands_tx: CommandsTx):
    while True:
        if ble_central.is_connected:
            logging.info("Motors on")
            result = await commands_tx.motors(True)
            if result:
                for i in range(4):
                    logging.info("Forward 500mm")
                    await commands_tx.forward(500)
                    logging.info("Turn right 90 degrees")
                    await commands_tx.right(90)

                logging.info("Motors off")
                await commands_tx.motors(False)

                logging.info("Pausing for 5 seconds before repeating")
                await asyncio.sleep(5)
        else:
            await asyncio.sleep(1)

async def aio_main():
    logging.info("Running BLE central async tasks") 
    ble_central = BleCentral()
    commands_tx = CommandsTx(ble_central)

    tasks = [
        asyncio.create_task(ble_central.run()),
        asyncio.create_task(demo(ble_central, commands_tx)),
    ]
    await asyncio.gather(*tasks)

def main():
    # Configure the logging module
    log_format = "[%(asctime)s %(filename)s::%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, filename="vt2demo.log")

    asyncio.run(aio_main())

if __name__ == "__main__":
    main()