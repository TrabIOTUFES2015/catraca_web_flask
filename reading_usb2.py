from serial import *
from threading import Thread
from time import sleep
from serial_stream import SerialStream

ser = SerialStream(
		port='/dev/ttyUSB1',
        baudrate=57600,
        # baudrate=111200,
        # baudrate=96600,
        # bytesize=EIGHTBITS,
        # parity=PARITY_NONE,
        # stopbits=STOPBITS_ONE,
        timeout=0.1,
        xonxoff=0,
        rtscts=0,
        interCharTimeout=None,
        bytesize=8, parity=PARITY_EVEN, stopbits=STOPBITS_ONE
	)


while True:
	s = ser.read(100)
	if (s):
		print s