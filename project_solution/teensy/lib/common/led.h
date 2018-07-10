#include <inttypes.h>

#pragma once

extern const int led_pin;

void led_init();
void led_set(uint8_t r, uint8_t g, uint8_t b);
