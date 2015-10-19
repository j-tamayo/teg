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
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

import json
import random
import string
import threading

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
		data = request.data
		mensaje = {}

		#Validando existencia del correo electronico...
		check_correo = SgtUsuario.objects.filter(correo=data['correo']).first()
		if check_correo:
			mensaje['mensaje'] = 'El correo ingresado ya se encuentra registrado'
			return Response(mensaje, status=status.HTTP_400_BAD_REQUEST)

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
			    sexo = registro['sexo'] if registro['sexo'] == 0 or registro['sexo'] == 1 else None,
			    rol = rol_cliente)

			usuario.set_password(data['password'])
			usuario.save()
			#Asignar póliza, si existe
			poliza = Poliza.objects.filter(cedula_cliente = usuario.cedula).first()
			if poliza:
			    poliza.usuario = usuario
			    poliza.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuariosEdit(APIView):
	"""
	Editar información de usuario
	"""
	def post(self, request, format = None):
		mensaje = {}
		data = request.data
		print "HAHtohjerthr0eihtyeirhh"
		if data: 	#queda pendiente validar los password...
			data['municipio'] = Municipio.objects.filter(id=data['municipio']).first()
			usuario = SgtUsuario.objects.filter(id=data['usuario']).first()

			if usuario.nombres != data['nombres']:
				usuario.nombres = data['nombres']

			if usuario.apellidos != data['apellidos']:
				usuario.apellidos = data['apellidos']

			if usuario.cedula != data['cedula']:
				usuario.cedula = data['cedula']

			if usuario.municipio.id != data['municipio'].id:
				usuario.municipio = data['municipio']

			if usuario.direccion != data['direccion']:
				usuario.direccion = data['direccion']

			if usuario.codigo_postal != data['codigo_postal']:
				usuario.codigo_postal = data['codigo_postal'] if data['codigo_postal'] else None
 			
 			if usuario.correo != data['correo']:
 				check_correo = SgtUsuario.objects.filter(correo=data['correo']).first()
				if check_correo:
					mensaje['mensaje'] = 'El correo ingresado ya se encuentra registrado'
					return Response(mensaje, status=status.HTTP_400_BAD_REQUEST)
				else:
					usuario.correo = data['correo']

			if usuario.fecha_nacimiento != data['fecha_nacimiento']:
				usuario.fecha_nacimiento = data['fecha_nacimiento']

			if usuario.telefono_local != data['telefono_local']:
				usuario.telefono_local = data['telefono_local']

			if usuario.telefono_movil != data['telefono_movil']:
				usuario.telefono_movil = data['telefono_movil']

			if data['sexo'] == '0' or data['sexo'] == '1':
				if usuario.sexo != data['sexo']:
					usuario.sexo = data['sexo']

			usuario.set_password(data['password'])
			usuario.save()

			mensaje['mensaje'] = 'Se han actualizado los datos del perfil exitosamente'
			resp_status = status.HTTP_200_OK
		else:
			mensaje['mensaje'] = 'No se proporcionaron los datos necesarios para realizar esta acción'
			resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR

		return Response(mensaje, status=resp_status)


class LoginUser(APIView):
	"""
	List all snippets, or create a new snippet.
	"""
	def post(self, request, format = None):
		serializer = LoginSerializer(data=request.data)
		if serializer.is_valid():
			correo = serializer.data['correo']
			password = serializer.data['password']
			usuario = authenticate(correo=correo, password=password)
			if usuario and usuario.es_cliente():
				user_serializer = SgtUsuarioSerializer(usuario)
				return Response(user_serializer.data, status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_404_NOT_FOUND)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InitialData(APIView):
	"""
	Obtiene la data inicial necesaria para el llenado de la base de datos móvil por primera vez
	"""
	def get(self, request, format = None):
		respuesta = {}
		data = []

		estados = Estado.objects.all()
		estados_serializer = EstadoSerializer(estados, many=True)
		if estados_serializer:
			#respuesta['sgt_estado'] = estados_serializer.data
			data.append({'sgt_estado': estados_serializer.data})

		municipios = Municipio.objects.all()
		municipios_serializer = MunicipioSerializer(municipios, many=True)
		if municipios_serializer:
			#respuesta['sgt_municipio'] = municipios_serializer.data
			data.append({'sgt_municipio': municipios_serializer.data})

		centros = CentroInspeccion.objects.all()
		centros_serializer = CentroSerializer(centros, many=True)
		if centros_serializer:
			#respuesta['sgt_centroinspeccion'] = centros_serializer.data
			data.append({'sgt_centroinspeccion': centros_serializer.data})

		tipos_inspeccion = TipoInspeccion.objects.all()
		tipos_inspeccion_serializer = TipoInspeccionSerializer(tipos_inspeccion, many=True)
		if tipos_inspeccion_serializer:
			respuesta['sgt_tipoinspeccion'] = tipos_inspeccion_serializer.data
			data.append({'sgt_tipoinspeccion': tipos_inspeccion_serializer.data})

		estatus = Estatus.objects.all()
		estatus_serializer = TipoInspeccionSerializer(estatus, many=True)
		if estatus_serializer:
			#respuesta['sgt_estatus'] = estatus_serializer.data
			data.append({'sgt_estatus': estatus_serializer.data})

		tipo_encuesta = TipoEncuesta.objects.all()
		tipo_encuesta_serializer = TipoEncuestaSerializer(tipo_encuesta, many=True)
		if tipo_encuesta_serializer:
			#respuesta['sgt_tipoencuesta'] = tipo_encuesta_serializer.data
			data.append({'sgt_tipoencuesta': tipo_encuesta_serializer.data})

		tipo_respuesta = TipoRespuesta.objects.all()
		tipo_respuesta_serializer = TipoRespuestaSerializer(tipo_respuesta, many=True)
		if tipo_respuesta_serializer:
			#respuesta['sgt_tiporespuesta'] = tipo_respuesta_serializer.data
			data.append({'sgt_tiporespuesta': tipo_respuesta_serializer.data})

		tipo_notificacion = TipoNotificacion.objects.all()
		tipo_notificacion_serializer = TipoNotificacionSerializer(tipo_notificacion, many=True)
		if tipo_notificacion_serializer:
			#respuesta['sgt_tiponotificacion'] = tipo_notificacion_serializer.data
			data.append({'sgt_tiponotificacion': tipo_notificacion_serializer.data})

		# fecha_no_laborable = FechaNoLaborable.objects.all()
		# fecha_no_laborable_serializer = FechaNoLaborableSerializer(fecha_no_laborable, many=True)
		# if fecha_no_laborable_serializer:
		# 	data.append({'sgt_fechanolaborable': fecha_no_laborable_serializer.data})

		# centros_fechas_serializer = []
		# for c in centros:
		# 	centros_fechas = c.fechas_no_laborables.through.objects.filter(centroinspeccion_id=c.id, fechanolaborable_id__in=c.fechas_no_laborables.values_list('id', flat=True))
		# 	print centros_fechas
		# 	centros_fechas_serializer += CentroInspFechasNoLabSerializer(centros_fechas, many=True).data
		
		# if centros_fechas_serializer:
		# 	data.append({'sgt_centroinspeccion_fechas_no_laborables': centros_fechas_serializer})

		if data:
			return Response(data, status=status.HTTP_200_OK)
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
		data = []

		if serializer:
			usuario = SgtUsuario.objects.filter(id=serializer['id']).first()
			notificacion_usuario = NotificacionUsuario.objects.filter(usuario__id=serializer['id'], borrada=False)
			if usuario:
				
				poliza = Poliza.objects.filter(usuario=usuario).first()
				if poliza:
					poliza_serializer = PolizaSerializer(poliza)
					print poliza_serializer
					data.append({'sgt_poliza': [poliza_serializer.data]})
				
				solicitudes = SolicitudInspeccion.objects.filter(usuario=usuario, borrada=False)
				solicitudes_serializer = SolicitudInspeccionSerializer(solicitudes, many=True)
				data.append({'sgt_solicitudinspeccion': solicitudes_serializer.data})
				#respuesta['sgt_solicitudinspeccion'] = solicitudes_serializer.data
				numero_orden = NumeroOrden.objects.filter(solicitud_inspeccion__in = solicitudes)
				numero_orden_serializer = NumeroOrdenSerializer(numero_orden, many=True)
				data.append({'sgt_numeroorden': numero_orden_serializer.data})
				#respuesta['sgt_numeroorden'] = numero_orden_serializer.data
				notificacion = Notificacion.objects.filter(id__in=notificacion_usuario.values_list('notificacion_id', flat=True))
				notificacion_serializer = NotificacionSerializer(notificacion, many=True)
				data.append({'sgt_notificacion': notificacion_serializer.data})
				#respuesta['sgt_notificacion'] = notificacion_serializer.data
				notificacion_usuario_serializer = NotificacionUsuarioSerializer(notificacion_usuario, many=True)
				data.append({'sgt_notificacionusuario': notificacion_usuario_serializer.data})
				#respuesta['sgt_notificacionusuario'] = notificacion_usuario_serializer.data
				encuestas = Encuesta.objects.filter(id__in=notificacion.exclude(encuesta=None).values_list('encuesta_id', flat=True))
				encuestas_serializer = EncuestaSerializer(encuestas, many=True)
				data.append({'sgt_encuesta': encuestas_serializer.data})

				preguntas = Pregunta.objects.filter(id__in=encuestas.values_list('preguntas', flat=True))
				preguntas_serializer = PreguntaSerializer(preguntas, many=True)
				data.append({'sgt_pregunta': preguntas_serializer.data})

				encuestas_preguntas_serializer = []
				for e in encuestas:
					encuestas_preguntas = e.preguntas.through.objects.filter(encuesta_id=e.id, pregunta_id__in=e.preguntas.values_list('id', flat=True))
					encuestas_preguntas_serializer += EncuestaPreguntaSerializer(encuestas_preguntas, many=True).data
				data.append({'sgt_encuesta_preguntas': encuestas_preguntas_serializer})

				preguntas_aux = preguntas.exclude(tipo_respuesta__codigo='RESP_INDEF')
				encuestas_aux = encuestas.filter(preguntas__in=preguntas_aux)
				valor_pregunta_encuesta = ValorPreguntaEncuesta.objects.filter(encuesta__in=encuestas_aux, pregunta__in=preguntas_aux)
				valor_pregunta_encuesta_serializer = ValorPreguntaEncuestaSerializer(valor_pregunta_encuesta, many=True)

				valores = ValorPosible.objects.filter(id__in=valor_pregunta_encuesta.values_list('valor', flat=True))
				valores_serializer = ValorPosibleSerializer(valores, many=True)

				data.append({'sgt_valorposible': valores_serializer.data})
				data.append({'sgt_valorpreguntaencuesta': valor_pregunta_encuesta_serializer.data})
				
				return Response(data, status=status.HTTP_200_OK)

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
		fecha_asistencia = request.data.get('fecha_asistencia', datetime.now().date().strftime('%d/%m/%Y'))
		fecha_asistencia = datetime.strptime(fecha_asistencia, '%d/%m/%Y')

		centros = []
		if municipio_id or estado_id:
			centros_query = CentroInspeccion.objects.filter(municipio__estado__id = estado_id)
			if municipio_id:
				centros_query = centros_query.filter(municipio__id = municipio_id)
			
			#Para calcular la disponibilidad de cada centro
			for c in centros_query:
				en_cola = NumeroOrden.objects.filter(fecha_atencion = fecha_asistencia).count()
				capacidad = solicitudes.calcular_capacidad_centro(c)
				c.disponibilidad = capacidad - en_cola
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
		fecha_asistencia = dates.convert(fecha_asistencia, '%d/%m/%Y', '%Y-%m-%d')
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

		# respuesta = {}
		# respuesta['errores'] = {'causa':'No se envía nada'}
		# return Response(respuesta, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
		data = []

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

			numero = codigo_solicitud + '-' + str(total_citas + 1)
			numero_orden = NumeroOrden(
				solicitud_inspeccion = solicitud,
				fecha_atencion = fecha_asistencia,
				hora_atencion = hora_asistencia
			)
			numero_orden.save()
			numero_orden.codigo = numero_orden.pk
			numero_orden.save()

			#data.append({'sgt_solicitudinspeccion': [SolicitudInspeccionSerializer(solicitud).data]})
			#respuesta['sgt_solicitudinspeccion'] = [SolicitudInspeccionSerializer(solicitud).data]
			#data.append({'sgt_numeroorden': [NumeroOrdenSerializer(numero_orden).data]})
			#respuesta['sgt_numeroorden'] = [NumeroOrdenSerializer(numero_orden).data]
			#return Response(data, status=status.HTTP_200_OK)

			respuesta['mensaje'] = {'contenido':'Solicitud creada exitosamente'}
			resp_status = status.HTTP_200_OK
		else:
			respuesta['errores'] = {'causa':'No hay disponibilidad'}
			resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR
		
		return Response(respuesta, status=resp_status)


class MarcarNotificacion(APIView):
	"""
	Marcar notidicaciones leidas o borradas
	"""
	def post(self, request, format=None):
		respuesta = {}
		id_notificacion_usuario = request.data['notificacion_usuario_id']
		flag_marca = request.data['flag_marca']

		if id_notificacion_usuario and flag_marca:
			notificacion_usuario = NotificacionUsuario.objects.get(id=id_notificacion_usuario)

			if flag_marca == '1':
				notificacion_usuario.leida = True
			elif flag_marca == '2':
				notificacion_usuario.borrada = True

			notificacion_usuario.save()

			respuesta['mensaje'] = 'Notificación marcada de manera exitosa'
			resp_status = status.HTTP_200_OK
		else:
			respuesta['mensaje'] = 'No se proporcionó el id de la notificación'
			resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR

		return Response(respuesta, status=resp_status)


class MarcarSolicitud(APIView):
	"""
	Marcar solicitudes borradas
	"""
	def post(self, request, format=None):
		respuesta = {}
		solicitud_id = request.data['solicitud_id']

		if solicitud_id:
			solicitud = SolicitudInspeccion.objects.get(id=solicitud_id)
			solicitud.borrada = True
			if solicitud.estatus.codigo == 'solicitud_en_proceso':
				solicitud.estatus = Estatus.objects.get(codigo = 'solicitud_cancelada')

			solicitud.save()

			respuesta['mensaje'] = 'Solicitud marcada de manera exitosa'
			resp_status = status.HTTP_200_OK
		else:
			respuesta['mensaje'] = 'No se proporcionó el id de la solicitud'
			resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR

		return Response(respuesta, status=resp_status)


class GuardarRespuestasEncuesta(APIView):
	"""
	Vista encargada de guardar las respuestas de los usuarios con relación a las encuestas que reciben
	"""
	def post(self, request, format=None):
		mensaje = {}
		data = request.data

		if data:
			usuario_id = data['usuario']
			usuario = SgtUsuario.objects.get(id=usuario_id)
			encuesta_id = data['encuesta']
			encuesta = Encuesta.objects.get(id=encuesta_id)
			notificacion_usuario_id = data['notificacion_usuario']
			notificacion_usuario = NotificacionUsuario.objects.get(id=notificacion_usuario_id)

			total_preguntas = data['total_preguntas']
			for index in range(int(total_preguntas)):
				aux = 'pregunta_' + str(index + 1)
				pregunta_id = data[aux]
				pregunta = Pregunta.objects.get(pk=pregunta_id)
				tipo_respuesta = pregunta.tipo_respuesta.codigo
				respuesta = Respuesta(encuesta=encuesta, pregunta=pregunta, usuario=usuario, notificacion_usuario=notificacion_usuario)
				respuesta.save()

				if tipo_respuesta == "RESP_DEF":
					aux = 'respuesta_def_' + pregunta_id
					valor_def_id = data[aux]
					valor_def = ValorPosible.objects.get(id=valor_def_id)
					respuesta_definida = RespuestaDefinida(respuesta=respuesta, valor_definido=valor_def)
					respuesta_definida.save()

				elif tipo_respuesta == "RESP_INDEF":
					aux = 'respuesta_indef_' + pregunta_id
					valor_indef = data[aux]
					respuesta_indefinida = RespuestaIndefinida(respuesta=respuesta, valor_indefinido=valor_indef)
					respuesta_indefinida.save()

			notificacion_usuario.borrada = True
			notificacion_usuario.encuesta_respondida = True
			notificacion_usuario.save()

			mensaje['mensaje'] = 'Respuestas guardadas de manera exitosa'
			resp_status = status.HTTP_200_OK
		else:
			mensaje['mensaje'] = 'No se proporcioron las respuestas solicitadas'
			resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR


		return Response(mensaje, status=resp_status)


class GuardarReclamo(APIView):
	"""
	Vista encargada de registrar los reclamos de los clientes
	"""
	def post(self, request, format=None):
		mensaje = {}
		data = request.data

		if data:
			usuario = SgtUsuario.objects.get(id=data['usuario'])
			reclamo = Reclamo(usuario=usuario, motivo=data['motivo'], contenido=data['contenido'])
			reclamo.save()

			mensaje['mensaje'] = 'Reclamo enviado de manera exitosa'
			resp_status = status.HTTP_200_OK
		else:
			mensaje['mensaje'] = 'No se proporcionaron los datos solicitados'
			resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR

		return Response(mensaje, status=resp_status)


class RecuperarClave(APIView):
	"""
	Vista encargada recuperar contraseñas
	"""
	def correoRecuperacion(self, contenido, correo):
	    threadCorreo = threading.Thread(
	        name = 'thread_correo',
	        target = self.enviarCorreoOlvidoClave,
	        args = (
	            u'[SGT] Recuperación de Contraseña - SISGETICKET', 
	            contenido,
	            [correo],
	            settings.EMAIL_HOST_USER,
	        )
	    )
	    threadCorreo.start()

	def enviarCorreoOlvidoClave(self, titulo, contenido, receptor, emisor):
	    funciona = False
	    i = 0
	    while i < 3 and funciona == False:
	        i += 1
	        try:
	            msg = EmailMultiAlternatives(titulo, contenido, emisor, receptor)
	            msg.attach_alternative(contenido, "text/html")           
	            msg.send()
	            funciona = True
	        except Exception, e:
	            print '=======>error enviar correo<========='
	            print e
	            continue

	def post(self, request, format=None):
		mensaje = {}
		data = request.data

		if data:
			correo = data['correo']
			
			# Se asigna una clave temporal
			clave_temporal = ''.join(random.choice(string.ascii_letters) for i in range(6))

			correoTemplate = get_template('correo/recuperar_clave.html')
			usuario = SgtUsuario.objects.filter(correo=correo).first()
			#Se le asigna la clave temporal al usuario
			usuario.set_password(clave_temporal)
			usuario.save()

			context = Context({
				'dominio': request.META['HTTP_HOST'],
				'clave_temporal': clave_temporal,
				'usuario': usuario
			})

			contenidoHtmlCorreo = correoTemplate.render(context)
			self.correoRecuperacion(contenidoHtmlCorreo, correo)

			mensaje['clave_temporal'] = clave_temporal
			mensaje['mensaje'] = 'Se ha enviado un correo a la dirección suministrada'
			resp_status = status.HTTP_200_OK
		else:
			mensaje['mensaje'] = 'No se proporcionó el correo electrónico para la recuperación de la contraseña'
			resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR

		return Response(mensaje, status=resp_status)

