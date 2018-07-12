from __future__ import print_function

from transitions import Machine, State
from .types import Command, DeviceType, DoorStates

class SafetySystem(object):

    states = [
        State(name='initial'),
        State(name='button_1_waiting', on_enter=['on_enter_button_1_waiting']),
        State(name='button_2_waiting', on_enter=['on_enter_button_2_waiting']),
        State(name='button_3_waiting', on_enter=['on_enter_button_3_waiting']),
        State(name='key_rack_waiting', on_enter=['on_enter_key_rack_waiting']),
        State(name='door_closing', on_enter=['on_enter_door_closing']),
        State(name='door_closed',on_enter=['on_enter_door_closed']),
        State(name='searched_and_locked',on_enter=['on_enter_searched_and_locked']),
        State(name='door_opening', on_enter=['on_enter_door_opening']),
        State(name='door_open', on_enter=['on_enter_door_open']),
        State(name='shutter_closing',on_enter=['on_enter_shutter_closing']),
        State(name='ready', on_enter=['on_enter_ready']),
        State(name='shutter_open', on_enter=['on_enter_shutter_open']),
        State(name='error',on_enter=['on_enter_error']),
    ]

    def __init__(self, device_group):
        self.device_group = device_group

        self.machine = Machine(
            model=self,
            states=SafetySystem.states,
            initial='initial'
        )

        self.machine.add_transition(
            trigger='press_button1',
            source=['button_1_waiting'],
            dest='button_2_waiting'
        )

        self.machine.add_transition(
            trigger='press_button2',
            source=['button_2_waiting'],
            dest='button_3_waiting'
        )

        self.machine.add_transition(
            trigger='press_button3',
            source=['button_3_waiting'],
            dest='key_rack_waiting'
        )

        self.machine.add_transition(
            trigger='key_rack_full',
            source=['key_rack_waiting'],
            dest='door_closing'
        )

        self.machine.add_transition(
            trigger='closed_limit_switch',
            source='door_closing',
            dest='door_closed'
        )

        self.machine.add_transition(
            trigger='door_locked',
            source='door_closed',
            dest='searched_and_locked'
        )

        self.machine.add_transition(
            trigger='open_door',
            source=['door_closed', 'door_closing', 'searched_and_locked'],
            dest='door_opening'
        )

        self.machine.add_transition(
            trigger='closed_limit_switch',
            source=['door_opening','door_open'],
            dest='error'
        )

        self.machine.add_transition(
            trigger='open_limit_switch',
            source='door_opening',
            dest='door_open'
        )

        self.machine.add_transition(
            trigger='open_limit_switch',
            source=['door_closing', 'door_closed'],
            dest='error'
        )

        self.machine.add_transition(
            trigger='safety_edge_hit',
            source=['door_opening', 'door_closing'],
            dest='error'
        )

        self.machine.add_transition(
            trigger='close_shutter',
            source=['searched_and_locked', 'shutter_open'],
            dest='shutter_closing'
        )

        self.machine.add_transition(
            trigger='shutter_closed',
            source=['shutter_closing'],
            dest='ready'
        )

        self.machine.add_transition(
            trigger='open_shutter',
            source=['shutter_closing','ready'],
            dest='shutter_open'
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
            self.press_button1()
        elif (node_type == DeviceType.SEARCH_POINT and node_id == 1):
            self.press_button2()
        elif (node_type == DeviceType.SEARCH_POINT and node_id == 2):
            self.press_button3()

        # TODO

    def on_enter_button_1_waiting(self):
        self.device_group.send_message(DeviceType.SEARCH_POINT, 0, Command.SET_LED, b'\xff\xff\x00')

    def on_enter_button_2_waiting(self):
        self.device_group.send_message(DeviceType.SEARCH_POINT, 0, Command.SET_LED, b'\x00\xff\x00')
        self.device_group.send_message(DeviceType.SEARCH_POINT, 1, Command.SET_LED, b'\xff\xff\x00')

    def on_enter_button_3_waiting(self):
        self.device_group.send_message(DeviceType.SEARCH_POINT, 1, Command.SET_LED, b'\x00\xff\x00')
        self.device_group.send_message(DeviceType.SEARCH_POINT, 2, Command.SET_LED, b'\xff\xff\x00')

    def on_enter_key_rack_waiting(self):
        self.device_group.send_message(DeviceType.SEARCH_POINT, 2, Command.SET_LED, b'\x00\xff\x00')
        self.device_group.send_message(DeviceType.KEY_RACK, 0, Command.SET_LED, b'\xff\xff\x00')

    def on_enter_door_closing(self):
        print('Change key rack LED green - door is closing')
        # TODO

    def on_enter_door_closed(self):
        print('Door closed, confirm locked')
        # TODO

    def on_enter_searched_and_locked(self):
        print('Door locked, ready to close shutter')
        # TODO

    def on_enter_door_opening(self):
        print('The door is opening')
        # TODO

    def on_enter_door_open(self):
        print('The door is open')
        # TODO

    def on_enter_shutter_closing(self):
        print('Please confirm when the shutter is closed')
        # TODO

    def on_enter_ready(self):
        self.device_group.send_message(DeviceType.SHUTTER_CONTROL, 0, Command.SET_LED, b'\x00\xff\x00')

    def on_enter_shutter_open(self):
        self.device_group.send_message(DeviceType.SHUTTER_CONTROL, 0, Command.SET_LED, b'\x00\x00\xff')

    def on_enter_error(self):
        print('There has been an error.')
        self.device_group.send_message(DeviceType.SHUTTER_CONTROL, 0, Command.SET_LED, b'\xff\x00\x00')
