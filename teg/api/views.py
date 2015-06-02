from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import SgtUsuarioSerializer,LoginSerializer
from cuentas.models import SgtUsuario, RolSgt
from sgt.models import Municipio
from django.contrib.auth import authenticate, login

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