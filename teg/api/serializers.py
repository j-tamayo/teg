#from django.forms import widgets
from rest_framework import serializers
from cuentas.models import SgtUsuario
from sgt.models import *
#from django.contrib.auth.models import User

class SgtUsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = SgtUsuario
		fields = ('id','nombres','apellidos','cedula','correo','codigo_postal','direccion','fecha_nacimiento','sexo','telefono_local','telefono_movil','municipio')

	# def create(self, validated_data):

	# 	print "h"
class PolizaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poliza
		fields = ('id','cedula_cliente','fecha_inicio_vigencia','fecha_fin_vigencia','numero','usuario')


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
		fields = ('id','nombre','direccion','capacidad','telefonos','tiempo_atencion','municipio','hora_apertura_manana','hora_cierre_manana','hora_apertura_tarde','hora_cierre_tarde')


class TipoInspeccionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TipoInspeccion
		feilds = ('id','codigo','descripcion','nombre')


class SolicitudInspeccionSerializer(serializers.ModelSerializer):
	usuario = serializers.ReadOnlyField(source='usuario.id')
	estatus = serializers.ReadOnlyField(source='estatus.id')
	tipo_inspeccion = serializers.ReadOnlyField(source='tipo_inspeccion.id')
	centro_inspeccion = serializers.ReadOnlyField(source='centro_inspeccion.id')
	fecha_creacion = serializers.DateTimeField(format='%d-%m-%Y')
	fecha_creacion = serializers.DateTimeField(format='%d-%m-%Y')
	perito = serializers.SerializerMethodField('nombres_apellidos_perito')

	class Meta:
		model = SolicitudInspeccion
		fields = ('id','fecha_creacion','fecha_culminacion','perito','tipo_inspeccion','usuario','estatus','centro_inspeccion')

	def nombres_apellidos_perito(self, obj):
		if obj.perito:
			return obj.perito.nombres + ' ' + obj.perito.apellidos
		else:
			return ''


class TipoInspeccionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TipoInspeccion
		fields = ('id', 'codigo', 'descripcion', 'nombre')


class NumeroOrdenSerializer(serializers.ModelSerializer):
	# estatus = serializers.ReadOnlyField(source='estatus.id')
	solicitud_inspeccion = serializers.ReadOnlyField(source='solicitud_inspeccion.id')
	fecha_atencion = serializers.DateField(format='%d-%m-%Y')

	class Meta:
		model = NumeroOrden
		fields = ('id','asistencia','solicitud_inspeccion','codigo','fecha_atencion','hora_atencion')


class EstatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Estatus
		fields = ('id', 'nombre', 'codigo')


class TipoEncuestaSerializer(serializers.ModelSerializer):
	class Meta:
		model = TipoEncuesta
		fields = ('id', 'codigo', 'descripcion')


class TipoRespuestaSerializer(serializers.ModelSerializer):
	class Meta:
		model = TipoRespuesta
		fields = ('id', 'codigo', 'descripcion')


class TipoNotificacionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TipoNotificacion
		fields = ('id', 'codigo', 'descripcion')


class NotificacionSerializer(serializers.ModelSerializer):
	tipo_notificacion = serializers.ReadOnlyField(source='tipo_notificacion.id')
	encuesta = serializers.ReadOnlyField(source='encuesta.id')

	class Meta:
		model = Notificacion
		fields = ('id', 'mensaje', 'tipo_notificacion', 'encuesta', 'asunto')


class NotificacionUsuarioSerializer(serializers.ModelSerializer):
	notificacion = serializers.ReadOnlyField(source='notificacion.id')
	usuario = serializers.ReadOnlyField(source='usuario.id')
	fecha_creacion = serializers.DateTimeField(format='%d-%m-%Y')

	class Meta:
		model = NotificacionUsuario
		fields = ('id', 'notificacion', 'usuario', 'fecha_creacion', 'leida')


class EncuestaSerializer(serializers.ModelSerializer):
	tipo_encuesta = serializers.ReadOnlyField(source='tipo_encuesta.id')

	class Meta:
		model = Encuesta
		fields = ('id', 'descripcion', 'nombre', 'tipo_encuesta')


class PreguntaSerializer(serializers.ModelSerializer):
	tipo_respuesta = serializers.ReadOnlyField(source='tipo_respuesta.id')

	class Meta:
		model = Pregunta
		fields = ('id', 'enunciado', 'requerida', 'tipo_respuesta')


class EncuestaPreguntaSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	encuesta_id = serializers.IntegerField()
	pregunta_id = serializers.IntegerField()


class ValorPosibleSerializer(serializers.ModelSerializer):
	class Meta:
		model = ValorPosible
		fields = ('id', 'valor')


class ValorPreguntaEncuestaSerializer(serializers.ModelSerializer):
	class Meta:
		model = ValorPreguntaEncuesta
		fields = ('id', 'valor', 'pregunta', 'encuesta', 'orden')
