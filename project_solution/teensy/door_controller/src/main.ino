#include <Fsm.h>
#include <communication.h>
#include <led.h>
#include <types.h>

enum StateTransitions {
  ST_CMD_OPEN,
  ST_CMD_CLOSE,
  ST_SAFETY_EDGE_HIT,
  ST_CMD_LOCK,
  ST_CMD_UNLOCK,
  ST_LIMIT_OPEN,
  ST_LIMIT_CLOSED
};

int8_t green_flash = -1;
int8_t yellow_flash = -1;

void on_enter_state_unknown() {
  led_set(0, 0, 0);
  uint8_t msg = DOOR_STATE_UNKNOWN;
  communication_tx(CMD_STATE_CHANGED, &msg, 1);
}

void on_enter_state_open() {
  led_set(0, 255, 0);
  uint8_t msg = DOOR_STATE_OPEN;
  communication_tx(CMD_STATE_CHANGED, &msg, 1);
}

void on_enter_state_closed() {
  led_set(255, 255, 0);
  uint8_t msg = DOOR_STATE_CLOSED;
  communication_tx(CMD_STATE_CHANGED, &msg, 1);
}

void on_enter_state_error() {
  led_set(255, 0, 0);
  uint8_t msg = DOOR_STATE_ERROR;
  communication_tx(CMD_STATE_CHANGED, &msg, 1);
}

void on_enter_state_opening() {
  green_flash = 0;
  uint8_t msg = DOOR_STATE_OPENING;
  communication_tx(CMD_STATE_CHANGED, &msg, 1);
}

void on_exit_state_opening() { green_flash = -1; }

void on_enter_state_closing() {
  yellow_flash = 0;
  uint8_t msg = DOOR_STATE_CLOSING;
  communication_tx(CMD_STATE_CHANGED, &msg, 1);
}

void on_exit_state_closing() { yellow_flash = -1; }

void on_enter_state_locked() {
  led_set(0, 0, 255);
  uint8_t msg = DOOR_STATE_LOCKED;
  communication_tx(CMD_STATE_CHANGED, &msg, 1);
}

State state_unknown(on_enter_state_unknown, NULL, NULL);
State state_error(on_enter_state_error, NULL, NULL);
State state_open(on_enter_state_open, NULL, NULL);
State state_opening(on_enter_state_opening, NULL, on_exit_state_opening);
State state_closed(on_enter_state_closed, NULL, NULL);
State state_closing(on_enter_state_closing, NULL, on_exit_state_closing);
State state_locked(on_enter_state_locked, NULL, NULL);

Fsm fsm(&state_unknown);

const uint8_t this_node_type = DEVICE_DOOR;
const uint8_t this_node_id = 0;

const int led_pin = 14;
// Open = 16, Close = 15, Safety = 17, limit up -> open = 18, limit down ->
// close = 19.
const int input_pins[] = {16, 15, 17, 18, 19};

volatile unsigned long last_change_time[] = {0, 0, 0, 0, 0};
volatile bool button_pushed[] = {false, false, false, false, false};

void communication_rx(uint8_t cmd, uint8_t *payload, size_t payload_len) {
  switch (cmd) {
    case CMD_DOOR_LOCK: {
      if (payload_len == 1) {
        if (payload[0] == 1) {
          fsm.trigger(ST_CMD_LOCK);
        } else if (payload[0] == 0) {
          fsm.trigger(ST_CMD_UNLOCK);
        }
      }
      break;
    }
  }
}

void handle_input_interrupt(int index) {
  const auto now = millis();

  if (now - last_change_time[index] > 500) {
    button_pushed[index] = true;
    last_change_time[index] = now;
  }
}

void open_door_button_interrupt() { handle_input_interrupt(0); }

void close_door_button_interrupt() { handle_input_interrupt(1); }

void safety_switch_interrupt() { handle_input_interrupt(2); }

void open_limit_switch_interrupt() { handle_input_interrupt(3); }

void closed_limit_switch_interrupt() { handle_input_interrupt(4); }

void setup() {
  Serial.begin(9600);

  /* Initialise LED */
  led_init();

  /* Initialise search button pin */
  pinMode(input_pins[0], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(input_pins[0]),
                  open_door_button_interrupt, FALLING);

  pinMode(input_pins[1], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(input_pins[1]),
                  close_door_button_interrupt, FALLING);

  pinMode(input_pins[2], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(input_pins[2]), safety_switch_interrupt,
                  FALLING);

  pinMode(input_pins[3], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(input_pins[3]),
                  open_limit_switch_interrupt, FALLING);

  pinMode(input_pins[4], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(input_pins[4]),
                  closed_limit_switch_interrupt, FALLING);

  /* Wait for serial connection to be established */
  while (!Serial) {
    delay(500);
  }

  fsm.add_transition(&state_unknown, &state_opening, ST_CMD_OPEN, NULL);
  fsm.add_transition(&state_open, &state_closing, ST_CMD_CLOSE, NULL);
  fsm.add_transition(&state_closing, &state_closed, ST_LIMIT_CLOSED, NULL);
  fsm.add_transition(&state_closed, &state_locked, ST_CMD_LOCK, NULL);
  fsm.add_transition(&state_locked, &state_closed, ST_CMD_UNLOCK, NULL);
  fsm.add_transition(&state_closed, &state_opening, ST_CMD_OPEN, NULL);
  fsm.add_transition(&state_opening, &state_error, ST_LIMIT_CLOSED, NULL);
  fsm.add_transition(&state_opening, &state_error, ST_SAFETY_EDGE_HIT, NULL);
  fsm.add_transition(&state_closing, &state_error, ST_SAFETY_EDGE_HIT, NULL);
  fsm.add_transition(&state_closing, &state_error, ST_LIMIT_OPEN, NULL);
  fsm.add_transition(&state_opening, &state_open, ST_LIMIT_OPEN, NULL);
}

uint32_t last_time = 0;

void loop() {
  /* Poll for new messages */
  communication_poll();

  fsm.run_machine();

  /* Handle buttons */
  for (uint8_t i = 0; i < 5; i++) {
    if (button_pushed[i]) {
      button_pushed[i] = false;

      if (i == 0) {
        fsm.trigger(ST_CMD_OPEN);
      }
      if (i == 1) {
        fsm.trigger(ST_CMD_CLOSE);
      }
      if (i == 2) {
        fsm.trigger(ST_SAFETY_EDGE_HIT);
      }
      if (i == 3) {
        fsm.trigger(ST_LIMIT_OPEN);
      }
      if (i == 4) {
        fsm.trigger(ST_LIMIT_CLOSED);
      }
    }
  }

  delay(1);

  uint32_t now = millis();

  // For Yellow Flashing LED
  if (yellow_flash != -1 && now - last_time > 500) {
    last_time = now;

    if (yellow_flash == 0) {
      led_set(255, 180, 0);
    } else {
      led_set(0, 0, 0);
    }

    yellow_flash = !yellow_flash;
  }

  // for green flashing led
  if (green_flash != -1 && now - last_time > 500) {
    last_time = now;

    if (green_flash == 0) {
      led_set(0, 255, 0);
    } else {
      led_set(0, 0, 0);
    }

    green_flash = !green_flash;
  }
}
