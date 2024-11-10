#************************************************************************ 
#
#   ble_central.py
#
#   BLE Central role
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

from log import log_debug, log_info, log_warn

from machine import Pin, unique_id
from micropython import const

from status_led import Status_led

import sys
import aioble
import bluetooth
import asyncio

_GPIO_BUTTON2 = const(19)

# Get this device's UID - Used as BLE serial number to ensure it's unique
def uid():
    return "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
        *unique_id())

# Button on GPIO19 only...
button_a = Pin(_GPIO_BUTTON2, Pin.IN, Pin.PULL_UP)

_ENV_SENSE_UUID = bluetooth.UUID(0x180A)
_GENERIC = bluetooth.UUID(0x1848)
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x1800)
_BUTTON_UUID = bluetooth.UUID(0x2A6E)

_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)

# BLE Advertising frequency
_ADV_INTERVAL_US = const(250000)

# Device service definitions
device_info = aioble.Service(_ENV_SENSE_UUID)

# Global connection flag
connection = None

# Create characteristics for device info
MANUFACTURER_ID = const(0x02A29)
MODEL_NUMBER_ID = const(0x2A24)
SERIAL_NUMBER_ID = const(0x2A25)
HARDWARE_REVISION_ID = const(0x2A26)
BLE_VERSION_ID = const(0x2A28)
aioble.Characteristic(device_info, bluetooth.UUID(MANUFACTURER_ID), read=True, initial="waitingforfriday.com")
aioble.Characteristic(device_info, bluetooth.UUID(MODEL_NUMBER_ID), read=True, initial="1.0")
aioble.Characteristic(device_info, bluetooth.UUID(SERIAL_NUMBER_ID), read=True, initial=uid())
aioble.Characteristic(device_info, bluetooth.UUID(HARDWARE_REVISION_ID), read=True, initial=sys.version)
aioble.Characteristic(device_info, bluetooth.UUID(BLE_VERSION_ID), read=True, initial="1.0")

remote_service = aioble.Service(_GENERIC)

button_characteristic = aioble.Characteristic(
    remote_service, _BUTTON_UUID, read=True, notify=True
)

aioble.register_services(remote_service, device_info)

# Global connected flag
connected = False

# Process commands task
async def process_commands_task():
    while True:
        if not connected:
            # Not connected - wait a second and try again
            await asyncio.sleep_ms(1000)
            continue

        if button_a.value() == 0:
            print(f'Button A pressed')
            #only need to write OR notify, not both!
            # button_characteristic.write(b"a")    
            button_characteristic.notify(connection,b"a")
        # elif button_b.read():
        #     print('Button B pressed')
        #     # button_characteristic.write(b"b")
        #     button_characteristic.notify(connection,b"b")
        # elif button_x.read():
        #     print('Button X pressed')
        #     # button_characteristic.write(b"x")
        #     button_characteristic.notify(connection,b"x")
        # elif button_y.read():
        #     print('Button Y pressed')
        #     # button_characteristic.write(b"y")
        #     button_characteristic.notify(connection,b"x")
        # else:
        #     button_characteristic.notify(connection,b"!")

        await asyncio.sleep_ms(10)
            
# Serially wait for connections. Don't advertise while a central is connected.    
async def ble_peripheral_task():
    log_debug("ble_central::peripheral_task - Task started")
    global connected, connection

    while True:
        # Wait for something to connect
        log_debug("ble_central::peripheral_task - Waiting for connection...")
        connection = await aioble.advertise(
                _ADV_INTERVAL_US,
                name="vt2-robot",
                services=[_ENV_SENSE_TEMP_UUID],
                appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL,
                manufacturer=(0xabcd, b"1234"),
            )
        log_info("ble_central::peripheral_task - BLE connection from", connection.device)
        connected = True

        # Wait for the connected device to disconnect
        await connection.disconnected()
        connected = False
        connection = None
        log_info("ble_central::peripheral_task - BLE disconnected")
        
# Task to blink the blue status LED
# 1 second blink = connected
# 1/4 second blink = not connected
async def connection_status_task(status_led: Status_led):
    log_debug("ble_central::connection_status_task - Task started")
    llevel = 255
    while True:
        status_led.set_brightness(llevel)
        if llevel == 255: llevel = 10
        else: llevel = 255

        blink = 1000
        if not connected: blink = 250

        await asyncio.sleep_ms(blink)