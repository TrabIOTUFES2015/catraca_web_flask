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
    msg = ser.last_msg()
    while True:
        sleep(0.100)
        last_msg = ser.last_msg()
        #print msg
        # print last_msg
        if last_msg and msg != last_msg:
            msg = last_msg
            yield 'id:' + str(msg['id']) + '\n' + 'data:' + msg['msg'] + '\n\n'

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
    msg = ser.last_msg()
    while True:
        sleep(0.01)
        last_msg = ser.last_msg()
        if last_msg and msg != last_msg:
            msg = last_msg
            yield 'id:' + str(msg['id']) + '\n' + 'data:' + msg['msg'] + '\n\n'
   
               




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