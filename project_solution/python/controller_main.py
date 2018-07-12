#!/usr/bin/env python2

from __future__ import print_function

import sys

from state_controller.device import Device, DeviceGroup
from state_controller.sttae_machine import SafetySystem


with DeviceGroup([Device(p) for p in sys.argv[1:]]) as dg:
    print(dg.device_count, 'device(s) connected.')

    fsm = SafetySystem(dg)
    dg.start_async_reading()

    while True:
        while dg.rx_messages_waiting:
            fsm.handle_message(dg.next_rx_message())
