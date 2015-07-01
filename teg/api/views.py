# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from cuentas.models import SgtUsuario, RolSgt
from sgt.models import *
from django.contrib.auth import authenticate, login
from django.core import serializers
from sgt.helpers import solicitudes,dates

import json

# Create your views here.
class Usuarios(APIView):
	"""
	List all snippets, or create a new snippet.
	"""
	def get(self, request, format = None):
		usuarios = SgtUsuario.objects.all()
		serializer = SgtUsuarioSerializer(usuarios, many=True)
		return Response(serializer.data)


	def post(self, request, format = None):
		serializer = SgtUsuarioSerializer(data=request.data)
		if serializer.is_valid():
			registro = serializer.data
			rol_cliente = RolSgt.objects.get(codigo='cliente')
			registro['municipio'] = Municipio.objects.filter(id=registro['municipio']).first()
			usuario = SgtUsuario(
			    nombres = registro['nombres'],
			    apellidos = registro['apellidos'],
			    cedula = registro['cedula'],
			    municipio = registro['municipio'],
			    direccion = registro['direccion'],
			    codigo_postal = registro['codigo_postal'],
			    correo = registro['correo'],
			    fecha_nacimiento = registro['fecha_nacimiento'],
			    telefono_local = registro['telefono_local'],
			    telefono_movil = registro['telefono_movil'],
			    sexo = registro['sexo'],
			    rol = rol_cliente)

			usuario.set_password(registro['password'])
			usuario.save()
			# serializer.data['rol'] = RolSgt.objects.get(codigo='cliente')
			# usuario_aux = SgtUsuario()
			# usuario_aux.set_password(serializer.data['password'])
			# serializer.password = usuario_aux.password
			# print serializer.data
			# serializer.save()
			# print serializer.data, request.data
			#print serializer.data['password']
			#serializer.set_password(serializer.data['password'])
			#print serializer
			#serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
	"""
	List all snippets, or create a new snippet.
	"""
	def get(self, request, format = None):
		usuarios = SgtUsuario.objects.all()
		serializer = SgtUsuarioSerializer(usuarios, many=True)
		return Response(serializer.data)

	def post(self, request, format = None):
		serializer = LoginSerializer(data=request.data)
		if serializer.is_valid():
			correo = serializer.data['correo']
			password = serializer.data['password']
			print serializer.data
			usuario = authenticate(correo=correo, password=password)
			if usuario:
				user_serializer = SgtUsuarioSerializer(usuario)
				return Response(user_serializer.data, status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_404_NOT_FOUND)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Estados(APIView):
	"""
	List all snippets, or create a new snippet.
	"""
	def get(self, request, format = None):
		estados = Estado.objects.all()
		serializer = EstadoSerializer(estados, many=True)

		if serializer:
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Municipios(APIView):
	"""
	List all snippets, or create a new snippet.
	"""
	def get(self, request, format = None):
		municipios = Municipio.objects.all()
		serializer = MunicipioSerializer(municipios, many=True)

		if serializer:
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Centros(APIView):
	"""
	List all snippets, or create a new snippet.
	"""
	def get(self, request, format = None):
		centros = CentroInspeccion.objects.all()
		serializer = CentroSerializer(centros, many=True)

		if serializer:
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InitialData(APIView):
	"""
	Obtiene la data inicial necesaria para el llenado de la base de datos móvil por primera vez
	"""
	def get(self, request, format = None):
		respuesta = {}
		estados = Estado.objects.all()
		estados_serializer = EstadoSerializer(estados, many=True)
		if estados_serializer:
			respuesta['sgt_estado'] = estados_serializer.data

		municipios = Municipio.objects.all()
		municipios_serializer = MunicipioSerializer(municipios, many=True)
		if municipios_serializer:
			respuesta['sgt_municipio'] = municipios_serializer.data

		centros = CentroInspeccion.objects.all()
		centros_serializer = CentroSerializer(centros, many=True)
		if centros_serializer:
			respuesta['sgt_centroinspeccion'] = centros_serializer.data

		tipos_inspeccion = TipoInspeccion.objects.all()
		tipos_inspeccion_serializer = TipoInspeccionSerializer(tipos_inspeccion, many=True)
		if tipos_inspeccion_serializer:
			respuesta['sgt_tipoinspeccion'] = tipos_inspeccion_serializer.data

		estatus = Estatus.objects.all()
		estatus_serializer = TipoInspeccionSerializer(estatus, many=True)
		if estatus_serializer:
			respuesta['sgt_estatus'] = estatus_serializer.data

		#print respuesta

		if respuesta:
			return Response(respuesta, status=status.HTTP_200_OK)
		else:
			respuesta['errores'] = {'causa':'No se envía nada'}
			return Response(respuesta, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserInfo(APIView):
	"""
	Obtiene toda la información del Usuarios
	"""
	def get(self, request, pk, format = None):
		usuario = SgtUsuario.objects.get(id=pk)
		serializer = SgtUsuarioSerializer(usuario)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = request.data
		respuesta = {}

		if serializer:
			usuario = SgtUsuario.objects.filter(id=serializer['id'])
			if usuario:
				encuestas = Encuesta.objects.filter(usuarios = usuario)
				encuestas_serializer = EncuestaSerializer(encuestas, many=True)
				respuesta['sgt_encuesta'] = encuestas_serializer.data
				poliza = Poliza.objects.filter(usuario = usuario)
				poliza_serializer = PolizaSerializer(poliza, many=True)
				respuesta['sgt_poliza'] = poliza_serializer.data
				solicitudes = SolicitudInspeccion.objects.filter(usuario = usuario)
				solicitudes_serializer = SolicitudInspeccionSerializer(solicitudes, many=True)
				respuesta['sgt_solicitudinspeccion'] = solicitudes_serializer.data
				numero_orden = NumeroOrden.objects.filter(solicitud_inspeccion__in = solicitudes)
				numero_orden_serializer = NumeroOrdenSerializer(numero_orden, many=True)
				respuesta['sgt_numeroorden'] = numero_orden_serializer.data
				
				return Response(respuesta, status=status.HTTP_200_OK)

			else:
				raise Http404
		else:
			respuesta['errores'] = {'causa':'No se envía nada'}
			return Response(respuesta, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ObtenerCentros(APIView):
	def get(self, request, format = None):
		usuario = SgtUsuario.objects.get(id=1)
		serializer = SgtUsuarioSerializer(usuario)
		return Response(serializer.data)

	def post(self, request, format=None):
		"""" Vista que retorna en formato JSON los centros de inspección dependiendo del municipio_id recibido """
		municipio_id = request.data['municipio_id']
		estado_id = request.data['estado_id']

		print municipio_id
		print estado_id

		centros = []
		if municipio_id or estado_id:
			centros_query = CentroInspeccion.objects.filter(municipio__estado__id = estado_id)
			if municipio_id:
				centros_query = centros_query.filter(municipio__id = municipio_id)
			
			print centros_query
			#Para calcular la disponibilidad de cada centro
			for c in centros_query:
				en_cola = ColaAtencion.objects.filter(centro_inspeccion = c).count()
				c.disponibilidad = c.capacidad - en_cola
				# Para calcular la disponibilidad (Alta, media, baja y muy baja)
				if c.disponibilidad > (3 * c.capacidad)/4:
					c.etiqueta = 'Alta'
					c.etiqueta_clase = 'success'
				elif c.disponibilidad > (2 * c.capacidad)/4:
					c.etiqueta = 'Media'
					c.etiqueta_clase = 'warning'
				elif c.disponibilidad > (1 * c.capacidad)/4:
					c.etiqueta = 'Baja'
					c.etiqueta_clase = 'low'
				else:
					c.etiqueta = 'Muy baja'
					c.etiqueta_clase = 'danger'

				centros.append({
					'id': c.pk,
					'disponibilidad': c.disponibilidad,
					'etiqueta': c.etiqueta,
					'etiqueta_clase': c.etiqueta_clase
				})

			return Response(centros, status=status.HTTP_200_OK)

		else:
			respuesta = {
				'msg_error': 'No se suministró el id del estado'
			}

			return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

class Horarios(APIView):
	"""
	Obtiene los horarios disponibles para solicitar una inspección
	"""
	def get(self, request, format = None):
		usuario = SgtUsuario.objects.get(id=1)
		serializer = SgtUsuarioSerializer(usuario)
		return Response(serializer.data)

	def post(self, request, format=None):
		id_centro = request.data['id_centro']
		fecha_asistencia = request.data['fecha']
		fecha_asistencia = dates.str_to_datetime(fecha_asistencia, '%d/%m/%Y')
		id_tipo_solicitud = request.data['id_tipo_inspeccion']

		centro_inspeccion = CentroInspeccion.objects.get(id=id_centro)

		horarios = []
		bloques = solicitudes.generar_horarios(centro_inspeccion, fecha_asistencia)
		for b in bloques:
			if b.capacidad > 0:
				horarios.append({
					'value':dates.to_string(b.hora_inicio,'%H:%M'),
					'text':dates.to_string(b.hora_inicio,'%I:%M %p')
				})

		return Response(horarios, status=status.HTTP_200_OK)

		respuesta = {}
		respuesta['errores'] = {'causa':'No se envía nada'}
		return Response(respuesta, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CrearSolicitud(APIView):
	"""
	Crear una solicitud para una fecha determinada de un centro determinado a una hora determinada
	"""
	def get(self, request, format = None):
		usuario = SgtUsuario.objects.get(id=1)
		serializer = SgtUsuarioSerializer(usuario)
		return Response(serializer.data)

	def post(self, request, format=None):
		respuesta = {}

		id_centro = request.data['centro_id']
		fecha_asistencia = request.data['fecha_asistencia']
		fecha_asistencia = dates.str_to_datetime(fecha_asistencia, '%d/%m/%Y')
		fecha_asistencia = fecha_asistencia.date()
		id_tipo_solicitud = request.data['tipo']
		hora_asistencia = request.data['horario']
		hora_asistencia = dates.str_to_datetime(hora_asistencia, '%H:%M')
		hora_asistencia = hora_asistencia.time()
		usuario = SgtUsuario.objects.get(id=request.data['usuario'])

		centro_inspeccion = CentroInspeccion.objects.get(id=id_centro)
		codigo_solicitud = TipoInspeccion.objects.get(id=id_tipo_solicitud).codigo

		total_citas = NumeroOrden.objects.filter(solicitud_inspeccion__centro_inspeccion = centro_inspeccion, fecha_atencion = fecha_asistencia).count()
		cantidad_citas_bloque = NumeroOrden.objects.filter(solicitud_inspeccion__centro_inspeccion = centro_inspeccion, fecha_atencion = fecha_asistencia, hora_atencion = hora_asistencia).count()
		if cantidad_citas_bloque < centro_inspeccion.peritos.all().count():
			estatus = Estatus.objects.get(codigo='solicitud_en_proceso')
			solicitud = SolicitudInspeccion(
				centro_inspeccion = centro_inspeccion,
				tipo_inspeccion_id = id_tipo_solicitud,
				estatus = estatus,
				usuario = usuario
			)
			solicitud.save()

			print solicitud.pk
			numero = codigo_solicitud + '-' + str(total_citas + 1)
			numero_orden = NumeroOrden(
				solicitud_inspeccion = solicitud,
				codigo = numero,
				fecha_atencion = fecha_asistencia,
				hora_atencion = hora_asistencia,
				estatus = estatus
			)
			numero_orden.save()

			respuesta['solicitud'] = SolicitudInspeccionSerializer(solicitud).data
			respuesta['numero_orden'] = NumeroOrdenSerializer(numero_orden).data

			return Response(respuesta, status=status.HTTP_200_OK)

		else:
			respuesta['errores'] = {'causa':'No hay disponibilidad'}
			return Response(respuesta, status=status.HTTP_500_INTERNAL_SERVER_ERROR)