
from threading import Thread
from time import sleep
from collections import deque

class Catraca(object):

	__slots__ = ['name', 'sensorAId', 'sensorBId']

	def ___init__(self, name, sensor1, sensor2):
		self.name = name
		self.sensorAId = sensorAId
		self.sensorBId = sensorBId


class Sensor(object):
	"""docstring for Sensor"""
	def __init__(self, id):
		super(Sensor, self).__init__()		
		self.leituras = deque(maxlen=4)
		self.pacotePendente = False
		self.id = id
		

	def addLeitura(self, valor):
		from datetime import datetime
		self.pacotePendente = True
		leitura = {'id': len(self.leituras), 'valor': int(valor), 'dataHora': datetime.now()}
		self.leituras.append(leitura)
		return leitura

	def lastLeitura(self):
		return self.leituras[-1]


class CatracaService(object):
	"""docstring for CatracaService"""



	def __init__(self, streamService):
		super(CatracaService, self).__init__()
		self.streamService = streamService
		self.sensores = []
		self.catracas = []
		t = Thread(name='CatracaService.streamService', target=self.streamPacketService)
		t.setDaemon(True)
		t.start()
		self.streamServiceThread = t


	def processarPacote(self, pacote):
		msg = pacote['msg']
		params = msg.split('|')
		nomePacote = params[0]
		sensorId = None
		valor = None

		if (len(params) > 1):


			if nomePacote == 'CATRACA':
				print 'Pacote configuracao'

			sensorId = int(params[1])

			#constroi sensor para busca
			sensor = None
			for s in self.sensores:
				if s.id == sensorId:
					sensor = s

			if not sensor:
				sensor = Sensor(id=sensorId)
				self.sensores.append(sensor)


			if len(params) > 3 and nomePacote == 'LEITURA':
				valor = params[2]
				sensor.addLeitura(valor)








	def listarSensores(self):
		return self.sensores






	def streamPacketService(self):
		msg = self.streamService.last_msg()
		while True:
		    sleep(0.01)
		    last_msg = self.streamService.last_msg() 
		    #print msg
		    # print last_msg
		    if last_msg and msg != last_msg:
		        msg = last_msg
		        self.processarPacote(msg)


