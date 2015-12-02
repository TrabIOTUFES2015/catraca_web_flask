from flask import Flask, render_template, Response
from serial import *
from time import sleep
from serial_stream import SerialStream
# from flask_socketio import SocketIO

app = Flask(__name__)
app.debug = True
# socketio = SocketIO(app)
ser = None



def event_barcode():
    messageid = 0
    
    str_list = []
    while True:
        sleep(0.01)
        nextchar = ser.read(100)
        if nextchar:
            str_list.append(nextchar)
        else:
            if len(str_list) > 0:
                yield 'id:' + str(messageid) + '\n' + 'data:' + ''.join(str_list) + '\n\n'
                messageid += 1
                str_list = []

def startUsbStream():
    messageid = 0
    return SerialStream(
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
        bytesize=8, parity=PARITY_NONE, stopbits=STOPBITS_ONE
    )   


def event_barcode2():
    messageid2 = 0
    
    str_list = []
    while True:
        sleep(0.01)
        nextchar = ser.read(100)
        if nextchar:
            str_list.append(nextchar)
        else:
            if len(str_list) > 0:
                yield 'id:' + str(messageid2) + '\n' + 'data:' + ''.join(str_list) + '\n\n'
                messageid2 += 1
                str_list = []





@app.route('/debug/')
def debug():
    return render_template('debug.html')



@app.route('/barcode')
def barcode():
    newresponse = Response(event_barcode(), mimetype="text/event-stream")
    newresponse.headers.add('Access-Control-Allow-Origin', '*')
    newresponse.headers.add('Cache-Control', 'no-cache')
    return newresponse


@app.route('/debug2/')
def debug2():
    return render_template('debug.html')

@app.route('/barcode2')
def barcode2():
    newresponse = Response(event_barcode2(), mimetype="text/event-stream")
    newresponse.headers.add('Access-Control-Allow-Origin', '*')
    newresponse.headers.add('Cache-Control', 'no-cache')
    return newresponse



if __name__ == '__main__':
    ser = startUsbStream()
    app.run(port=8080, threaded=True)