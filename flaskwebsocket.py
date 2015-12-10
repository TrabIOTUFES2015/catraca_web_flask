from flask import Flask, render_template, Response, jsonify, request
from serial import *
from time import sleep
from serial_stream import SerialStream
from service import *

# from flask_socketio import SocketIO

app = Flask(__name__)
app.debug = True
# socketio = SocketIO(app)
ser = None
service = None




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
        baudrate=57600        
    )   



def event_barcode2():
    msg = ser.last_msg()
    while True:
        sleep(0.01)
        last_msg = ser.last_msg()
        if last_msg and msg != last_msg:
            msg = last_msg
            yield 'id:' + str(msg['id']) + '\n' + 'data:' + msg['msg'] + '\n\n'
   
               


@app.route('/sensores')
def sensores():
    sensores = service.listarSensoresLivres()
    strHtml = ""
    for s in sensores:
        strId = str(s.id)
        strHtml += "<option id=" + strId + ">TOS_NODE_ID=" + strId +"</option>"

    return strHtml

@app.route('/criarCatraca')
def criarCatraca():
    sensorId1 = request.args.get('sensorId1')
    sensorId2 = request.args.get('sensorId2')
    catraca = None

    sensor1 = next(sensor for sensor in service.sensores if sensor.id == int(sensorId1))
    sensor2 = next(sensor for sensor in service.sensores if sensor.id == int(sensorId2))
    if (sensor1 and sensor2):
        catraca = service.criarCatraca(sensor1, sensor2)

    if (catraca):
        return str(catraca)
    else:
        return 'Falha na associacao. Recarregue a pagina de associacao.'



@app.route('/catracas')
def catracas():
    catracas = service.catracas()
    strHtml = ""
    for s in catracas:
        strId = str(s.id)
        strHtml += "<option id=" + strId + ">TOS_NODE_ID=" + strId +"</option>"

    return strHtml





@app.route('/ultimasLeituras')
def ultimasLeituras():
    sensores = service.sensores
    return render_template('tabelaSensores.html', sensoresList=sensores)




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

@app.route('/')
def index():
    return render_template('index.html')
    #pass


if __name__ == '__main__':
    ser = startUsbStream()
    service = CatracaService(ser)
    app.run(port=8080, threaded=True)

    #app.view_functions['index'] = index