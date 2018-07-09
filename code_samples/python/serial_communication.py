#!/usr/bin/env python2

from __future__ import print_function

import sys

import crcmod.predefined
import serial


port = serial.Serial(
    port=sys.argv[1],
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)


def handle_message(payload):
    values = [hex(ord(v)) for v in payload]
    print("Payload:", ' '.join(values))


def send_message(payload):
    crc = crcmod.predefined.Crc('crc-8')
    crc.update(chr(len(payload)))
    crc.update(payload)

    port.write('>')
    port.write(chr(len(payload)))
    for b in payload:
        port.write(b)
    port.write(chr(crc.crcValue))
    port.write('\x00')


send_message(b'\x01\x02\x03\x04\x05\x06\x07\x08')

while True:
    c = port.read()
    if c == '>':
        length = ord(port.read())
        payload = port.read(length)

        crc = crcmod.predefined.Crc('crc-8')
        crc.update(chr(length))
        crc.update(payload)

        rx_crc = ord(port.read())
        if rx_crc == crc.crcValue and port.read() == '\x00':
            handle_message(payload)
