# -*- coding: utf-8 -*-
from openpyxl import load_workbook

def cargar_centros_desde_xls(file):
	"""Función para cargar los centros de inspección desde un archivo xls"""
	wb = load_workbook(file)
	ws = wb['centros']
	print "HEEEY"
	print ws.get_highest_row()