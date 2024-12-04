# Stepper motor control test program
import library.logging as logging
from machine import Pin
import time

from drv8825 import Drv8825
from stepper import Stepper
from pulse_generator import PulseGenerator

_GPIO_LM_STEP = const(2)
_GPIO_RM_STEP = const(3)
_GPIO_LM_DIR = const(4)
_GPIO_RM_DIR = const(5)
_GPIO_ENABLE = const(6)
_GPIO_M0 = const(12)
_GPIO_M1 = const(13)
_GPIO_M2 = const(14)

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Main test function
    left_step_pin = Pin(_GPIO_LM_STEP, Pin.OUT)
    left_direction_pin = Pin(_GPIO_LM_DIR, Pin.OUT)
    right_step_pin = Pin(_GPIO_RM_STEP, Pin.OUT)
    right_direction_pin = Pin(_GPIO_RM_DIR, Pin.OUT)

    drv8825_enable_pin = Pin(_GPIO_ENABLE, Pin.OUT)
    drv8825_m0_pin = Pin(_GPIO_M0, Pin.OUT)
    drv8825_m1_pin = Pin(_GPIO_M1, Pin.OUT)
    drv8825_m2_pin = Pin(_GPIO_M2, Pin.OUT)

    # The DRV8825 driver is shared between the two stepper motors
    drv8825 = Drv8825(drv8825_enable_pin, drv8825_m0_pin, drv8825_m1_pin, drv8825_m2_pin)
    drv8825.set_steps_per_revolution(800)
    drv8825.set_enable(False)

    # Create the left and right stepper motor instances
    left_stepper = Stepper(drv8825, left_step_pin, left_direction_pin, True)
    #right_stepper = Stepper(drv8825, right_step_pin, right_direction_pin, False)

    while True:
        # Set forwards
        left_stepper.set_direction_forwards()
        logging.debug("Main - Forwards")
        drv8825.set_enable(True)

        logging.debug("Main - Running")
        left_stepper.set_acceleration_spsps(16)
        left_stepper.set_target_speed_sps(800)
        left_stepper.move(800 * 4)

        while left_stepper.is_busy:
            time.sleep_ms(100)

        logging.debug("Main - Waiting...")
        drv8825.set_enable(False)
        time.sleep_ms(5000)

main()