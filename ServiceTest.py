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
        self.packageId = 0
        self.service = CatracaService()

    def __buildCatracaPackage(self, sensorId):
        self.packageId += 1
        return {'id': self.packageId, 'msg': 'CATRACA|%d' %(sensorId)}

    def __buildLeituraPackage(self, sensorId, value):
        self.packageId += 1
        return {'id': self.packageId, 'msg': 'LEITURA|%d|%d|' %(sensorId, value)}


    def testProcessarPacote1(self):
        self.service.processarPacote(self.__buildCatracaPackage(2))
        self.assertTrue(len(self.service.sensores) > 0, 'Deveria já haver sensor')

        sensor = self.service.sensores[0]
        self.assertEqual(sensor.id, int(2), 'Id do sensor deveria ser 2')

        self.service.processarPacote(self.__buildLeituraPackage(2, 300))

        firstData = sensor.lastLeitura()
        self.assertIsNotNone(firstData, 'Deveria haver leitura')

        self.assertEqual(firstData['valor'], 300, 'Valor da leitura deveria ser 300')


    


    def tearDown(self):
        pass







if __name__ == '__main__':
    mainTest()