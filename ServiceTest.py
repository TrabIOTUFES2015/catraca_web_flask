__author__ = 'btoffoli'

from service import *

from unittest import *

class ServiceTest(TestCase):

    def setUp(self):
        self.service = CatracaService()

    def processarPacote1Test(self):
        self.service.processarPacote('CATRACA|2')
        self.assertTrue(len(self.service.sensores) > 0, 'Deveria já haver sensor')

        self.as





