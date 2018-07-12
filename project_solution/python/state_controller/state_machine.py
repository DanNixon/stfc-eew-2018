from __future__ import print_function

from transitions import Machine, State

class SafetySystem(object):

    states = [
        State(name='button1_waiting'),
        State(name='button2_waiting', on_enter=['B12LED']),
        State(name='button3_waiting', on_enter=['B23LED']),
        State(name='key_rack_waiting', on_enter=['B3keyrackLED']),
        State(name='door_closing', on_enter=['keyrackLED']),
        State(name='door_closed',on_enter=['on_closed']),
        State(name='searched_and_locked',on_enter=['on_locked']),
        State(name='door_opening', on_enter=['dooropening']),
        State(name='door_open', on_enter=['dooropen']),
        State(name='shutter_closing',on_enter=['confirm_shutter_closed']),
        State(name='ready', on_enter=['readymessage']),
        State(name='shutter_open', on_enter=['shutteropen']),
        State(name='error',on_enter=['error_message']),
    ]

    def __init__(self):
        self.machine = Machine(
            model=self,
            states=SafetySystem.states,
            initial='button1_waiting'
        )
        self.machine.add_transition(
            trigger='press_button1',
            source=['button1_waiting'],
            dest='button2_waiting'
        )
        self.machine.add_transition(
            trigger='press_button2',
            source=['button2_waiting'],
            dest='button3_waiting'
        )
        self.machine.add_transition(
            trigger='press_button3',
            source=['button3_waiting'],
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
            source=['door_closed','door_closing','searched_and_locked'],
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
            source=['door_closing','door_closed'],
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

    def B12LED(self):
        print('Change LED 1 green and LED 2 yellow')
    def B23LED(self):
        print('Change LED 2 green and LED 3 yellow')
    def B3keyrackLED(self):
        print('Change LED 3 green and key rack LED yellow')
    def keyrackLED(self):
        print('Change key rack LED green - door is closing')
    def on_closed(self):
        print('Door closed, confirm locked')
    def on_locked(self):
        print('Door locked, ready to close shutter')
    def dooropening(self):
        print('The door is opening')
    def dooropen(self):
        print('The door is open')
    def confirm_shutter_closed(self):
        print('Please confirm when the shutter is closed')
    def readymessage(self):
        print('The area is now ready to start')
    def shutteropen(self):
        print('The shutter is now open')
    def error_message(self):
        print('There has been an error')
