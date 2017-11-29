#!/usr/bin/python
"""This is the super fun main file to run the whole thing. Be nice."""

import platform
import sys
import time
import threading

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
    elif platform.system() == 'Darwin':
        DPORT = '/dev/tty.usbserial-EN215593' 
        # Erwin: tty.usbserial-EN215593
        # Timmy: tty.usbserial-EN17533
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

PIXELS.start_websocket()
PIXELS.start_webserver()

PIXELS.set_color(0, 0, Color.RED)

# def infinit_test():
#     while True:
#         color = Color.RED
#         for x in range(5):
#             for y in range(12):
#                 PIXELS.set_color(x, y, color)
#                 time.sleep(1)

#         color = Color.OFF
#         for x in range(5):
#             for y in range(12):
#                 PIXELS.set_color(x, y, color)
#                 time.sleep(1)

#         color = Color.GREEN
#         for x in range(5):
#             for y in range(12):
#                 PIXELS.set_color(x, y, color)
#                 time.sleep(1)

# test_thread = threading.Thread(target=infinit_test)
# test_thread.daemon = True
# test_thread.start()

command = None
while command != "stop":
    command = raw_input("Enter a command: ")