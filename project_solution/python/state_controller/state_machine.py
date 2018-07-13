from __future__ import print_function

from transitions import Machine, State
from .types import Command, DeviceType, DoorStates

COLOUR_OFF = b'\x00\x00\x00'
COLOUR_RED = b'\xff\x00\x00'
COLOUR_GREEN = b'\x00\xff\x00'
COLOUR_BLUE = b'\x00\x00\xff'
COLOUR_YELLOW = b'\xff\xff\x00'

class SafetySystem(object):

    states = [
        State(name='initial'),
        State(name='button_1_waiting', on_enter=['on_enter_button_1_waiting']),
        State(name='button_2_waiting', on_enter=['on_enter_button_2_waiting']),
        State(name='button_3_waiting', on_enter=['on_enter_button_3_waiting']),
        State(name='key_rack_waiting', on_enter=['on_enter_key_rack_waiting']),
        State(name='key_rack_full', on_enter=['on_enter_key_rack_full']),
        State(name='door_closed',on_enter=['on_enter_door_closed']),
        State(name='door_locking',on_enter=['on_enter_door_locking']),
        State(name='shutter_open',on_enter=['on_enter_shutter_open']),
        State(name='door_unlocking',on_enter=['on_enter_door_unlocking']),
        State(name='error',on_enter=['on_enter_error']),
    ]

    def __init__(self, device_group=None):
        self.device_group = device_group

        self.machine = Machine(
            model=self,
            states=SafetySystem.states,
            initial='initial'
        )

        self.machine.add_transition(
            trigger='press_search_point_1_button',
            source=['button_1_waiting'],
            dest='button_2_waiting'
        )

        self.machine.add_transition(
            trigger='press_search_point_2_button',
            source=['button_2_waiting'],
            dest='button_3_waiting'
        )

        self.machine.add_transition(
            trigger='press_search_point_3_button',
            source=['button_3_waiting'],
            dest='key_rack_waiting'
        )

        self.machine.add_transition(
            trigger='key_rack_full',
            source=['key_rack_waiting'],
            dest='key_rack_full'
        )

        self.machine.add_transition(
            trigger='key_rack_not_full',
            source=['key_rack_full'],
            dest='button_1_waiting'
        )

        self.machine.add_transition(
            trigger='door_is_closed',
            source=['key_rack_full'],
            dest='door_closed'
        )

        self.machine.add_transition(
            trigger='door_is_opening',
            source=['door_closed'],
            dest='button_1_waiting'
        )

        self.machine.add_transition(
            trigger='open_shutter',
            source=['door_closed'],
            dest='door_locking'
        )

        self.machine.add_transition(
            trigger='door_is_locked',
            source=['door_locking'],
            dest='shutter_open'
        )

        self.machine.add_transition(
            trigger='close_shutter',
            source=['shutter_open'],
            dest='door_unlocking'
        )

        self.machine.add_transition(
            trigger='door_is_unlocked',
            source=['door_unlocking'],
            dest='door_closed'
        )

        self.machine.add_transition(
            trigger='error',
            source='*',
            dest='error'
        )

    def handle_message(self, msg):
        print(msg)
        node_type, node_id, command, payload = msg

        if (node_type == DeviceType.SEARCH_POINT and node_id == 0):
            self.press_search_point_1_button()
        elif (node_type == DeviceType.SEARCH_POINT and node_id == 1):
            self.press_search_point_2_button()
        elif (node_type == DeviceType.SEARCH_POINT and node_id == 2):
            self.press_search_point_3_button()

        # TODO

    def on_enter_button_1_waiting(self):
        print('Waiting for search point 1')
        if self.device_group is not None:
            self.device_group.send_message(DeviceType.SEARCH_POINT, 0, Command.SET_LED, COLOUR_YELLOW)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 1, Command.SET_LED, COLOUR_OFF)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 2, Command.SET_LED, COLOUR_OFF)
            self.device_group.send_message(DeviceType.KEY_RACK, 0, Command.SET_LED, COLOUR_OFF)

    def on_enter_button_2_waiting(self):
        print('Waiting for search point 2')
        if self.device_group is not None:
            self.device_group.send_message(DeviceType.SEARCH_POINT, 0, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 1, Command.SET_LED, COLOUR_YELLOW)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 2, Command.SET_LED, COLOUR_OFF)
            self.device_group.send_message(DeviceType.KEY_RACK, 0, Command.SET_LED, COLOUR_OFF)

    def on_enter_button_3_waiting(self):
        print('Waiting for search point 3')
        if self.device_group is not None:
            self.device_group.send_message(DeviceType.SEARCH_POINT, 0, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 1, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 2, Command.SET_LED, COLOUR_YELLOW)
            self.device_group.send_message(DeviceType.KEY_RACK, 0, Command.SET_LED, COLOUR_OFF)

    def on_enter_key_rack_waiting(self):
        print('Blockhouse search complete, waiting for full key rack')
        if self.device_group is not None:
            self.device_group.send_message(DeviceType.SEARCH_POINT, 0, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 1, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 2, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.KEY_RACK, 0, Command.SET_LED, COLOUR_YELLOW)

    def on_enter_key_rack_full(self):
        print('Key rack is full, waiting for blockhouse door to be closed')
        if self.device_group is not None:
            self.device_group.send_message(DeviceType.SEARCH_POINT, 0, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 1, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.SEARCH_POINT, 2, Command.SET_LED, COLOUR_GREEN)
            self.device_group.send_message(DeviceType.KEY_RACK, 0, Command.SET_LED, COLOUR_GREEN)

    def on_enter_door_closed(self):
        print('Blockhouse door is closed, ready to lock door and open shutter')
        if self.device_group is not None:
            self.device_group.send_message(DeviceType.SHUTTER_CONTROL, 0, Command.SET_LED, COLOUR_GREEN)

    def on_enter_door_locking(self):
        print('Shutter open requested, locking blockhouse door')
        if self.device_group is not None:
            # TODO: send door lock command
            self.device_group.send_message(DeviceType.SHUTTER_CONTROL, 0, Command.SET_LED, COLOUR_YELLOW)

    def on_enter_shutter_open(self):
        print('Blockhouse door is locked, shutter is open')
        if self.device_group is not None:
            self.device_group.send_message(DeviceType.SHUTTER_CONTROL, 0, Command.SET_LED, COLOUR_BLUE)

    def on_enter_door_unlocking(self):
        print('Shutter is closed, unlocking blockhouse door')
        if self.device_group is not None:
            # TODO: send door unlock command
            self.device_group.send_message(DeviceType.SHUTTER_CONTROL, 0, Command.SET_LED, COLOUR_GREEN)

    def on_enter_error(self):
        print('There has been an error')
        if self.device_group is not None:
            self.device_group.send_message(DeviceType.SHUTTER_CONTROL, 0, Command.SET_LED, COLOUR_RED)
