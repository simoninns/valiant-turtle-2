#************************************************************************ 
#
#   main.py
#
#   Main module for the Valiant Turtle 2 Communicator firmware
#   Valiant Turtle 2 - Communicator firmware
#   Copyright (C) 2025 Simon Inns
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

import picolog
from micropython import const
from options import Options
from machine import Pin, UART
from leds import Leds
from commands_tx import CommandsTx
from ble_central import BleCentral
from serial_comms import SerialComms
import asyncio

# GPIO Hardware mapping
_GPIO_GREEN_LED = const(16)
_GPIO_BLUE_LED = const(18)
_GPIO_IR_LED = const(22)

_GPIO_SDA0 = const(8)
_GPIO_SCL0 = const(9)
_GPIO_SDA1 = const(10)
_GPIO_SCL1 = const(11)

_GPIO_INT0 = const(12)

_GPIO_UART0_TX = const(0)
_GPIO_UART0_RX = const(1)
_GPIO_UART1_TX = const(4)
_GPIO_UART1_RX = const(5)
_GPIO_UART1_RTS = const(7)
_GPIO_UART1_CTS = const(6)

_GPIO_BUTTON0 = const(21)
_GPIO_BUTTON1 = const(20)
_GPIO_BUTTON2 = const(19)

_GPIO_OPTION0 = const(26)
_GPIO_OPTION1 = const(27)
_GPIO_OPTION2 = const(28)

async def led_control_task(leds: Leds, ble_central: BleCentral):
    loop = 0
    green_led = 0
    blue_led = 1

    leds.set_fade_speed(green_led, 10)
    leds.set_fade_speed(blue_led, 2)

    leds.set_brightness(green_led, 255)

    while True:
        # Show BLE connection status
        if ble_central.connected:
            if loop < 3:
                leds.set_brightness(blue_led, 32)
            else:
                leds.set_brightness(blue_led, 100)
        else:
            leds.set_brightness(blue_led, 0)

        loop += 1
        if loop > 4: loop = 0
        await asyncio.sleep(0.25)

async def aio_main(ble_central: BleCentral, serial_comms: SerialComms, leds: Leds):
    picolog.info("aio_main - Running main async tasks") 

    tasks = [
        asyncio.create_task(ble_central.run()),
        asyncio.create_task(serial_comms.run()),
        asyncio.create_task(leds.run()),
        asyncio.create_task(led_control_task(leds, ble_central)),
    ]
    await asyncio.gather(*tasks)

def main():
    # Configure the options object
    options = Options(_GPIO_OPTION0, _GPIO_OPTION1, _GPIO_OPTION2)

    # If the option 2 header is closed, output debug information to UART0
    # otherwise output to the REPL
    if options.option2:
        uart0 = UART(0, baudrate=115200, tx=Pin(_GPIO_UART0_TX), rx=Pin(_GPIO_UART0_RX),
            txbuf=1024, rxbuf=1024, bits=8, parity=None, stop=1)
    else:
        uart0 = None

    # Configure the picolog module
    picolog.basicConfig(level=picolog.DEBUG, uart=uart0)

    # Show the options now debug is running
    options.show_options()

    # Ensure IR LED driver is off
    ir_led = Pin(_GPIO_IR_LED, Pin.OUT)
    ir_led.value(0)

    # Initialise LEDs
    leds = Leds([_GPIO_GREEN_LED, _GPIO_BLUE_LED])

    # Configure the UART1 for serial <-> host communication
    uart1 = UART(1, baudrate=4800, tx=Pin(_GPIO_UART1_TX), rx=Pin(_GPIO_UART1_RX),
        cts=Pin(_GPIO_UART1_CTS), rts=Pin(_GPIO_UART1_RTS), flow=(UART.RTS | UART.CTS),
        txbuf=1024, rxbuf=1024, bits=8, parity=None, stop=1)
    
    # Create the required objects before going asynchronous
    ble_central = BleCentral()
    commands_tx = CommandsTx(ble_central)
    serial_comms = SerialComms(uart1, commands_tx)
    
    while True:
        asyncio.run(aio_main(ble_central, serial_comms, leds))
    
if __name__ == "__main__":
    main()