from enum import IntEnum

class Command(IntEnum):
  ALIVE = 1
  HEARTBEAT = 2
  SET_LED = 3
  STATE_CHANGED = 4
  BUTTON_PRESS = 5
  SWITCH_CHANGE = 6
  DOOR_LOCK = 7

class DeviceType(IntEnum):
  SEARCH_POINT = 1
  SHUTTER_CONTROL = 2
  DOOR = 3
  KEY_RACK = 4

class DoorStates(IntEnum):
  UNKNOWN = 1
  CLOSED = 2
  CLOSING = 3
  OPEN = 4
  OPENING = 5
  ERROR = 6
  LOCKED = 7
