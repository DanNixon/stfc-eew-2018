#include "led.h"

#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel leds = Adafruit_NeoPixel(1, led_pin, NEO_GRB + NEO_KHZ800);

void led_init() {
  leds.begin();
  leds.setBrightness(16);
  delay(5);
  led_set(0, 0, 0);
}

void led_set(uint8_t r, uint8_t g, uint8_t b) {
  leds.setPixelColor(0, leds.Color(r, g, b));
  leds.show();
}
