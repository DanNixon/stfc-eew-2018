#include <FastCRC.h>

const uint8_t start = '>';
const uint8_t end = '\0';

FastCRC8 crc8;

const size_t serial_buffer_length = 32;
uint8_t serial_buffer[serial_buffer_length];

void handle_message(uint8_t *buffer, size_t length) {
  send_message(buffer, length);

  const uint32_t now = millis();
  send_message((uint8_t *)&now, sizeof(uint32_t));
}

void send_message(uint8_t *buffer, size_t length) {
  uint8_t message_buffer[length + 4];
  message_buffer[0] = start;
  message_buffer[1] = length;
  memcpy(message_buffer + 2, buffer, length);
  message_buffer[length + 2] = crc8.smbus(message_buffer + 1, length + 1);
  message_buffer[length + 3] = end;

  for (int i = 0; i < length + 4; i++) {
    Serial.print((char)message_buffer[i]);
  }
}

void setup() {
  Serial.begin(9600);

  /* Wait for serial connection to be established */
  while (!Serial) {
    delay(500);
  }

  /* Send an empty message when we are online */
  char *msg = "Hello!";
  send_message((uint8_t *)msg, strlen(msg));
}

void handle_serial() {
  if (Serial.available() >= 2) {
    /* If we have received the start marker */
    if (Serial.read() == start) {
      /* Read payload length */
      serial_buffer[0] = Serial.read();
      const size_t length = serial_buffer[0];

      /* Wait for remainder of serial data to be available */
      const auto start = millis();
      while (Serial.available() < length + 2) {
        /* Check if a timeout has elapsed */
        if (millis() - start > 500) {
          return;
        }
        delay(5);
      }

      /* Read message payload */
      for (size_t i = 0; i < length; i++) {
        serial_buffer[i + 1] = Serial.read();
      }

      /* Read CRC sent by PC */
      const uint8_t crc_rx = Serial.read();

      /* Compare received CRC with calculated CRC and check for null terminator
       * character */
      if (crc8.smbus(serial_buffer, length + 1) == crc_rx &&
          Serial.read() == end) {
        /* Call message handler if payload is OK */
        handle_message(serial_buffer + 1, length);
      }
    }
  }
}

void loop() {
  handle_serial();

  delay(10);
}
