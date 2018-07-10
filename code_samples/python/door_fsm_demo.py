#!/usr/bin/env python2

# Best run through IPython: open IPython and use `%run door_fsm_demo.py`

from __future__ import print_function

from transitions import Machine, State


class Door(object):

    states = [
        State(name='closed', on_enter=['on_closed']),
        State(name='open', on_enter=['on_open']),
        State(name='closing'),
        State(name='opening'),
        State(name='error', on_enter=['on_error']),
        State(name='unknown position')
    ]

    def __init__(self):
        self.machine = Machine(
            model=self,
            states=Door.states,
            initial='unknown position'
        )

        self.machine.add_transition(
            trigger='close_door',
            source=['unknown position', 'open'],
            dest='closing'
        )

        self.machine.add_transition(
            trigger='open_door',
            source=['unknown position', 'closed', 'closing'],
            dest='opening'
        )

        self.machine.add_transition(
            trigger='closed_limit_switch',
            source='closing',
            dest='closed'
        )

        self.machine.add_transition(
            trigger='closed_limit_switch',
            source='opening',
            dest='error'
        )

        self.machine.add_transition(
            trigger='open_limit_switch',
            source='opening',
            dest='open'
        )

        self.machine.add_transition(
            trigger='open_limit_switch',
            source='closing',
            dest='error'
        )

        self.machine.add_transition(
            trigger='safety_edge_hit',
            source=['opening', 'closing'],
            dest='error'
        )

        self.machine.add_transition(
            trigger='error',
            source='*',
            dest='error'
        )

    def on_open(self):
        print('The door is now open')

    def on_error(self):
        print('The dorr is now closed.')

    def on_error(self):
        print('Oh no, it\'s all gone wrong!')


d = Door();
