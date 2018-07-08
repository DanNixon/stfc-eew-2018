#include <FastCRC.h>

const uint8_t start = '>';

FastCRC8 CRC8;

void send_message(uint8_t * buffer, size_t length)
{
  uint8_t message_buffer[length + 4];
  message_buffer[0] = start;
  message_buffer[1] = length;
  memcpy(message_buffer + 2, buffer, length);
  message_buffer[length + 2] = CRC8.smbus(message_buffer + 1, length + 1);
  message_buffer[length + 3] = '\0';

  for (int i = 0; i < length + 4; i++) {
    Serial.print((char)message_buffer[i]);
  }
}

void setup() {
  Serial.begin(9600);

  while(!Serial)
  {
    delay(500);
  }
}

void loop() {
  const uint32_t now = millis();
  send_message((uint8_t *) &now, sizeof(uint32_t));

  delay(1000);
}
