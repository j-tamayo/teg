# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from cuentas.models import SgtUsuario, RolSgt
from sgt.models import Estado, Municipio, CentroInspeccion
from django.contrib.auth import authenticate, login
from django.core import serializers

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

		#print respuesta

		if respuesta:
			return Response(respuesta, status=status.HTTP_200_OK)
		else:
			respuesta['errores'] = {'causa':'No se envía nada'}
			return Response(respuesta, status=status.HTTP_500_INTERNAL_SERVER_ERROR)