from django.db import models
from cuentas.models import SgtUsuario,RolSgt
from datetime import datetime

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
	tiempo_empresa = models.IntegerField()

	def __unicode__(self):
		return u'%s %s' % (self.nombres, self.apellidos)


class TipoInspeccion(models.Model):
	codigo = models.CharField(max_length=50)
	descripcion = models.TextField(blank=True,null=True)
	nombre = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.nombre


class SolicitudInspeccion(models.Model):
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_culminacion = models.DateTimeField(blank=True, null=True)
	perito = models.ForeignKey(Perito, blank=True, null=True)
	tipo_inspeccion = models.ForeignKey(TipoInspeccion)
	usuario = models.ForeignKey(USER_MODEL)

	def __unicode__(self):
		return u'%s' % self.tipo_inspeccion.nombre


class NumeroOrden(models.Model):
	asistencia = models.IntegerField(default=0)
	solicitud_inspeccion = models.ForeignKey(SolicitudInspeccion)
	codigo = models.CharField(max_length=50)
	fecha_atencion = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.codigo


class Encuesta(models.Model):
	codigo = models.CharField(max_length=50)
	descripcion = models.TextField(blank=True, null=True)
	nombre = models.CharField(max_length=255)
	preguntas = models.ManyToManyField('Pregunta')
	usuarios = models.ManyToManyField(USER_MODEL)

	def __unicode__(self):
		return u'%s' % self.nombre


class Pregunta(models.Model):
	codigo = models.CharField(max_length=50)
	pregunta = models.CharField(max_length=255)
	respuesta = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.codigo


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