# -*- coding: utf-8 -*-
__author__ = 'btoffoli'

from service import *

from unittest import TestCase, main as mainTest

"""
Format Packet waited
CATRACA|SENSORID
LEITURA|SENSORID|LIGHTSENSOR
"""

class ServiceTest(TestCase):

    def setUp(self):
        self.service = CatracaService()

    def processarPacote1Test(self):
        self.service.processarPacote('CATRACA|2')
        self.assertTrue(len(self.service.sensores) > 0, 'Deveria já haver sensor')

        sensor = self.service.sensores[0]
        self.assertEqual(sensor.id, int(2), 'Id do sensor deveria ser 2')

        self.service.processarPacote('LEITURA|2|300')

        firstData = sensor.lastLeitura()
        self.assertIsNotNone(firstData, 'Deveria haver leitura')

        self.assertEqual(firstData['valor'], 300)







if __name__ == '__main__':
    mainTest()