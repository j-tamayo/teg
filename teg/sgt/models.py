from django.db import models
from cuentas.models import SgtUsuario,RolSgt
from datetime import datetime
from django.db.models import Q
import operator

USER_MODEL = SgtUsuario

# Create your models here.
class Estado(models.Model):
	nombre = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.nombre


class Municipio(models.Model):
	nombre = models.CharField(max_length=255)
	estado = models.ForeignKey(Estado)

	def __unicode__(self):
		return u'%s' % self.nombre


class CentroInspeccion(models.Model):
	codigo = models.CharField(max_length=20)
	nombre = models.CharField(max_length=255)
	direccion = models.TextField()
	capacidad = models.IntegerField(default=0)
	telefonos = models.CharField(max_length=255)
	tiempo_atencion = models.IntegerField(default=0)
	municipio = models.ForeignKey(Municipio)
	peritos = models.ManyToManyField('Perito')
	numero_orden = models.ManyToManyField('NumeroOrden', through='ColaAtencion')
	hora_apertura_manana = models.TimeField(blank=True, null=True)
	hora_cierre_manana = models.TimeField(blank=True, null=True)
	hora_apertura_tarde = models.TimeField(blank=True, null=True)
	hora_cierre_tarde = models.TimeField(blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.nombre


class Perito(models.Model):
	apellidos = models.CharField(max_length=200)
	cedula = models.CharField(max_length=100)
	fecha_ingreso = models.DateField()
	nombres = models.CharField(max_length=200)
	sexo = models.IntegerField()
	activo = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s %s' % (self.nombres, self.apellidos)


class TipoInspeccion(models.Model):
	codigo = models.CharField(max_length=50)
	descripcion = models.TextField(blank=True,null=True)
	nombre = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.nombre


class SolicitudInspeccion(models.Model):
	centro_inspeccion = models.ForeignKey(CentroInspeccion)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_culminacion = models.DateTimeField(blank=True, null=True)
	perito = models.ForeignKey(Perito, blank=True, null=True)
	tipo_inspeccion = models.ForeignKey(TipoInspeccion)
	estatus = models.ForeignKey('Estatus')
	usuario = models.ForeignKey(USER_MODEL)

	def __unicode__(self):
		return u'%s' % self.tipo_inspeccion.nombre


class NumeroOrden(models.Model):
	asistencia = models.IntegerField(default=0)
	solicitud_inspeccion = models.ForeignKey(SolicitudInspeccion)
	codigo = models.CharField(max_length=50)
	fecha_atencion = models.DateField(blank=True, null=True)
	hora_atencion = models.TimeField(blank=True, null=True)
	estatus = models.ForeignKey('Estatus')

	def __unicode__(self):
		return u'%s' % self.codigo

	@staticmethod
	def reporte(filtros):
		condiciones = []
		fechaInicio = filtros.get('fecha_inicio', None)
		fechaFin = filtros.get('fecha_fin', None)

		numeros_orden = NumeroOrden.objects.all()
		if filtros:
			if fechaInicio and fechaFin:
				fechainicio = datetime.datetime.strptime(fechaInicio, '%d-%m-%Y')
				fechafin = datetime.datetime.strptime(fechaFin, '%d-%m-%Y')
				if fechainicio <= fechafin:
					condiciones.append(Q(solicitud_inspeccion__fecha_creacion__range=(fechainicio,fechafin)))

			numeros_orden = numeros_orden.filter(reduce(operator.and_, condiciones)).order_by('fecha')

		return numeros_orden

# MANEJO DE ENCUESTAS...

class TipoEncuesta(models.Model):
	codigo = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.descripcion


class Encuesta(models.Model):
	#codigo = models.CharField(max_length=50)
	nombre = models.CharField(max_length=255)
	preguntas = models.ManyToManyField('Pregunta')
	usuarios = models.ManyToManyField(USER_MODEL)
	descripcion = models.TextField(blank=True, null=True)
	tipo_encuesta = models.ForeignKey(TipoEncuesta, null=True)

	def __unicode__(self):
		return u'%s' % self.nombre


class TipoRespuesta(models.Model):
	codigo = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.descripcion


class Pregunta(models.Model):
	#codigo = models.CharField(max_length=50)
	enunciado = models.CharField(max_length=255)
	requerida = models.BooleanField(default=False)
	tipo_respuesta = models.ForeignKey(TipoRespuesta, null=True)
	#respuesta = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.enunciado


class ValorPosible(models.Model):
	valor = models.CharField(max_length=255)
	valor_pregunta = models.ManyToManyField('Pregunta')

	def __unicode__(self):
		return u'%s' % self.valor


class Respuesta(models.Model):
	pregunta = models.ForeignKey(Pregunta)
	usuario = models.ForeignKey(USER_MODEL, null=True)

	def __unicode__(self):
		return u'%s' % self.id


class RespuestaIndefinida(models.Model):
	respuesta = models.ForeignKey(Respuesta)
	valor_indefinido = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.valor_indefinido


class RespuestaDefinida(models.Model):
	respuesta = models.ForeignKey(Respuesta)
	valor_definido = models.ForeignKey(ValorPosible)

	def __unicode__(self):
		return u'%s' % self.valor_definido

#FIN MANEJO DE ENCUESTAS...

class SistemaOperativo(models.Model):
	nombre = models.CharField(max_length=255)
	version = models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s' % self.nombre


class ColaAtencion(models.Model):
	centro_inspeccion = models.ForeignKey(CentroInspeccion)
	numero_orden = models.ForeignKey(NumeroOrden)
	orden = models.IntegerField()


class Poliza(models.Model):
	descripcion = models.TextField(blank=True, null=True)
	numero = models.IntegerField()
	usuario = models.ForeignKey(USER_MODEL)

	def __unicode__(self):
		return u'%s' % self.numero


class Dispositivo(models.Model):
	marca = models.CharField(max_length=255)
	modelo = models.CharField(max_length=255)
	sistema_operativo = models.ForeignKey(SistemaOperativo)
	wifi = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return u'%s - %s' % (self.modelo, self.marca)


class Estatus(models.Model):
	nombre = models.CharField(max_length=255)
	codigo = models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s' % self.nombre


class Notificacion(models.Model):
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	leida = models.BooleanField(default=False)
	texto = models.TextField()
	tipo_notificacion = models.ForeignKey('TipoNotificacion')
	usuario = models.ForeignKey(USER_MODEL)

	def __unicode__(self):
		return u'%s - %s' % (self.fecha_creacion,self.texto)


class TipoNotificacion(models.Model):
	codigo = models.CharField(max_length=100)
	nombre = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.nombre