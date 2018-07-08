#include <Streaming.h>

const int switch_pin = 15;

volatile unsigned long last_change_time = 0;
volatile bool switch_changed = false;

void handle_interrupt() {
  const auto now = millis();

  if (now - last_change_time > 100) {
    switch_changed = true;
    last_change_time = now;
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(switch_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switch_pin), handle_interrupt, CHANGE);
}

void loop() {
  if (switch_changed) {
    switch_changed = false;

    const auto state = digitalRead(switch_pin);
    Serial << "Switch state is now " << state << '\n';
  }

  delay(10);
}
