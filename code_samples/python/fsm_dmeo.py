#!/usr/bin/env python2

# Best run through IPython: open IPython and use `%run fsm_demo.py`

from __future__ import print_function

from transitions import Machine


class Door(object):

    states = ['closed', 'open', 'closing', 'opening', 'error', 'unknown position']

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
            source='*',
            dest='error'
        )
        self.machine.add_transition(
            trigger='safety_edge_hit',
            source='*',
            dest='error'
        )

        self.machine.add_transition(
            trigger='error',
            source='*',
            dest='error'
        )


d = Door();
