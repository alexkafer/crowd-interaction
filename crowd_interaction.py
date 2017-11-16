#!/usr/bin/python
"""This is the super fun main file to run the whole thing. Be nice."""

import platform
import sys
import time

from PixelManager import PixelManager, Color
import EnttecUsbDmxPro


print "Welcome to the Crowd Interaction software. We put the cool in cool beans."

print " - Initializing PixelManager"
PIXELS = PixelManager()

print " - Initializing EnttecUsbDmxPro"
DMX = EnttecUsbDmxPro.EnttecUsbDmxPro()

DPORT = None
if len(sys.argv) < 2:
    if platform.system() == 'Linux':
        DPORT = '/dev/ttyUSB0'
    elif platform.system() == 'Mac':
        DPORT = '/dev/tty.usbserial-ENT095626'
else:
    DPORT = sys.argv[1]

if DPORT is None:
    DMX.list()
    sys.stderr.write("ERROR: No serial port for DMX detected!\n")
    sys.exit()

print " - dport selected as " + DPORT

DMX.setPort(DPORT)
DMX.connect()

PIXELS.link_dmx(DMX)

PIXELS.set_color(0, 0, Color.RED)

print PIXELS.get_pixels()[0]
