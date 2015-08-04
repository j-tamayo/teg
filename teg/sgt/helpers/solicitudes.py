from datetime import datetime
from sgt.models import *
import datetime

class Bloque():
	hora_inicio = datetime.time()
	hora_fin = datetime.time()
	capacidad = 0

	def __init__(self, hora_inicio, hora_fin):
		self.hora_inicio = hora_inicio
		self.hora_fin = hora_fin


def generar_horarios(centro, fecha_asistencia):
	fecha_asistencia_date = datetime.datetime.strptime(fecha_asistencia, '%Y-%m-%d').date()
	now = datetime.datetime.today()
	if now.date()>=fecha_asistencia_date and now.time() > centro.hora_apertura_manana:
		hora_inicial_manana = now.time()
	else:
		hora_inicial_manana = centro.hora_apertura_manana

	if now.date()>=fecha_asistencia_date and now.time() > centro.hora_apertura_tarde:
		hora_inicial_tarde = now.time()
	else:
		hora_inicial_tarde = centro.hora_apertura_tarde
	# hora_inicial_manana = centro.hora_apertura_manana if now < centro.hora_apertura_manana else now
	# hora_inicial_tarde = centro.hora_apertura_tarde if now < centro.hora_apertura_tarde else now
	
	if hora_inicial_manana < centro.hora_cierre_manana:
		cantidad_minutos_manana = diff_times_in_minutes(hora_inicial_manana,centro.hora_cierre_manana)
	else:
		cantidad_minutos_manana = 0

	if hora_inicial_tarde < centro.hora_cierre_tarde:
		cantidad_minutos_tarde = diff_times_in_minutes(hora_inicial_tarde,centro.hora_cierre_tarde)
	else:
		cantidad_minutos_tarde = 0

	cantidad_bloques_manana = cantidad_minutos_manana / centro.tiempo_atencion
	cantidad_bloques_tarde = cantidad_minutos_tarde / centro.tiempo_atencion
	
	lista_bloques = []
	contador_horas = hora_inicial_manana
	print "Bloq man",cantidad_bloques_manana,"bloq tard",cantidad_bloques_tarde

	for i in range(0,cantidad_bloques_manana):
		datetime_aux = datetime.datetime(2014,1,1,contador_horas.hour,contador_horas.minute)
		proxima_hora = (datetime_aux + datetime.timedelta(minutes = centro.tiempo_atencion)).time()
		bloque = Bloque(contador_horas, proxima_hora)
		cantidad_citas = NumeroOrden.objects.filter(hora_atencion = contador_horas, fecha_atencion = fecha_asistencia).count()
		bloque.capacidad = centro.peritos.filter(activo=True).count() - cantidad_citas
		lista_bloques.append(bloque)
		contador_horas = proxima_hora

	contador_horas = hora_inicial_tarde
	for i in range(0,cantidad_bloques_tarde):
		datetime_aux = datetime.datetime(2014,1,1,contador_horas.hour,contador_horas.minute)
		proxima_hora = (datetime_aux + datetime.timedelta(minutes = centro.tiempo_atencion)).time()
		bloque = Bloque(contador_horas, proxima_hora)
		cantidad_citas = NumeroOrden.objects.filter(hora_atencion = contador_horas, fecha_atencion = fecha_asistencia).count()
		bloque.capacidad = centro.peritos.filter(activo=True).count() - cantidad_citas
		lista_bloques.append(bloque)
		contador_horas = proxima_hora

	return lista_bloques
		



def diff_times_in_minutes(t1, t2):
    # caveat emptor - assumes t1 & t2 are python times, on the same day and t2 is after t1
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    return( (t2_secs - t1_secs)/60)