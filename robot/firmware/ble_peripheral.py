#************************************************************************ 
#
#   ble_peripheral.py
#
#   BLE Peripheral Role
#   Valiant Turtle 2 - Robot firmware
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

import aioble
import bluetooth
import machine
import asyncio

# Bluetooth UUIDS can be found online at https://www.bluetooth.com/specifications/gatt/services/

_REMOTE_UUID = bluetooth.UUID(0x1848)
_ENV_SENSE_UUID = bluetooth.UUID(0x1800) 
_REMOTE_CHARACTERISTICS_UUID = bluetooth.UUID(0x2A6E)

connected = False
alive = False

async def find_vt2_communicator():
    # Scan for 5 seconds, in active mode, with very low interval/window (to
    # maximise detection rate).
    log_debug("ble_peripheral::find_vt2_communicator - Scanning for VT2 communicator device...")
    async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            # See if it matches our name
            if result.name() == "vt2-robot":
                log_debug("ble_peripheral::find_vt2_communicator - Found VT2 communicator device")
                for item in result.services():
                    log_debug("ble_peripheral::find_vt2_communicator - got service:", item)
                if _ENV_SENSE_UUID in result.services():
                    log_debug("ble_peripheral::find_vt2_communicator - Got service from VT2 communicator")
                    return result.device

    return None

# async def blink_task():
#     """ Blink the LED on and off every second """
    
#     print('blink task started')
#     toggle = True
    
#     while True and alive:
#         blink = 250
#         #led.value(toggle)
#         toggle = not toggle
#         # print(f'blink {toggle}, connected: {connected}')
#         if connected:
#             blink = 1000
#         else:
#             blink = 250
#         await asyncio.sleep_ms(blink)
#     print('blink task stopped')

def move_robot(command):
    if command == b'a':
        print("a button pressed")
    elif command == b'b':
        print("b button pressed")
    elif command == b'x':
        print("x button pressed")
    elif command == b'y':
        print("y button pressed")

async def connect_to_communicator():
    global connected, alive
    connected = False
    device = await find_vt2_communicator()
    if not device:
        log_debug("ble_peripheral::ble_peripheral_task - VT2 Communicator not found")
        return
    try:
        log_debug("ble_peripheral::ble_peripheral_task - VT2 Communicator with ID", device, "found.  Attempting to connect")
        connection = await device.connect()
        
    except asyncio.TimeoutError:
        log_debug("ble_peripheral::ble_peripheral_task - Connection attempt timed out!")
        return
      
    async with connection:
        log_debug("ble_peripheral::ble_peripheral_task - Connected to VT2 communicator")
        alive = True
        connected = True

        robot_service = await connection.service(_REMOTE_UUID)
        control_characteristic = await robot_service.characteristic(_REMOTE_CHARACTERISTICS_UUID)
        
        while True:
            try:
                if robot_service == None:
                    log_debug("ble_peripheral::ble_peripheral_task - VT2 Communicator disconnected")
                    alive = False
                    break
                
            except asyncio.TimeoutError:
                log_debug("ble_peripheral::ble_peripheral_task - Timeout discovering services/characteristics")
                alive = False
                break
            
            if control_characteristic == None:
                log_debug("ble_peripheral::ble_peripheral_task - no control characteristics found")
                alive = False
                break
           
            try:
                data = await control_characteristic.read(timeout_ms=1000)

                await control_characteristic.subscribe(notify=True)
                while True:
                    command = await control_characteristic.notified()
                    move_robot(command)
                                                            
            except Exception as e:
                log_debug("ble_peripheral::ble_peripheral_task - Exception was flagged, device gone?")
                connected = False
                alive = False
                break
        await connection.disconnected()
        log_debug("ble_peripheral::ble_peripheral_task - VT2 Communicator disconnected")
        alive = False

async def ble_peripheral_task():
    log_debug("ble_peripheral::ble_peripheral_task - Task started")
    while True:
        await connect_to_communicator()