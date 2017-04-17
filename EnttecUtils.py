import sys
import time
import EnttecUsbDmxPro
import serial
try:
	import serial.tools
	import serial.tools.list_ports
	serial_tools_avail = True
except ImportError:
	serial_tools_avail = False


dmx = EnttecUsbDmxPro.EnttecUsbDmxPro()

data = [0]*512

def begin(port):
	dmx.setPort(port)
	dmx.connect()

def send():
	dmx.sendDMX(data)

def on(ch):
	global data
	data[ch] = 255
	send()

def off(ch):
	global data
	data[ch] = 255
	send()

def one(ch):
	global data
	data = [0]*255
	data[ch] = 255
	send()

def oneBox(box):
	allOff()
	for i in range(0,16):
		on(getDMX(box,i))

def getDMX(box, plug):
	return box*16+plug

def allOn():
	global data
	data = [255]*512
	send()

def allOff():
	global data
	data = [0]*512
	send()

def loop(start, end, t):
	for i in range(start, end+1):
		one(i)
		time.sleep(t)
begin("/dev/ttyUSB0")