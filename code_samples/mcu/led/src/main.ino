#include <Adafruit_NeoPixel.h>

const int led_pin = 14;

Adafruit_NeoPixel leds = Adafruit_NeoPixel(1, led_pin, NEO_GRB + NEO_KHZ800);

void set_led(int r, int g, int b) {
  leds.setPixelColor(0, leds.Color(r, g, b));
  leds.show();
}

void setup() {
  leds.begin();

  leds.setBrightness(16);
}

void loop() {
  set_led(255, 0, 0);
  delay(500);

  set_led(0, 255, 0);
  delay(500);

  set_led(0, 0, 255);
  delay(500);

  set_led(255, 255, 255);
  delay(500);
}
