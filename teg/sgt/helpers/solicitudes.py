from datetime import datetime
from sgt.models import *
import datetime

# class Bloque():
# 	hora_inicio = datetime.time()
# 	hora_fin = datetime.time()
# 	capacidad = 0

# 	def __init__(self, hora_inicio, hora_fin):
# 		self.hora_inicio = hora_inicio
# 		self.hora_fin = hora_fin


def generar_horarios(centro):
	cantidad_minutos_manana = diff_times_in_minutes(centro.hora_apertura_manana,centro.hora_cierre_manana)
	cantidad_minutos_tarde = diff_times_in_hours(centro.hora_apertura_tarde,centro.hora_cierre_tarde)
	cantidad_bloques_manana = cantidad_minutos_manana / centro.tiempo_atencion
	cantidad_bloques_tarde = cantidad_minutos_tarde / centro.tiempo_atencion
	lista_bloques = []
	contador_horas = centro.hora_apertura_manana
	# for i in range(0,cantidad_bloques_manana):
	# 	proxima_hora = contador_horas + datetime.deltatime(minutes = centro.tiempo_atencion)
	# 	bloque = Bloque(contador_horas, proxima_hora)
		



def diff_times_in_minutes(t1, t2):
    # caveat emptor - assumes t1 & t2 are python times, on the same day and t2 is after t1
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    return( (t2_secs - t1_secs)/60)/60