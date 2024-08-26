/*
* RP2040-Button
* Button debounce library for Raspberry Pi Pico
*
* Fork of https://github.com/jkroso/pico-button.c
* including https://github.com/jkroso/pico-gpio-interrupt.c,
* both by Jake Rosoman. MIT license.
*
* 2023-02-13: Adapted by Turi Scandurra
*/

#ifndef PICO_BUTTON_H
#define PICO_BUTTON_H

#include "pico/stdlib.h"

#ifdef __cplusplus
extern "C" {
#endif

#define DEBOUNCE_US 200

typedef struct button_t {
  uint8_t pin;
  bool state;
  void (*onchange)(struct button_t *button);
} button_t;

typedef void (*handler)(void *argument);

typedef struct {
  void * argument;
  handler fn;
} closure_t;

long long int handle_button_alarm(long int a, void *p);

void handle_button_interrupt(void *p);

void handle_interrupt(uint gpio, uint32_t events);

void listen(uint pin, int condition, handler fn, void *arg);

button_t * create_button(int pin, void (*onchange)(button_t *));

#ifdef __cplusplus
}
#endif

#endif