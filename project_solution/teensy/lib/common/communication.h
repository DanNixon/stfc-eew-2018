#include <Arduino.h>

#pragma once

extern const uint8_t this_node_type;
extern const uint8_t this_node_id;

void communication_poll();
void communication_tx(uint8_t cmd, uint8_t* payload, size_t payload_len);

void communication_rx(uint8_t cmd, uint8_t* payload, size_t payload_len);
