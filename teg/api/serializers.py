#from django.forms import widgets
from rest_framework import serializers
from cuentas.models import SgtUsuario
from sgt.models import Estado, Municipio, CentroInspeccion
#from django.contrib.auth.models import User

class SgtUsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = SgtUsuario
		fields = ('id','password','nombres','apellidos','cedula','correo','codigo_postal','direccion','fecha_nacimiento','sexo','telefono_local','telefono_movil','municipio')

	# def create(self, validated_data):

	# 	print "h"

class LoginSerializer(serializers.Serializer):
	correo = serializers.EmailField()
	password = serializers.CharField(style={'input_type': 'password'})

class EstadoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Estado
		fields = ('id','nombre')

class MunicipioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Municipio
		fields = ('id','nombre','estado')

class CentroSerializer(serializers.ModelSerializer):
	class Meta:
		model = CentroInspeccion
		fields = ('id','codigo','nombre','direccion','capacidad','telefonos','tiempo_atencion','municipio','hora_apertura','hora_cierre')