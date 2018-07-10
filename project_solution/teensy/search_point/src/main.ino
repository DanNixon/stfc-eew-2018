#include <communication.h>
#include <led.h>
#include <types.h>

const uint8_t this_node_type = DEVICE_SEARCH_POINT;
const uint8_t this_node_id = 0;
const int led_pin = 14;

const int search_button_pin = 15;

volatile unsigned long last_change_time = 0;
volatile bool search_button_pushed = false;

void communication_rx(uint8_t cmd, uint8_t* payload, size_t payload_len) {
  switch (cmd) {
    case CMD_SET_LED: {
      if (payload_len == 3) {
        led_set(payload[0], payload[1], payload[2]);
      }
      break;
    }
  }
}

void handle_search_button_interrupt() {
  const auto now = millis();

  if (now - last_change_time > 500) {
    search_button_pushed = true;
    last_change_time = now;
  }
}

void setup() {
  Serial.begin(9600);

  /* Initialise LED */
  led_init();

  /* Initialise search button pin */
  pinMode(search_button_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(search_button_pin),
                  handle_search_button_interrupt, FALLING);

  /* Wait for serial connection to be established */
  while (!Serial) {
    delay(500);
  }
}

void loop() {
  /* Poll for new messages */
  communication_poll();

  /* Check if search button was pushed */
  if (search_button_pushed) {
    search_button_pushed = false;

    /* Send message if it was */
    communication_tx(CMD_BUTTON_PRESS, NULL, 0);
  }

  delay(1);
}
