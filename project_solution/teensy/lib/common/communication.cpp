#include "communication.h"

#include <FastCRC.h>

const uint8_t start_byte = '>';
const uint8_t end_byte = '\0';
const size_t buffer_length = 32;

uint8_t buffer[buffer_length];
FastCRC8 crc8;

void communication_send(uint8_t* buffer, size_t length);
void communication_handle_message(uint8_t* buffer, size_t length);

void communication_poll() {
  if (Serial.available() >= 2) {
    /* If we have received the start_byte marker */
    if (Serial.read() == start_byte) {
      /* Read payload length */
      buffer[0] = Serial.read();
      const size_t length = buffer[0];

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
        buffer[i + 1] = Serial.read();
      }

      /* Read CRC sent by PC */
      const uint8_t crc_rx = Serial.read();

      /* Compare received CRC with calculated CRC and check for null terminator
       * character */
      if (crc8.smbus(buffer, length + 1) == crc_rx &&
          Serial.read() == end_byte) {
        /* Call message handler if payload is OK */
        communication_handle_message(buffer + 1, length);
      }
    }
  }
}

void communication_tx(uint8_t cmd, uint8_t* payload, size_t payload_len) {
  const size_t length = payload_len + 3;
  uint8_t buffer[length];
  buffer[0] = this_node_type;
  buffer[1] = this_node_id;
  buffer[2] = cmd;
  memcpy(buffer + 3, payload, payload_len);
  communication_send(buffer, length);
}

void communication_send(uint8_t* buffer, size_t length) {
  uint8_t message_buffer[length + 4];
  message_buffer[0] = start_byte;
  message_buffer[1] = length;
  memcpy(message_buffer + 2, buffer, length);
  message_buffer[length + 2] = crc8.smbus(message_buffer + 1, length + 1);
  message_buffer[length + 3] = end_byte;

  for (size_t i = 0; i < length + 4; i++) {
    Serial.print((char)message_buffer[i]);
  }
}

void communication_handle_message(uint8_t* buffer, size_t length) {
  if (length < 3 || buffer[0] != this_node_type || buffer[1] != this_node_id) {
    return;
  }

  communication_rx(buffer[2], buffer + 3, length - 3);
}
