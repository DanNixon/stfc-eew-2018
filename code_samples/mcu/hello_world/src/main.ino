#include <Streaming.h>

/* Define the pin that has an LED connected to it (in this case on the board) */
const int led_pin = 13;

void setup() {
  /* Open the VCP/serial port, this must be done before it is used */
  Serial.begin(9600);

  /* Set the mode of the PIN with an LED connected */
  pinMode(led_pin, OUTPUT);

  /* Set the LED pin low/off */
  digitalWrite(led_pin, LOW);
}

void loop() {
  /* Get the previous state of the LED pin */
  const auto led_state = digitalRead(led_pin);

  /* Set the LED pin to the opposite of what it just was (toggle it) */
  const auto new_led_state = !led_state;
  digitalWrite(led_pin, new_led_state);

  /* Send some data via serial */
  Serial << "The LED was " << led_state << ", now it is " << new_led_state
         << '\n';

  /* Wait 100 milliseconds (0.1 seconds) */
  delay(100);
}
