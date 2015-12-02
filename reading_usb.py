from serial import *
from threading import Thread
from time import sleep

last_received = ''

def receiving(ser):
    global last_received
    buffer = ''

    while True:
        # last_received = ser.readline()
        buffer = ser.read(ser.inWaiting())
        # if '\n' in buffer:
        #     last_received, buffer = buffer.split('\n')[-2:]
        print(buffer.decode('LATIN1'))
        # buffer1 = buffer.decode('utf-8')
        # print(buffer1)
        # buffer2 = unicode(buffer)
        # print(buffer)
        # print(type(buffer))
        sleep(1)

if __name__ ==  '__main__':
    ser = Serial(
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

    t = Thread(target=receiving, args=(ser,))
    t.setDaemon(True)
    t.start()
    t.join()
