#include <communication.h>
#include <led.h>
#include <types.h>

const uint8_t this_node_type = DEVICE_KEY_RACK;
const uint8_t this_node_id = 0;

const int led_pin = 14;
const int key_rack_switch_pin = 15;

volatile unsigned long last_change_time = 0;
volatile bool key_rack_state_changed = false;

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

void handle_key_rack_interupt() {
  const auto now = millis();

  if (now - last_change_time > 50) {
    key_rack_state_changed = true;
    last_change_time = now;
  }
}

void setup() {
  Serial.begin(9600);

  /* Initialise LED */
  led_init();

  /* Initialise key rack switch pin */
  pinMode(key_rack_switch_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(key_rack_switch_pin),
                  handle_key_rack_interupt, CHANGE);

  /* Wait for serial connection to be established */
  while (!Serial) {
    delay(500);
  }
}

void loop() {
  /* Poll for new messages */
  communication_poll();

  /* Check if key rack state has changed */
  if (key_rack_state_changed) {
    key_rack_state_changed = false;

    /* Get new switch state (state is 0x01 if all keys are in place 0x00 if
     * not)*/
    delay(2);
    const uint8_t state = !digitalRead(key_rack_switch_pin);

    /* Send message if it has */
    communication_tx(CMD_STATE_CHANGED, (uint8_t*)&state, 1);
  }

  delay(1);
}
