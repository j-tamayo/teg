from datetime import datetime

def to_string(fecha, formato):
	return fecha.strftime(formato)

def convert(fecha, formato_origen, formato_destino):
	fecha = datetime.strptime(fecha, formato_origen)
	return fecha.strftime(formato_destino)