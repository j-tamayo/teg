# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from sgt.models import *
from sgt.forms import *
from sgt.helpers import solicitudes,dates
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from cuentas import forms as CuentasForm
from cuentas.models import *

import json

# Create your views here.
class ObtenerMunicipios(View):
	def get(self, request, *args, **kwargs):
		"""" Vista que retorna en formato JSON los municipios dependiendo del estado_id recibido """
		estado_id = kwargs['estado_id']
		if estado_id:
			municipios = Municipio.objects.filter(estado__id = estado_id)
			# Para obtener los municipios que tengan asociado al menos un centro de inspeccion
			if request.GET.get('con_centro', None):
				centros = CentroInspeccion.objects.filter(municipio__estado__id = estado_id)
				municipios = municipios.filter(centroinspeccion = centros).distinct('id')

			municipios = serializers.serialize('json', municipios)

			return HttpResponse(
				municipios,
				content_type="application/json"
			)

		else:
			respuesta = {
				'msg_error': 'No se suministró el id del estado'
			}

			return HttpResponse(
			    json.dumps(respuesta),
			    content_type="application/json"
			)


class ObtenerCentroInspeccion(View):
	def get(self, request, *args, **kwargs):
		"""" Vista que retorna en formato JSON los centros de inspección dependiendo del municipio_id recibido """
		municipio_id = request.GET.get('municipio_id', None)
		estado_id = request.GET.get('estado_id', None)
		centros = []
		if municipio_id or estado_id:
			if municipio_id:
				centros_query = CentroInspeccion.objects.filter(municipio__id = municipio_id)
			else:
				centros_query = CentroInspeccion.objects.filter(municipio__estado__id = estado_id)
			
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
					'pk': c.pk,
					'nombre': c.nombre,
					'direccion': c.direccion,
					'disponibilidad': c.disponibilidad,
					'etiqueta': c.etiqueta,
					'etiqueta_clase': c.etiqueta_clase
				})

			centros = json.dumps(centros)

			return HttpResponse(
				centros,
				content_type="application/json"
			)

		else:
			respuesta = {
				'msg_error': 'No se suministró el id del estado'
			}

			return HttpResponse(
			    json.dumps(respuesta),
			    content_type="application/json"
			)


class GenerarNumeroOrden(View):
	def get(self, request, *args, **kwargs):
		centro_id = kwargs['centro_id']
		print centro_id
		centro_inspeccion = CentroInspeccion.objects.get(id=centro_id)
		fecha_asistencia = request.GET.get('fecha_asistencia', None)

		horarios = []
		
		centro = []
		en_cola = ColaAtencion.objects.filter(centro_inspeccion = centro_inspeccion).count()
		centro_inspeccion.disponibilidad = centro_inspeccion.capacidad - en_cola
		# Para calcular la disponibilidad (Alta, media, baja y muy baja)
		if centro_inspeccion.disponibilidad > (3 * centro_inspeccion.capacidad)/4:
			centro_inspeccion.etiqueta = 'Alta'
			centro_inspeccion.etiqueta_clase = 'success'
		elif centro_inspeccion.disponibilidad > (2 * centro_inspeccion.capacidad)/4:
			centro_inspeccion.etiqueta = 'Media'
			centro_inspeccion.etiqueta_clase = 'warning'
		elif centro_inspeccion.disponibilidad > (1 * centro_inspeccion.capacidad)/4:
			centro_inspeccion.etiqueta = 'Baja'
			centro_inspeccion.etiqueta_clase = 'low'
		else:
			centro_inspeccion.etiqueta = 'Muy baja'
			centro_inspeccion.etiqueta_clase = 'danger'

		fecha_asistencia = dates.convert(fecha_asistencia, '%m/%d/%Y', '%Y-%m-%d')
		#Falta calcular Informacion para generar numero de orden y hora de asistencia...
		horarios = []
		bloques = solicitudes.generar_horarios(centro_inspeccion, fecha_asistencia)
		for b in bloques:
			if b.capacidad > 0:
				horarios.append({
					'value':dates.to_string(b.hora_inicio,'%H:%M'),
					'text':dates.to_string(b.hora_inicio,'%I:%M %p')
				})

		centro.append({
			'nombre': centro_inspeccion.nombre,
			'estado': centro_inspeccion.municipio.estado.nombre,
			'municipio': centro_inspeccion.municipio.nombre,
			'horarios': horarios,
			#'fecha_asistencia': ,
			#'numer_orden': ,
			#'hora_asistencia':
		})
		centro = json.dumps(centro)
		

		return HttpResponse(
			centro,
			content_type="application/json"
		)


class CrearSolicitudInspeccion(View):
	def dispatch(self, *args, **kwargs):
		return super(CrearSolicitudInspeccion, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		estado_id = request.GET.get('estado', None)
		tipo_solicitudes = TipoInspeccion.objects.all()
		centros = CentroInspeccion.objects.all()
		municipios = Municipio.objects.filter(estado__id = estado_id)

		if estado_id:
			aux = centros.filter(municipio__estado__id = estado_id)
			if aux:
				centros = aux

		#Para calcular la disponibilidad de cada centro
		for c in centros:
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

		form = SolicitudInspeccionForm(request.GET)

		context = {
		    'centros': centros,
		    'form': form,
		    'municipios': municipios,
		    'tipo_solicitudes': tipo_solicitudes,
		}

		return render(request,'crear_solicitud.html', context)

	def post(self, request, *args, **kwargs):
		# form = SolicitudInspeccionForm(request.GET)
		# if form.is_valid():
		# 	datos = form.cleaned_data
		respuesta = {}
		usuario = request.user

		centro_id = request.POST.get('centro',None)
		centro_inspeccion = CentroInspeccion.objects.filter(id=centro_id).first()
		fecha_asistencia = request.POST.get('fecha_asistencia', None)
		fecha_asistencia = dates.str_to_datetime(fecha_asistencia, '%m/%d/%Y')
		fecha_asistencia = fecha_asistencia.date()
		hora_asistencia = request.POST.get('hora_asistencia', None)
		hora_asistencia = dates.str_to_datetime(hora_asistencia, '%H:%M')
		hora_asistencia = hora_asistencia.time()
		tipo_inspeccion = request.POST.get('tipo_inspeccion', None)
	
		if centro_inspeccion and fecha_asistencia and hora_asistencia and tipo_inspeccion:
			cantidad_citas = NumeroOrden.objects.filter(solicitud_inspeccion__centro_inspeccion = centro_inspeccion, fecha_atencion = fecha_asistencia, hora_atencion = hora_asistencia).count()
			if cantidad_citas < centro_inspeccion.peritos.all().count():
				estatus = Estatus.objects.get(codigo='solicitud_en_proceso')
				
				solicitud = SolicitudInspeccion(
					centro_inspeccion = centro_inspeccion,
					tipo_inspeccion_id = tipo_inspeccion,
					estatus = estatus,
					usuario = usuario
				)
				solicitud.save()

				numero_orden = NumeroOrden(
					solicitud_inspeccion = solicitud,
					codigo = 'XYZ',
					fecha_atencion = fecha_asistencia,
					hora_atencion = hora_asistencia,
					estatus = estatus
				)
				numero_orden.save()

				respuesta['solicitud'] = {
					'tipo_solicitud': solicitud.tipo_inspeccion.nombre,
					'numero_orden': numero_orden.codigo,
					'estatus': solicitud.estatus.nombre,
				}

				respuesta['resultado'] = 0

				return HttpResponse(
				    json.dumps(respuesta),
				    content_type="application/json"
				)

			else:
				respuesta['resultado'] = 1
				respuesta['error_msg'] = 'Ya no quedan cupos disponibles'

				return HttpResponse(
				    json.dumps(respuesta),
				    content_type="application/json"
				)



class BandejaCliente(View):
	def dispatch(self, *args, **kwargs):
		return super(BandejaCliente, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que maneja la bandeja del usuario común """
		usuario = request.user
		tipo_solicitudes = TipoInspeccion.objects.all()
		form = SolicitudInspeccionForm(request.POST)
		poliza = Poliza.objects.filter(usuario = usuario).first()
		solicitudes = SolicitudInspeccion.objects.filter()

		for s in solicitudes:
			s.numero_orden = NumeroOrden.objects.filter(solicitud_inspeccion = s).first()

		context = {
		    'usuario': usuario,
		    'tipo_solicitudes': tipo_solicitudes,
		    'form': form,
		    'poliza': poliza,
		    'solicitudes': solicitudes,
		}

		return render(request,'cuentas/perfil_cliente.html', context)


class AdminBandejaCentros(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminBandejaCentros, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que lista los centros de inspección al administrador """
		usuario = request.user
		print "ARGS", args
		print "KWARGS", kwargs
		centros = CentroInspeccion.objects.all()

		# Provide Paginator with the request object for complete querystring generation
		paginator = Paginator(centros, 10, request=request)
		try:
			page = request.GET.get('page', 1)
			centros = paginator.page(page)
		except PageNotAnInteger:
			centros = paginator.page(1)
			page = 0
		except EmptyPage:
			centros = paginator.page(paginator.num_pages)
		
		context = {
			'admin': True,
			'centros': centros,
			'seccion_centros': True,
			'usuario': usuario,
		}

		return render(request, 'admin/bandeja_centros.html', context)


class AdminAgregarCentro(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminAgregarCentro, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Despliega el formulario para crear un centro de inspección"""
		usuario = request.user

		form = CentroInspeccionForm()
		estados = Estado.objects.all()
		peritos = Perito.objects.all()

		context = {
			'admin': True,
			'form': form,
			'estados': estados,
			'peritos': peritos,
			'seccion_centros': True,
			'usuario': usuario,
		}

		return render(request, 'admin/crear_centro.html', context)

	def post(self, request, *args, **kwargs):
		"""Crea el centro de inspección"""
		usuario = request.user

		estados = Estado.objects.all()
		peritos = Perito.objects.all()
		form = CentroInspeccionForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect(reverse('admin_centros'))

		else:
			print "MALLLL", form.errors
			c_estado_id = request.POST.get('estado', None)
			c_municipios = Municipio.objects.filter(estado__id = c_estado_id)
			c_municipio_id = request.POST.get('municipio', None)
			if c_estado_id:
				c_estado_id = int(c_estado_id)
			if c_municipio_id:
				c_municipio_id = int(c_municipio_id)

			context = {
				'admin': True,
				'form': form,
				'c_estado_id': c_estado_id,
				'c_municipios': c_municipios,
				'c_municipio_id': c_municipio_id,
				'estados': estados,
				'peritos': peritos,
				'seccion_centros': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_centro.html', context)


class AdminEditarCentro(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEditarCentro, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Despliega el formulario para editar un centro de inspección"""
		usuario = request.user

		centro = CentroInspeccion.objects.filter(id=kwargs['centro_id']).first()

		if centro:
			c_estado_id = centro.municipio.estado.pk
			c_municipios = Municipio.objects.filter(estado__id = c_estado_id)
			c_municipio_id = centro.municipio.pk
			form = CentroInspeccionForm(instance = centro)
			estados = Estado.objects.all()
			peritos = Perito.objects.all()

			context = {
				'admin': True,
				'c_estado_id': c_estado_id,
				'c_municipios': c_municipios,
				'c_municipio_id': c_municipio_id,
				'centro_id': kwargs['centro_id'],
				'editar': True,
				'form': form,
				'estados': estados,
				'peritos': peritos,
				'seccion_centros': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_centro.html', context)

		else:
			return redirect(reverse('admin_centros'))

	def post(self, request, *args, **kwargs):
		"""Edita el centro de inspección"""
		usuario = request.user

		estados = Estado.objects.all()
		peritos = Perito.objects.all()
		centro = CentroInspeccion.objects.filter(id=kwargs['centro_id']).first()
		form = CentroInspeccionForm(request.POST, instance = centro)

		if form.is_valid():
			print form.cleaned_data['municipio']
			form.save()
			return redirect(reverse('admin_centros'))

		else:
			print "MALLLL", form.errors
			c_estado_id = request.POST.get('estado', None)
			c_municipios = Municipio.objects.filter(estado__id = c_estado_id)
			c_municipio_id = request.POST.get('municipio', None)
			if c_estado_id:
				c_estado_id = int(c_estado_id)
			if c_municipio_id:
				c_municipio_id = int(c_municipio_id)
			context = {
				'admin': True,
				'form': form,
				'c_estado_id': c_estado_id,
				'c_municipios': c_municipios,
				'c_municipio_id': c_municipio_id,
				'centro_id': kwargs['centro_id'],
				'editar': True,
				'estados': estados,
				'peritos': peritos,
				'seccion_centros': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_centro.html', context)


class AdminEliminarCentro(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEliminarCentro, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista que elimina un Centro de Inspección"""
		page = request.POST.get('page', None)
		centro_id = request.POST.get('centro_id', None)
		centro = CentroInspeccion.objects.filter(id=centro_id)
		if centro:
			centro.delete()
			redirect_url = reverse('admin_centros')
			if int(page) > 1:
				extra_params = '?page=%s' % page
				redirect_url = '%s%s' % (redirect_url, extra_params)

			return redirect(redirect_url, kwargs={'location': page})
		else:
			return redirect(redirect_url, kwargs={'location': page})


class AdminBandejaUsuarios(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminBandejaUsuarios, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que lista los usuarios taquilla al administrador"""
		usuario = request.user

		usuarios = SgtUsuario.objects.filter(rol__codigo = 'taquilla')

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		paginator = Paginator(usuarios, 10, request=request)
		usuarios = paginator.page(page)

		context = {
			'admin': True,
			'seccion_usuarios':True,
			'usuarios': usuarios,
			'usuario': usuario,
		}

		return render(request, 'admin/bandeja_usuarios.html', context)


class AdminCrearUsuario(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminCrearUsuario, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que despliega el formulario para la creación de usuarios Taquilla """
		usuario = request. user
		estados = Estado.objects.all()

		form = CuentasForm.RegistroForm()

		context = {
			'admin': True,
			'form': form,
			'estados': estados,
			'seccion_usuarios': True,
			'usuario': usuario,
		}

		return render(request, 'admin/crear_usuario.html', context)

	def post(self, request, *args, **kwargs):
		usuario = request.user

		estados = Estado.objects.all()
		form = CuentasForm.RegistroForm(request.POST)

		if form.is_valid():
			registro = form.cleaned_data
			rol_cliente = RolSgt.objects.get(codigo="taquilla")

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

			return redirect(reverse('admin_usuarios'))

		else:
			u_estado_id = request.POST.get('estado', None)
			u_municipios = Municipio.objects.filter(estado__id = u_estado_id)
			u_municipio_id = request.POST.get('municipio', None)
			if u_estado_id:
				u_estado_id = int(u_estado_id)
			if u_municipio_id:
				u_municipio_id = int(u_municipio_id)

			context = {
				'admin': True,
				'form': form,
				'u_estado_id': u_estado_id,
				'u_municipios': u_municipios,
				'u_municipio_id': u_municipio_id,
				'estados': estados,
				'seccion_usuarios': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_usuario.html', context)


class AdminEditarUsuarios(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEditarUsuarios, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Despliega el formulario para editar un usuario"""
		usuario = request.user 


class AdminBandejaEncuestas(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminBandejaEncuestas, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que lista las encuestas al administrador"""
		usuario = request.user

		encuestas = Encuesta.objects.all()

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		paginator = Paginator(encuestas, 10, request=request)
		encuestas = paginator.page(page)

		context = {
			'admin': True,
			'seccion_encuestas':True,
			'encuestas': encuestas,
			'usuario': usuario,
		}

		return render(request, 'admin/bandeja_encuestas.html', context)

class AdminAgregarEncuesta(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminAgregarEncuesta, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Despliega el formulario para crear encuestas"""
		usuario = request.user
		form = CrearEncuestaForm()

		preguntas = Pregunta.objects.all()
		tipos_respuesta = TipoRespuesta.objects.all()
		valores = ValorPosible.objects.all()

		context = {
			'admin': True,
			'form': form,
			'preguntas': preguntas,
			'valores': valores,
			'editar': False,
			'tipos_respuesta': tipos_respuesta,
			'usuario': usuario,
		}

		return render(request, 'admin/crear_encuesta.html', context)

	def post(self, request, *args, **kwargs):
		"""Crea el centro de inspección"""
		usuario = request.user
		form = RegistroForm(request.POST)

		if form.is_valid():

			print "guardando data..."

			return redirect(reverse('admin_encuestas'))

		else:
			preguntas = Pregunta.objects.all()
			tipos_respuesta = TipoRespuesta.objects.all()
			valores = ValorPosible.objects.all()

			context = {
				'admin': True,
				'form': form,
				'preguntas': preguntas,
				'valores': valores,
				'editar': False,
				'tipos_respuesta': tipos_respuesta,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_encuesta.html', context)



		# estados = Estado.objects.all()
		# peritos = Perito.objects.all()
		# form = CentroInspeccionForm(request.POST)

		# if form.is_valid():
		# 	form.save()
		# 	return redirect(reverse('admin_centros'))

		# else:
		# 	print "MALLLL", form.errors
		# 	c_estado_id = request.POST.get('estado', None)
		# 	c_municipios = Municipio.objects.filter(estado__id = c_estado_id)
		# 	c_municipio_id = request.POST.get('municipio', None)
		# 	if c_estado_id:
		# 		c_estado_id = int(c_estado_id)
		# 	if c_municipio_id:
		# 		c_municipio_id = int(c_municipio_id)

		# 	context = {
		# 		'admin': True,
		# 		'form': form,
		# 		'c_estado_id': c_estado_id,
		# 		'c_municipios': c_municipios,
		# 		'c_municipio_id': c_municipio_id,
		# 		'estados': estados,
		# 		'peritos': peritos,
		# 		'seccion_centros': True,
		# 		'usuario': usuario,
		# 	}

		# 	return render(request, 'admin/crear_centro.html', context)
