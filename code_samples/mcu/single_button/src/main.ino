#include <Streaming.h>

const int button_pin = 15;

volatile unsigned long last_change_time = 0;
volatile bool button_pushed = false;

unsigned int times_pressed = 0;

void handle_interrupt() {
  const auto now = millis();

  if (now - last_change_time > 500) {
    button_pushed = true;
    last_change_time = now;
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(button_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(button_pin), handle_interrupt, FALLING);
}

void loop() {
  if (button_pushed) {
    button_pushed = false;

    Serial << "Button was pushed " << ++times_pressed << " time(s)\n";
  }

  delay(10);
}
