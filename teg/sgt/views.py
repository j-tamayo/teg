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
		#print "ARGS", args
		#print "KWARGS", kwargs
		centros = CentroInspeccion.objects.all().order_by('-id')

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
			'peritos_asignados': [],
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
				'peritos_asignados': [],
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
			peritos_asignados = centro.peritos.all()

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
				'peritos_asignados': peritos_asignados,
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
		peritos_asignados = centro.peritos.all()
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
				'peritos_asignados': peritos_asignados,
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
			u_municipios = []
			u_municipio_id = request.POST.get('municipio', None)
			if u_estado_id:
				u_municipios = Municipio.objects.filter(estado__id = u_estado_id)
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


class AdminEditarUsuario(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEditarUsuario, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Despliega el formulario para editar un usuario"""
		usuario = request.user

		user = SgtUsuario.objects.filter(id=kwargs['user_id']).first()

		if user:
			u_estado_id = user.municipio.estado.pk
			u_municipios = Municipio.objects.filter(estado__id = u_estado_id)
			u_municipio_id = user.municipio.pk
			initial_data = {
				'nombres': user.nombres,
				'apellidos': user.apellidos,
				'cedula': user.cedula,
				'estado': user.municipio.estado.pk,
				'municipio': user.municipio.pk,
				'codigo_postal': user.codigo_postal,
				'direccion': user.direccion,
				'correo': user.correo,
				'sexo': user.sexo,
				'telefono_local': user.telefono_local,
				'telefono_movil': user.telefono_movil,
				'fecha_nacimiento': user.fecha_nacimiento
			}
			form = CuentasForm.RegistroForm(initial = initial_data)
			estados = Estado.objects.all()

			context = {
				'admin': True,
				'form': form,
				'u_estado_id': u_estado_id,
				'u_municipios': u_municipios,
				'u_municipio_id': u_municipio_id,
				'user_id': kwargs['user_id'],
				'editar': True,
				'estados': estados,
				'seccion_usuarios': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_usuario.html', context)

		else:
			return redirect(reverse('admin_usuarios'))

	def post(self, request, *args, **kwargs):
		"""Edita el Usuario"""
		usuario = request.user

		estados = Estado.objects.all()
		user = SgtUsuario.objects.filter(id=kwargs['user_id']).first()
		form = CuentasForm.RegistroForm(request.POST)

		if form.is_valid():
			registro = form.cleaned_data
			user.nombres = registro['nombres']
			user.apellidos = registro['apellidos']
			user.cedula = registro['cedula']
			user.municipio_id = registro['municipio']
			user.direccion = registro['direccion']
			user.codigo_postal = registro['codigo_postal']
			user.correo = registro['correo']
			user.fecha_nacimiento = registro['fecha_nacimiento']
			user.telefono_local = registro['telefono_local']
			user.telefono_movil = registro['telefono_movil']
			user.sexo = registro['sexo']

			user.save()

			return redirect(reverse('admin_centros'))

		else:
			print "MALLLL", form.errors
			u_estado_id = request.POST.get('estado', None)
			u_municipio_id = request.POST.get('municipio', None)
			if u_estado_id:
				u_municipios = Municipio.objects.filter(estado__id = u_estado_id)
				u_estado_id = int(u_estado_id)
			if u_municipio_id:
				u_municipio_id = int(u_municipio_id)
			context = {
				'admin': True,
				'form': form,
				'u_estado_id': u_estado_id,
				'u_municipios': u_municipios,
				'u_municipio_id': u_municipio_id,
				'user_id': kwargs['user_id'],
				'editar': True,
				'estados': estados,
				'seccion_usuarios': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_usuario.html', context)


class AdminDeshabilitarUsuario(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminDeshabilitarUsuario, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista que deshabilita o habilita a un usuario"""
		page = request.POST.get('page', None)
		user_id = request.POST.get('user_id', None)
		user = SgtUsuario.objects.filter(id=user_id).first()
		redirect_url = reverse('admin_usuarios')
		if user:
			user.is_active = not user.is_active
			user.save()
			if int(page) > 1:
				extra_params = '?page=%s' % page
				redirect_url = '%s%s' % (redirect_url, extra_params)

			return redirect(redirect_url, kwargs={'location': page})
		else:
			return redirect(redirect_url, kwargs={'location': page})


class AdminBandejaPeritos(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminBandejaPeritos, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que lista los Peritos """
		usuario = request.user

		peritos = Perito.objects.all().order_by('-id')

		paginator = Paginator(peritos, 10, request=request)
		try:
			page = request.GET.get('page', 1)
			peritos = paginator.page(page)
		except PageNotAnInteger:
			peritos = paginator.page(1)
			page = 0
		except EmptyPage:
			peritos = paginator.page(paginator.num_pages)
		
		context = {
			'admin': True,
			'peritos': peritos,
			'seccion_peritos': True,
			'usuario': usuario,
		}

		return render(request, 'admin/bandeja_peritos.html', context)


class AdminAgregarPerito(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminAgregarPerito, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que despliega el formulario para la creación de un Perito"""
		usuario = request.user

		form = PeritoForm()

		context = {
			'admin': True,
			'form': form,
			'seccion_peritos': True,
			'usuario': usuario,
		}

		return render(request, 'admin/crear_perito.html', context)

	def post(self, request, *args, **kwargs):
		"""Crea el Perito"""
		usuario = request.user

		form = PeritoForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect(reverse('admin_peritos'))

		else:
			print "MALLLL", form.errors

			context = {
				'admin': True,
				'form': form,
				'seccion_peritos': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_perito.html', context)


class AdminEditarPerito(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEditarPerito, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que despliega el formulario para editar un perito"""
		usuario = request.user

		perito = Perito.objects.filter(id=kwargs['perito_id']).first()

		if perito:
			form = PeritoForm(instance = perito)

			context = {
				'admin': True,
				'perito_id': kwargs['perito_id'],
				'editar': True,
				'form': form,
				'seccion_peritos': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_perito.html', context)

		else:
			return redirect(reverse('admin_peritos'))

	def post(self, request, *args, **kwargs):
		"""Edita el centro de inspección"""
		usuario = request.user

		perito = Perito.objects.filter(id=kwargs['perito_id']).first()
		form = PeritoForm(request.POST, instance = perito)

		if form.is_valid():
			form.save()
			return redirect(reverse('admin_peritos'))

		else:
			print "MALLLL", form.errors
			context = {
				'admin': True,
				'form': form,
				'perito_id': kwargs['perito_id'],
				'editar': True,
				'seccion_peritos': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_centro.html', context)


class AdminDeshabilitarPerito(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminDeshabilitarPerito, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista que deshabilita los Peritos"""
		page = request.POST.get('page', None)
		perito_id = request.POST.get('perito_id', None)
		perito = Perito.objects.filter(id=perito_id).first()
		redirect_url = reverse('admin_peritos')
		if perito:
			perito.activo = not perito.activo
			perito.save()
			if int(page) > 1:
				extra_params = '?page=%s' % page
				redirect_url = '%s%s' % (redirect_url, extra_params)

			return redirect(redirect_url)
		else:
			return redirect(redirect_url)


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
		
		data_initial = {
			'extra_field_count': 0
		}
		
		form = CrearEncuestaForm(initial=data_initial)
		form_preg = CrearPreguntaForm()
		form_val = CrearValorForm()

		tipos_respuesta = TipoRespuesta.objects.all()
		preguntas = Pregunta.objects.all()
		tipos_encuesta = TipoEncuesta.objects.all()
		valores = ValorPosible.objects.all()

		context = {
			'admin': True,
			'editar': False,
			'form': form,
			'form_preg': form_preg,
			'form_val': form_val,
			'preguntas': preguntas,
			'valores': valores,
			'tipos_respuesta': tipos_respuesta,
			'tipos_encuesta': tipos_encuesta,
			'usuario': usuario,
		}

		return render(request, 'admin/crear_encuesta.html', context)

	def post(self, request, *args, **kwargs):
		"""Crea la encuesta"""
		usuario = request.user
		form = CrearEncuestaForm(request.POST, extra=request.POST.get('extra_field_count'))
		form_preg = CrearPreguntaForm()
		form_val = CrearValorForm()

		if form.is_valid():
			encuesta_data = form.cleaned_data
			extra_fields = encuesta_data['extra_field_count']
			
			encuesta = Encuesta(
				nombre=encuesta_data['nombre'], 
				descripcion=encuesta_data['descripcion'], 
				tipo_encuesta=encuesta_data['tipo_encuesta'])

			encuesta.save()

			for index in range(int(extra_fields)):
				aux = 'tipo_respuesta_' + str(index + 1)
				tipo_respuesta = encuesta_data[aux]

				aux = 'pregunta_' + str(index + 1)
				pregunta = encuesta_data[aux]

				if tipo_respuesta.codigo == 'RESP_DEF':
					aux = 'valores_posibles_' + str(index + 1)
					valores_posibles = encuesta_data[aux]

					for v in valores_posibles:
						#v.valor_pregunta.add(pregunta)
						valor_pregunta_encuesta = ValorPreguntaEncuesta(
							valor = v, 
							pregunta = pregunta,
							encuesta = encuesta)

						valor_pregunta_encuesta.save()

				encuesta.preguntas.add(pregunta)

			return redirect(reverse('admin_encuestas'))

		else:
			print form.errors

			tipos_respuesta = TipoRespuesta.objects.all()
			preguntas = Pregunta.objects.all()
			tipos_encuesta = TipoEncuesta.objects.all()
			valores = ValorPosible.objects.all()

			context = {
				'admin': True,
				'editar': False,
				'form': form,
				'form_preg': form_preg,
				'form_val': form_val,
				'preguntas': preguntas,
				'valores': valores,
				'tipos_respuesta': tipos_respuesta,
				'tipos_encuesta': tipos_encuesta,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_encuesta.html', context)


class AdminEditarEncuesta(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEditarEncuesta, self).dispatch(*args, **kwargs)

	def get_context(self, encuesta, usuario, form=None):
		form_preg = CrearPreguntaForm()
		form_val = CrearValorForm()

		tipos_respuesta = TipoRespuesta.objects.all()
		preguntas = Pregunta.objects.all()
		tipos_encuesta = TipoEncuesta.objects.all()
		valores = ValorPosible.objects.all()

		extra_fields = len(encuesta.preguntas.all())
		encuesta_preguntas = encuesta.preguntas.all().order_by('id')
		encuesta_valores = ValorPosible.objects.filter(valor_pregunta__pregunta=encuesta_preguntas)
		print encuesta_valores 

		if not form:
			initial_data = {
				'nombre': encuesta.nombre,
				'descripcion': encuesta.descripcion,
				'tipo_encuesta': encuesta.tipo_encuesta,
				'extra_field_count': str(extra_fields)
			}

			#Probablemente esto sea innecesario... xD
			for index in range(int(extra_fields)):
				aux = 'tipo_respuesta_' + str(index + 1)
				initial_data[aux] = encuesta_preguntas[index].tipo_respuesta
				codigo_tipo_respuesta = encuesta_preguntas[index].tipo_respuesta.codigo
				
				aux = 'pregunta_' + str(index + 1)
				initial_data[aux] = encuesta_preguntas[index]

				if codigo_tipo_respuesta == 'RESP_DEF':
					aux = 'valores_posibles_' + str(index + 1)
					
					valores_pregunta = [] 
					for v in encuesta_valores:
						preguntas_valores = v.valor_pregunta.all()
						if encuesta_preguntas[index] in preguntas_valores:
							valores_pregunta.append(v)

					initial_data[aux] = valores_pregunta

			form = CrearEncuestaForm(initial=initial_data, extra=str(extra_fields))

		context = {
			'admin': True,
			'editar': True,
			'form': form,
			'form_preg': form_preg,
			'form_val': form_val,
			'preguntas': preguntas,
			'valores': valores,
			'tipos_respuesta': tipos_respuesta,
			'tipos_encuesta': tipos_encuesta,
			'encuesta': encuesta,
			'encuesta_preguntas': encuesta_preguntas,
			'encuesta_valores': encuesta_valores,
			'usuario': usuario,
		}

		return context

	def get(self, request, *args, **kwargs):
		"""Cargando formulario de encuesta"""
		usuario = request.user
		encuesta_id = kwargs['encuesta_id']
		encuesta = Encuesta.objects.filter(id=kwargs['encuesta_id']).first()

		if encuesta:
			return render(request, 'admin/crear_encuesta.html', self.get_context(encuesta, usuario))
		else:
			return redirect(reverse('admin_encuestas'))

	def post(self, request, *args, **kwargs):
		"""Edita la encuesta"""
		usuario = request.user
		encuesta_id = kwargs['encuesta_id']
		encuesta = Encuesta.objects.filter(id=kwargs['encuesta_id']).first()
		form = CrearEncuestaForm(request.POST, extra=request.POST.get('extra_field_count'))

		if form.is_valid():
			print "Editando la encuesta..."
			encuesta_data = form.cleaned_data
			extra_fields = encuesta_data['extra_field_count']
			
			encuesta_preguntas = encuesta.preguntas.all()
			encuesta.nombre = encuesta_data['nombre']
			encuesta.descripcion = encuesta_data['descripcion']
			encuesta.tipo_encuesta = encuesta_data['tipo_encuesta']
			encuesta.save()

			for index in range(int(extra_fields)):
				aux = 'tipo_respuesta_' + str(index + 1)
				tipo_respuesta = encuesta_data[aux]

				aux = 'pregunta_' + str(index + 1)
				pregunta = encuesta_data[aux]

				#si no existe previamente, entonces se agrega
				if pregunta not in encuesta_preguntas:
					if tipo_respuesta.codigo == 'RESP_DEF':
						aux = 'valores_posibles_' + str(index + 1)
						valores_posibles = encuesta_data[aux]

						for valor in valores_posibles:
							print "agregando valor:", valor, "para pregunta:", pregunta
							vpe = ValorPreguntaEncuesta(
								valor = valor, 
								pregunta = pregunta, 
								encuesta = encuesta)
							vpe.save()

					print "guardando pregunta", pregunta
					encuesta.preguntas.add(pregunta)
				else:
					encuesta_preguntas.exclude(id=pregunta.id)
				
					if tipo_respuesta.codigo == 'RESP_DEF':
						valores_pregunta = ValorPosible.objects.filter(valor_pregunta_encuesta=pregunta)
						aux = 'valores_posibles_' + str(index + 1)
						valores_posibles = encuesta_data[aux]

						for valor in valores_pregunta:
							if valor not in valores_posibles:
								print "agregando valor:", valor, "para pregunta:", pregunta
								vpe = ValorPreguntaEncuesta(
									valor = valor, 
									pregunta = pregunta, 
									encuesta = encuesta)
								vpe.save()
							else:
								print valores_pregunta
								valores_pregunta.exclude(id=valor.id)
								print valores_pregunta

						for valor in valores_pregunta:
							vpe = ValorPreguntaEncuesta.objects.get(valor=valor, pregunta=pregunta, encuesta=encuesta)
							vpe.delete()

			#Nota: hay que excluir para despues eliminar lo que sobra...
			for pregunta in encuesta_preguntas:
				encuesta.preguntas.remove(pregunta)

			return redirect(reverse('admin_encuestas'))
		else:
			return render(request, 'admin/crear_encuesta.html', self.get_context(encuesta, usuario, form))

class AdminEliminarEncuesta(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEliminarEncuesta, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista que elimina un Centro de Inspección"""
		page = request.POST.get('page', None)
		print "eliminando encuesta"
		encuesta_id = request.POST.get('encuesta_id', None)
		encuesta = Encuesta.objects.filter(id=encuesta_id).first()
		if encuesta:
			encuesta_preguntas = encuesta.preguntas.all()
			encuesta_valores = ValorPosible.objects.filter(valor_pregunta__pregunta=encuesta_preguntas)

			for v in encuesta_valores:
				preguntas_valores = v.valor_pregunta.all()
				for p in encuesta_preguntas:
					if p in preguntas_valores:
						vpe = ValorPreguntaEncuesta.objects.get(valor=v, pregunta=p, encuesta=encuesta)
						vpe.delete()
						#v.valor_pregunta.remove(p)

			encuesta.preguntas.clear()

			encuesta.delete()

			redirect_url = reverse('admin_encuestas')
			if int(page) > 1:
				extra_params = '?page=%s' % page
				redirect_url = '%s%s' % (redirect_url, extra_params)

			return redirect(redirect_url, kwargs={'location': page})
		else:
			return redirect(redirect_url, kwargs={'location': page})


class AdminAgregarPregunta(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminAgregarPregunta, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Buscando preguntas existentes"""
		usuario = request.user
		tipo_respuesta_id = kwargs['tipo_respuesta_id']

		respuesta = {}
		if tipo_respuesta_id:
			preguntas = Pregunta.objects.filter(tipo_respuesta__id = tipo_respuesta_id)
			respuesta = serializers.serialize('json', preguntas)

		else:
			respuesta = {
				'mensaje': 'No se suministró el id del tipo de respuesta'
			}
			resuesta = json.dumps(respuesta)

		return HttpResponse(
		    respuesta,
		    content_type="application/json"
		)

	def post(self, request, *args, **kwargs):
		"""Crea nueva pregunta"""
		usuario = request.user
		form = CrearPreguntaForm(request.POST)
		data = request.POST

		respuesta = {}
		if form.is_valid():
			tipo_respuesta = TipoRespuesta.objects.get(id=data['tipo_respuesta'])
			pregunta = Pregunta(enunciado=data['enunciado'], tipo_respuesta=tipo_respuesta)
			pregunta.save();
			respuesta = {
				'id_pregunta': pregunta.id, 
				'enunciado': pregunta.enunciado,
				'tipo_respuesta': tipo_respuesta.codigo
			}
			
		else:
			respuesta = {'mensaje': form.errors}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class AdminEliminarPregunta(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEliminarPregunta, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Eliminar preguntas"""
		usuario = request.user
		data = request.POST
		preguntas_id = data['preguntas_id']
		
		respuesta = {}
		if preguntas_id:
			preguntas_id = preguntas_id.split('|');
			for p in preguntas_id:
				preguntas = Pregunta.objects.get(id=p)
				preguntas.delete()
			
			respuesta = {
				'mensaje': 'Preguntas eliminadas satisfactoriamente'
			}

		else:
			respuesta = {
				'mensaje': 'No se suministró el id de la pregunta'
			}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class AdminAgregarRespuesta(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminAgregarRespuesta, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Crea nueva respuesta"""
		usuario = request.user
		form = CrearValorForm(request.POST)
		data = request.POST

		respuesta = {}
		if form.is_valid():
			valor_posible = ValorPosible(valor=data['valor'])
			valor_posible.save();
			
			respuesta = {
				'id_respuesta': valor_posible.id, 
				'valor': valor_posible.valor
			}
			
		else:
			respuesta = {'mensaje': form.errors}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class AdminEliminarRespuesta(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminEliminarRespuesta, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Eliminar respuestas"""
		usuario = request.user
		data = request.POST
		valores_id = data['valores_id']
		
		respuesta = {}
		if valores_id:
			valores_id = valores_id.split('|');
			for v in valores_id:
				valor_posible = ValorPosible.objects.get(id=v)
				valor_posible.delete()
			
			respuesta = {
				'mensaje': 'Respuestas eliminadas satisfactoriamente'
			}

		else:
			respuesta = {
				'mensaje': 'No se suministró el id de la pregunta'
			}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class AdminReportes(View):
	def dispatch(self, *args, **kwargs):
		return super(AdminReportes, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que muestra el reporte de las solicitudes"""
		usuario = request.user
		filtros = {}
		centros = CentroInspeccion.objects.filter()
		estados = Estado.objects.filter(municipio__centroinspeccion=centros).distinct('id')
		estatus = Estatus.objects.filter(codigo__in = ['solicitud_en_proceso','solicitud_procesada','solicitud_no_procesada'])
		
		if request.session.has_key('filtros_reporte'):
			filtros = request.session['filtros_reporte']

		numeros_orden = NumeroOrden.reporte(filtros)
		print numeros_orden

		paginator = Paginator(numeros_orden, 10, request=request)
		try:
			page = request.GET.get('page', 1)
			numeros_orden = paginator.page(page)
		except PageNotAnInteger:
			numeros_orden = paginator.page(1)
			page = 0
		except EmptyPage:
			numeros_orden = paginator.page(paginator.num_pages)

		context = {
			'admin': True,
			'estados': estados,
			'estatus': estatus,
			'numeros_orden': numeros_orden,
			'seccion_reportes': True,
			'usuario': usuario,
		}

		return render(request, 'admin/reportes.html', context)

	def post(self, request, *args, **kwargs):
		"""Metodo que aplica los filtros"""
		usuario = request.user
		centros = CentroInspeccion.objects.filter()
		estados = Estado.objects.filter(municipio__centroinspeccion=centros).distinct('id')
		estatus = Estatus.objects.filter(codigo__in = ['solicitud_en_proceso','solicitud_procesada','solicitud_no_procesada'])
		#Se guardan en la sesión los filtros seleccionados
		filtros = {}
		for key in request.POST:
			filtros[key] = request.POST.getlist(key)
			if len(filtros[key]) == 1:
				filtros[key] = request.POST.get(key)

		request.session['filtros_reporte'] = filtros

		numeros_orden = NumeroOrden.reporte(filtros)
		print numeros_orden

		paginator = Paginator(numeros_orden, 10, request=request)
		try:
			page = request.GET.get('page', 1)
			numeros_orden = paginator.page(page)
		except PageNotAnInteger:
			numeros_orden = paginator.page(1)
			page = 0
		except EmptyPage:
			numeros_orden = paginator.page(paginator.num_pages)

		context = {
			'admin': True,
			'estados': estados,
			'estatus': estatus,
			'numeros_orden': numeros_orden,
			'seccion_reportes': True,
			'usuario': usuario,
		}

		return render(request, 'admin/reportes.html', context)
