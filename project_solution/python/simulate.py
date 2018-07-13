#!/usr/bin/env python2

from __future__ import print_function

import IPython

from state_controller.state_machine import SafetySystem


fsm = SafetySystem()
IPython.embed()
