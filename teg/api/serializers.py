#from django.forms import widgets
from rest_framework import serializers
from cuentas.models import SgtUsuario
#from django.contrib.auth.models import User

class SgtUsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = SgtUsuario
		fields = ('id','password','nombres','apellidos','cedula','correo','codigo_postal','direccion','fecha_nacimiento','sexo','telefono_local','telefono_movil','municipio')

	# def create(self, validated_data):

	# 	print "h"
