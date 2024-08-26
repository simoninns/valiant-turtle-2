/************************************************************************ 

    leds.c

    Valiant Turtle 2 - Raspberry Pi Pico W Firmware
    Copyright (C) 2023 Simon Inns

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

#include <stdio.h>
#include <pico/stdlib.h>
#include "pico/cyw43_arch.h"
#include "hardware/pwm.h"
#include "hardware/clocks.h"

#include "leds.h"

// Initialise all LED GPIO functions
void ledInitialise(void)
{
    // Set default LED states
    ledSystem(false);

    // Initialise the RGB LEDs
    ledRedInitialise();
    ledGreenInitialise();
    ledBlueInitialise();

    // Set all LEDs to off
    ledRedSet(0);
    ledGreenSet(0);
    ledBlueSet(0);
}

void ledRedInitialise(void)
{
    gpio_set_function(LED_R_GPIO, GPIO_FUNC_PWM);
    uint slice_num = pwm_gpio_to_slice_num(LED_R_GPIO);

    pwm_config config = pwm_get_default_config();
    pwm_config_set_clkdiv(&config, 4.f);
    pwm_init(slice_num, &config, true);
}

void ledGreenInitialise(void)
{
    gpio_set_function(LED_G_GPIO, GPIO_FUNC_PWM);
    uint slice_num = pwm_gpio_to_slice_num(LED_G_GPIO);

    pwm_config config = pwm_get_default_config();
    pwm_config_set_clkdiv(&config, 4.f);
    pwm_init(slice_num, &config, true);
}

void ledBlueInitialise(void)
{
    gpio_set_function(LED_B_GPIO, GPIO_FUNC_PWM);
    uint slice_num = pwm_gpio_to_slice_num(LED_B_GPIO);

    pwm_config config = pwm_get_default_config();
    pwm_config_set_clkdiv(&config, 4.f);
    pwm_init(slice_num, &config, true);
}

// Control the onboard system LED
void ledSystem(bool ledState)
{
    if (ledState) cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    else cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
}

void ledRedSet(int16_t brightness)
{
    if (brightness < 0) brightness = 0;
    if (brightness > 255) brightness = 255;

    pwm_set_gpio_level(LED_R_GPIO, brightness * brightness);
}

void ledGreenSet(int16_t brightness)
{
    if (brightness < 0) brightness = 0;
    if (brightness > 255) brightness = 255;

    pwm_set_gpio_level(LED_G_GPIO, brightness * brightness);
}

void ledBlueSet(int16_t brightness)
{
    if (brightness < 0) brightness = 0;
    if (brightness > 255) brightness = 255;

    pwm_set_gpio_level(LED_B_GPIO, brightness * brightness);
}