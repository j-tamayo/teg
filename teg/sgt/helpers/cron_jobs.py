from datetime import datetime
from mipt.models import *
from cuentas.models import *

def verificacion_diaria_solicitudes():
	now = datetime.now()
	numeros_orden = NumeroOrden.objects.filter(fecha_atencion = now.date(), asistencia=False)
	for numero in numeros_orden:
		tipo_notificacion = TipoNotificacion.objects.get(codigo='no_asistencia')
		notificacion = Notificacion(
			texto = 'Usted ha faltado a la cita programada, por favor llene la encuesta indicando los motivos',
			tipo_notificacion = tipo_notificacion, 
			usuario = numero.solicitud_inspeccion.usuario,
		)
		notificacion.save()