# -*- encoding: utf-8 -*-
from django.test import TestCase
from sgt.models import *
import datetime

# Create your tests here.
def load_initial_data():
	estado = Estado(nombre='Estado 1')
	estado.save()
	Municipio(nombre='Municipio 1', estado = estado).save()

class CentroInspeccionTests(TestCase):

	def test_insert_centro_inspeccion(self):
		load_initial_data()
		municipio = Municipio.objects.filter().first()
		hora_apertura_manana = datetime.time(hour = 8, minute = 0)
		hora_cierre_manana = datetime.time(hour = 12, minute = 0)
		hora_apertura_tarde = datetime.time(hour = 14, minute = 0)
		hora_cierre_tarde = datetime.time(hour = 18, minute = 0)
		centro = CentroInspeccion(
			nombre = 'Centro prueba 1',
			direccion = 'Dirección de prueba',
			telefonos = '0212-213-2414',
			municipio = municipio,
			hora_apertura_manana = hora_apertura_manana,
			hora_cierre_manana = hora_cierre_manana,
			hora_apertura_tarde = hora_apertura_tarde,
			hora_cierre_tarde = hora_cierre_tarde
		)
		centro.save()
		self.assertIsNotNone(centro.pk)