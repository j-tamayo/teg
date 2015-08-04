# -*- coding: utf-8 -*-
from sgt.models import *
from openpyxl import load_workbook

def cargar_centros_desde_xls(file):
	"""Función para cargar los centros de inspección desde un archivo xls"""
	reg = {}
	wb = load_workbook(file)
	ws = wb['centros']
	print "HEEEY",ws.get_highest_row()
	for i in range(2,ws.get_highest_row()+1):
		
		reg['nombre'] = ws['A'+str(i)].value
		reg['estado'] = ws['B'+str(i)].value
		reg['municipio'] = ws['C'+str(i)].value
		reg['direccion'] = ws['D'+str(i)].value
		reg['telefonos'] = ws['E'+str(i)].value
		reg['hora_apertura_manana'] = ws['F'+str(i)].value
		reg['hora_cierre_manana'] = ws['G'+str(i)].value
		reg['hora_apertura_tarde'] = ws['H'+str(i)].value
		reg['hora_cierre_tarde'] = ws['I'+str(i)].value
		
		municipio = Municipio.objects.filter(nombre__icontains = reg['municipio'], estado__nombre__icontains = reg['estado']).first()
		existe_centro = CentroInspeccion.objects.filter(nombre = reg['nombre'], municipio = municipio).count()
		if existe_centro < 1:
			centro = CentroInspeccion(
				nombre = reg['nombre'],
				municipio = municipio,
				direccion = reg['direccion'],
				telefonos = reg['telefonos'],
				hora_apertura_manana = reg['hora_apertura_manana'],
				hora_cierre_manana = reg['hora_cierre_manana'],
				hora_apertura_tarde = reg['hora_apertura_tarde'],
				hora_cierre_tarde = reg['hora_cierre_tarde']
			)
			centro.save()
		else:
			print "Ya se agregó este centro"

	return True
		