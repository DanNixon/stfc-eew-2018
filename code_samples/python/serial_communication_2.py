#!/usr/bin/env python2

from __future__ import print_function

import sys
import time
from threading import Thread, Event
from Queue import Queue

import crcmod.predefined
import serial
from transitions.extensions import LockedMachine as Machine
from transitions import State


class Device(object):

    def __init__(self, port_name):
        self.port = serial.Serial(
            port=port_name,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )

        self._read_thread = None
        self._read_thread_exit = Event()

    def start_async_reading(self, cb):
        def do_read():
            while not self._read_thread_exit.is_set():
                msg = self.receive_message()
                if msg is not None:
                    cb(msg)

        self._read_thread_exit.clear()
        self._read_thread = Thread(target=do_read)
        self._read_thread.start()

    def stop_async_reading(self):
        self._read_thread_exit.set()
        if self._read_thread is not None:
            self._read_thread.join()

    def _transmit(self, payload):
        crc = crcmod.predefined.Crc('crc-8')
        crc.update(chr(len(payload)))
        crc.update(payload)

        self.port.write('>')
        self.port.write(chr(len(payload)))
        for b in payload:
            self.port.write(b)
        self.port.write(chr(crc.crcValue))
        self.port.write('\x00')

    def _receive(self):
        c = self.port.read()
        if c == '>':
            length = ord(self.port.read())
            payload = self.port.read(length)

            crc = crcmod.predefined.Crc('crc-8')
            crc.update(chr(length))
            crc.update(payload)

            rx_crc = ord(self.port.read())
            if rx_crc == crc.crcValue and self.port.read() == '\x00':
                return payload

    def send_message(self, node_type, node_id, command, payload=None):
        message = chr(node_type) + chr(node_id) + chr(command)
        if payload is not None:
            message = message + payload
        self._transmit(message)

    def receive_message(self):
        payload = self._receive()
        if payload is None:
            return None

        return ord(payload[0]), ord(payload[1]), ord(payload[2]), payload[3:]


class DeviceGroup(object):

    def __init__(self, devices):
        self.devices = devices
        self.rx_msg_queue = Queue()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop_async_reading()

    def start_async_reading(self):
        def handle(msg):
            self.rx_msg_queue.put(msg)

        for d in self.devices:
            d.start_async_reading(handle)

    def stop_async_reading(self):
        for d in self.devices:
            d.stop_async_reading()

    @property
    def rx_messages_waiting(self):
        return not self.rx_msg_queue.empty()

    def next_rx_message(self):
        return self.rx_msg_queue.get()

    def send_message(self, node_type, node_id, command, payload=None):
        for d in self.devices:
            d.send_message(node_type, node_id, command, payload)


class TestFSM(object):

    states = [
        State('r', on_enter='set_red'),
        State('g', on_enter='set_green'),
        State('b', on_enter='set_blue')
    ]

    def __init__(self, device_group):
        self.device_group = device_group

        self.machine = Machine(self, states=TestFSM.states, initial='r')

        self.machine.add_transition(
            trigger='switch',
            source='r',
            dest='g'
        )

        self.machine.add_transition(
            trigger='switch',
            source='g',
            dest='b'
        )

        self.machine.add_transition(
            trigger='switch',
            source='b',
            dest='r'
        )

    def set_red(self):
        self.device_group.send_message(4, 0, 3, b'\xff\x00\x00')

    def set_green(self):
        self.device_group.send_message(4, 0, 3, b'\x00\xff\x00')

    def set_blue(self):
        self.device_group.send_message(4, 0, 3, b'\x00\x00\xff')

    def handle_message(self, msg):
        if msg[0] == 4 and msg[2] == 4 and msg[3] == '\x01':
            self.switch()


with DeviceGroup([Device(sys.argv[1])]) as dg:
    fsm = TestFSM(dg)

    dg.start_async_reading()

    while True:
        while dg.rx_messages_waiting:
            fsm.handle_message(dg.next_rx_message())
