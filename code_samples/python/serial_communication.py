#!/usr/bin/env python

import sys

import crcmod.predefined
import serial


port = serial.Serial(sys.argv[1])


def handle_message(payload):
    values = [hex(ord(v)) for v in payload]
    print ' '.join(values)


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
