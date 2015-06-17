from datetime import datetime
from sgt.models import *

# class Bloque():
# 	hora_inicio = datetime.time()
# 	hora_fin = datetime.time()
# 	capacidad = 0

# 	def __init__(self, hora_inicio, hora_fin):
# 		self.hora_inicio = hora_inicio
# 		self.hora_fin = hora_fin


def generar_horarios(centro):
	cantidad_minutos = diff_times_in_minutes(centro.hora_apertura_manana,centro.hora_cierre_manana) + diff_times_in_hours(centro.hora_apertura_tarde,centro.hora_cierre_tarde)
	cantidad_bloques = cantidad_minutos / centro.tiempo_atencion



def diff_times_in_minutes(t1, t2):
    # caveat emptor - assumes t1 & t2 are python times, on the same day and t2 is after t1
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    return( (t2_secs - t1_secs)/60)/60