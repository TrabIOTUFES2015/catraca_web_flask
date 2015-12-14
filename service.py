
from threading import Thread
from time import sleep
from collections import deque

class Catraca(object):

	"""docstring for Catraca"""
	def __init__(self, id, sensor1, sensor2):
		super(Catraca, self).__init__()
		self.id = id
		self.sensorA = sensor1
		self.sensorB = sensor2
        #self.s1Tos2 = 0
        #self.s2Tos1 = 0

	def __eq__(self, other):
		return self.id == other.id

	def __str__(self):
		return "{0} | {1} | {2}".format(self.id, self.sensorA.id, self.sensorB.id)




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
		if self.leituras:
			return self.leituras[-1]
		else:
			return None

	def __eq__(self, other):
		return self.id == other.id


class CatracaService(object):
	"""docstring for CatracaService"""



	def __init__(self, streamService=None):
		super(CatracaService, self).__init__()
		self.streamService = streamService
		self.sensores = []
		self.catracas = []
		if streamService:
			t = Thread(name='CatracaService.streamService', target=self.streamPacketService)
			t.setDaemon(True)
			t.start()
			self.streamServiceThread = t


	def processarPacote(self, pacote):
		msg = pacote['msg']
		params = msg.split('|')
		nomePacote = params[0]
		sensor_id = None
		valor = None

		if (len(params) > 1):


			if nomePacote == 'CATRACA':
				print 'Pacote configuracao'

			sensor_id = int(params[1])

			#constroi sensor para busca
			sensor = None
			for s in self.sensores:
				if s.id == sensor_id:
					sensor = s

			if not sensor:
				sensor = Sensor(id=sensor_id)
				self.sensores.append(sensor)


			if len(params) > 2 and nomePacote == 'LEITURA':
				valor = params[2]
				sensor.addLeitura(valor)





	def criarCatraca(self, sensor1, sensor2):
		# TODO check for sensors already used
		catraca = Catraca(len(self.catracas), sensor1, sensor2)
		self.catracas.append(catraca)
		return  catraca


	def listarSensoresLivres(self):
		sensoresEmCatracas = [sensor for sensorTuple in  (map(lambda catraca: (catraca.sensorA, catraca.sensorB), self.catracas)) for sensor in sensorTuple]
		sensoresNaoUtilizados = [sensor for sensor in self.sensores if sensor not in sensoresEmCatracas]
		return sensoresNaoUtilizados


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


