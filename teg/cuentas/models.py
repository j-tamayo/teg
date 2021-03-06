# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
class SgtUsuarioManager(BaseUserManager):
	def create_user(self, correo, nombres, apellidos, password=None):
		""" Crea un usuario dado su correo, cedula, nombres y apellidos """
		if not correo:
			mensaje = u'El usuario debe poseer correo electrónico'
			raise ValueError(mensaje)

		# if not cedula:
		# 	mensaje = u'El usuario debe poseer cédula'
		# 	raise ValueError(mensaje)

		if not nombres:
			mensaje = u'El usuario debe poseer nombres'
			raise ValueError(mensaje)

		if not apellidos:
			mensaje = u'El usuario debe poseer apellidos'
			raise ValueError(mensaje)

		# if not fecha_nacimiento:
		# 	mensaje = u'EL usuario debe poseer fecha de nacimiento'
		# 	raise ValueError(mensaje)

		# if not sexo:
		# 	mensaje = u'El usuario debe poseer sexo'
		# 	raise ValueError(mensaje)

		user = self.model(
		    correo=SgtUsuarioManager.normalize_email(correo),
		    nombres=nombres,
		    apellidos=apellidos,
		)

		user.set_password(password)
		user.rol = RolSgt.objects.filter(codigo = 'admin').first()
		user.save(using=self._db)
		return user

	def create_superuser(self, correo, nombres, apellidos, password):
		""" Crea un super usuario dado su correo, cedula, nombres y apellidos """
		user = self.create_user(
		    correo=correo,
		    password=password,
		    nombres=nombres,
		    apellidos=apellidos,
		)

		user.is_admin = True
		user.rol = RolSgt.objects.filter(codigo = 'admin').first()
		user.save(using=self._db)
		return user


class SgtUsuario(AbstractBaseUser):
	apellidos = models.CharField(max_length=200)
	cedula = models.CharField(max_length=100, blank=True, null=True)
	correo = models.CharField(max_length=255, unique=True, db_index=True, error_messages={'unique':"Ya existe un usuario registrado con este correo electrónico."})
	codigo_postal = models.IntegerField(blank=True, null=True)
	direccion = models.TextField(blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	fecha_nacimiento = models.DateField(blank=True, null=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	municipio = models.ForeignKey('sgt.Municipio', blank=True, null=True)
	nombres = models.CharField(max_length=200)
	rol = models.ForeignKey('RolSgt')
	sexo = models.IntegerField(blank=True, null=True)
	telefono_local = models.CharField(max_length=100, blank=True, null=True)
	telefono_movil = models.CharField(max_length=100, blank=True, null=True)
	centro_inspeccion = models.ForeignKey('sgt.CentroInspeccion', blank=True, null=True)

	objects = SgtUsuarioManager()

	USERNAME_FIELD = 'correo'
	REQUIRED_FIELDS = ['nombres', 'apellidos', 'cedula', 'fecha_nacimiento', 'sexo']

	def get_full_name(self):
		return u'%s %s' % (self.nombres, self.apellidos)

	def get_short_name(self):
		return u'%s' % self.correo

	def is_staff(self):
		return False

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	def es_cliente(self):
		rol_cliente = RolSgt.objects.filter(codigo =  'cliente').first()
		return self.rol == rol_cliente

	def es_admin(self):
		rol_admin = RolSgt.objects.filter(codigo = 'admin').first()
		return self.rol == rol_admin

	def es_taquilla(self):
		rol_taquilla = RolSgt.objects.filter(codigo = 'taquilla').first()
		return self.rol == rol_taquilla

	def __unicode__(self):
		return u'%s - %s' % (self.correo, self.cedula)


class RolSgt(models.Model):
	nombre = models.CharField(max_length=255)
	codigo = models.CharField(max_length=100)
	descripcion = models.TextField(blank=True, null=True)
	permisos = models.ManyToManyField('Permiso')

	def __unicode__(self):
		return '%s' % self.nombre


class Permiso(models.Model):
	nombre = models.CharField(max_length=255)
	codigo = models.CharField(max_length=100)
	descripcion = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return '%s' % self.nombre