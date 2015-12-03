from collections import deque

class Catraca(object):

	__slots__ = ['name', 'sensorAId', 'sensorBId']

	def ___init__(self, name, sensor1, sensor2):
		self.name = name
		self.sensorAId = sensorAId
		self.sensorBId = sensorBId


class Sensor(object):
	"""docstring for Sensor"""
	def __init__(self, arg):
		super(Sensor, self).__init__()
		self.arg = arg
		self.leituras = deque(maxlen=4)
		self.pacotePendente = false
		

	def addLeitura(self, leitura):
		self.pacotePendente = true
		self.leituras.append(leitura)
		return leitura

	def lastLeitura():
		return self.leituras[-1]



