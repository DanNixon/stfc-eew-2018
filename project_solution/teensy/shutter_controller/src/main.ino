#include <communication.h>
#include <led.h>
#include <types.h>

const uint8_t this_node_type = DEVICE_SHUTTER_CONTROL;
const uint8_t this_node_id = 0;

const int led_pin = 14;
const int openButton_Pin = 15;
const int closeButton_Pin = 16;

volatile unsigned long last_change_time[] = {0, 0};
volatile bool button_pushed[] = {false, false};

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

void handle_button_interrupt(int index) {
  const auto now = millis();

  if (now - last_change_time[index] > 500) {
    button_pushed[index] = true;
    last_change_time[index] = now;
  }
}
void open_shutter_button_interrupt() { handle_button_interrupt(0); }

void close_shutter_button_interrupt() { handle_button_interrupt(1); }

void setup() {
  Serial.begin(9600);

  /* Initialise LED */
  led_init();

  /* Initialise search button pin */
  pinMode(openButton_Pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(openButton_Pin),
                  open_shutter_button_interrupt, FALLING);

  pinMode(closeButton_Pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(closeButton_Pin),
                  close_shutter_button_interrupt, FALLING);

  /* Wait for serial connection to be established */
  while (!Serial) {
    delay(500);
  }
}

void loop() {
  /* Poll for new messages */
  communication_poll();

  for (uint8_t i = 0; i < 2; i++) {
    /* Check if search button was pushed */
    if (button_pushed[i]) {
      button_pushed[i] = false;

      /* Send message if it was */
      communication_tx(CMD_BUTTON_PRESS, &i, 1);
    }
  }

  delay(1);
}
