#!/usr/bin/env python2

from __future__ import print_function

import sys

from state_controller.device import Device, DeviceGroup


with DeviceGroup([Device(p) for p in sys.argv[1:]]) as dg:
    print(dg.device_count, 'device(s) connected.')
    dg.start_async_reading()

    while True:
        while dg.rx_messages_waiting:
            print(dg.next_rx_message())
