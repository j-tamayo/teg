from django.db import models

# Create your models here.
class Estado(models.Model):
	nombre = models.CharField(max_length=255)

	def __unicode__(self):
		return '%s' % self.nombre


class Municipio(models.Model):
	nombre = models.CharField(max_length=255)
	estado = models.ForeignKey(Estado)

	def __unicode__(self):
		return '%s' % self.nombre


class CentroInspeccion(models.Model):
	nombre = models.CharField(max_length=255)
	direccion = models.TextField()
	municipio = models.ForeignKey(Municipio)

	def __unicode__(self):
		return '%s' % self.nombre