from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
class SgtUsuarioManager(BaseUserManager):
	def crear_usuario(self, nombres):
		pass


class SgtUsuario(AbstractBaseUser):
	apellidos = models.CharField(max_length=200)
	cedula = models.CharField(max_length=100)
	correo = models.CharField(max_length=255)
	nombres = models.CharField(max_length=200)
	fecha_nacimiento = models.DateField()
	fecha_registro = models.DateTimeField(auto_now_add=True)
	sexo = models.IntegerField()
	telefono_local = models.CharField(max_length=100)
	telefono_movil = models.CharField(max_length=100)
	direccion = models.TextField()
	clave = models.CharField(max_length=255)