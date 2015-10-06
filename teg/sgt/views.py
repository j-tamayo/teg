# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from sgt.models import *
from sgt.forms import *
from sgt.helpers import solicitudes,dates,utils
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from cuentas import forms as CuentasForm
from cuentas.models import *
from datetime import datetime

import json

# Create your views here.
class ObtenerMunicipios(View):
	def dispatch(self, *args, **kwargs):
		return super(ObtenerMunicipios, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""" Vista que retorna en formato JSON los municipios dependiendo del estado_id recibido """
		estado_id = kwargs['estado_id']
		if estado_id:
			municipios = Municipio.objects.filter(estado__id = estado_id)
			# Para obtener los municipios que tengan asociado al menos un centro de inspeccion
			if request.GET.get('con_centro', None):
				print "ENTRO"
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(ObtenerCentroInspeccion, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""" Vista que retorna en formato JSON los centros de inspección dependiendo del municipio_id recibido """
		municipio_id = request.GET.get('municipio_id', None)
		estado_id = request.GET.get('estado_id', None)
		fecha_asistencia = request.GET.get('fecha_asistencia', datetime.now().date().strftime('%d/%m/%Y'))
		fecha_asistencia = datetime.strptime(fecha_asistencia, '%d/%m/%Y')
		centros = []
		if municipio_id or estado_id:
			if municipio_id:
				centros_query = CentroInspeccion.objects.filter(municipio__id = municipio_id)
			else:
				centros_query = CentroInspeccion.objects.filter(municipio__estado__id = estado_id)
			
			#Para calcular la disponibilidad de cada centro
			for c in centros_query:
				en_cola = NumeroOrden.objects.filter(fecha_atencion = fecha_asistencia).exclude(solicitud_inspeccion__estatus__codigo = 'solicitud_cancelada').count()
				capacidad = solicitudes.calcular_capacidad_centro(c)
				c.disponibilidad = capacidad - en_cola
				# Para calcular la disponibilidad (Alta, media, baja y muy baja)
				if c.disponibilidad > (3 * capacidad)/4:
					c.etiqueta = 'Alta'
					c.etiqueta_clase = 'success'
				elif c.disponibilidad > (2 * capacidad)/4:
					c.etiqueta = 'Media'
					c.etiqueta_clase = 'warning'
				elif c.disponibilidad > (1 * capacidad)/4:
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(GenerarNumeroOrden, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		centro_id = kwargs['centro_id']
		print centro_id
		centro_inspeccion = CentroInspeccion.objects.get(id=centro_id)
		fecha_asistencia = fecha_asistencia = request.GET.get('fecha_asistencia', None)
		# fecha_asistencia = datetime.strptime(fecha_asistencia, '%d/%m/%Y')

		horarios = []
		
		centro = []
		# en_cola = NumeroOrden.objects.filter(fecha_atencion = fecha_asistencia).count()
		# capacidad = solicitudes.calcular_capacidad_centro(centro_inspeccion)
		# centro_inspeccion.disponibilidad = capacidad - en_cola
		# # Para calcular la disponibilidad (Alta, media, baja y muy baja)
		# if centro_inspeccion.disponibilidad > (3 * centro_inspeccion.capacidad)/4:
		# 	centro_inspeccion.etiqueta = 'Alta'
		# 	centro_inspeccion.etiqueta_clase = 'success'
		# elif centro_inspeccion.disponibilidad > (2 * centro_inspeccion.capacidad)/4:
		# 	centro_inspeccion.etiqueta = 'Media'
		# 	centro_inspeccion.etiqueta_clase = 'warning'
		# elif centro_inspeccion.disponibilidad > (1 * centro_inspeccion.capacidad)/4:
		# 	centro_inspeccion.etiqueta = 'Baja'
		# 	centro_inspeccion.etiqueta_clase = 'low'
		# else:
		# 	centro_inspeccion.etiqueta = 'Muy baja'
		# 	centro_inspeccion.etiqueta_clase = 'danger'

		fecha_asistencia = dates.convert(fecha_asistencia, '%d/%m/%Y', '%Y-%m-%d')
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(CrearSolicitudInspeccion, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		usuario = request.user
		estado_id = request.GET.get('estado', None)
		# tipo_solicitudes = TipoInspeccion.objects.all()
		centros = CentroInspeccion.objects.all()
		municipios = Municipio.objects.filter(estado__id = estado_id)
		fecha_asistencia = request.GET.get('fecha_asistencia', datetime.now().date().strftime('%d/%m/%Y'))
		fecha_asistencia = datetime.strptime(fecha_asistencia, '%d/%m/%Y')
		poliza = Poliza.objects.filter(usuario = usuario).first()
		# Para obtener los tipos de solicitudes dependiendo de la póliza del usuario
		today = datetime.now().date()
		print "POLIZA", poliza
		if poliza and poliza.fecha_inicio_vigencia <= today and poliza.fecha_fin_vigencia >= today:
			tipo_solicitudes = TipoInspeccion.objects.all()
		
		else:
			tipo_solicitudes = TipoInspeccion.objects.all().exclude(codigo = 'SRI')
			print tipo_solicitudes

		if estado_id:
			aux = centros.filter(municipio__estado__id = estado_id)
			if aux:
				centros = aux

		#Para calcular la disponibilidad de cada centro
		for c in centros:
			en_cola = NumeroOrden.objects.filter(fecha_atencion = fecha_asistencia).exclude(solicitud_inspeccion__estatus__codigo = 'solicitud_cancelada').count()
			capacidad = solicitudes.calcular_capacidad_centro(c)
			c.disponibilidad = capacidad - en_cola
			if c.disponibilidad < 0:
				c.disponibilidad = 0
			# Para calcular la disponibilidad (Alta, media, baja y muy baja)
			if c.disponibilidad > (3 * capacidad)/4:
				c.etiqueta = 'Alta'
				c.etiqueta_clase = 'success'
			elif c.disponibilidad > (2 * capacidad)/4:
				c.etiqueta = 'Media'
				c.etiqueta_clase = 'warning'
			elif c.disponibilidad > (1 * capacidad)/4:
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
		fecha_asistencia = dates.str_to_datetime(fecha_asistencia, '%d/%m/%Y')
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
					fecha_atencion = fecha_asistencia,
					hora_atencion = hora_asistencia
				)
				numero_orden.save()
				#Actualizamos el codigo del número de orden
				numero_orden.codigo = str(numero_orden.pk)
				numero_orden.save()

				#Para guardar el tiempo de atención para esta fecha
				if CentrosTiemposAtencion.objects.filter(fecha = fecha_asistencia).count() <= 0:
					centro_tiempo_anterior = CentrosTiemposAtencion(
						fecha = fecha_asistencia,
						centro_inspeccion = centro_inspeccion,
						tiempo_atencion = centro_inspeccion.tiempo_atencion
					)
					centro_tiempo_anterior.save()

				respuesta['solicitud'] = {
					'id': solicitud.pk,
					'tipo_solicitud': solicitud.tipo_inspeccion.nombre,
					'numero_orden': numero_orden.codigo,
					'estatus': solicitud.estatus.nombre,
					'fecha_atencion': numero_orden.fecha_atencion.strftime('%d/%m/%Y'),
					'hora_atencion': numero_orden.hora_atencion.strftime('%I:%M %p')
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


class MarcarSolicitud(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(MarcarSolicitud, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""
		Marcar solicitudes borradas
		"""
		valido = True
		error_msg = ''
		id_solicitud = request.POST.get('id_solicitud', 0)
		solicitud_resp = None

		solicitud = SolicitudInspeccion.objects.filter(id = id_solicitud).first()
		if solicitud:
			solicitud.borrada = True
			if solicitud.estatus.codigo == 'solicitud_en_proceso':
				solicitud.estatus = Estatus.objects.get(codigo = 'solicitud_cancelada')

			solicitud.save()
			solicitud_resp = {'estatus': solicitud.estatus.nombre}

		else:
			valido = False
			error_msg = 'No se suministró una solicitud válida'

		respuesta = {
			'valido': valido,
			'error_msg': error_msg,
			'solicitud': solicitud_resp if solicitud_resp else ''
		}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class MarcarFechasNoLaborables(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(MarcarFechasNoLaborables, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""
		Vista encargada de marcar las fechas no fechas_no_laborables
		para todos los centros
		"""
		valido = True
		error_msg = ''
		fechas_no_laborables = request.POST.getlist('fechas_no_laborables', [])
		if not fechas_no_laborables:
			valido = False
			error_msg = 'No se suministró ninguna fecha'

		else:
			centros = CentroInspeccion.objects.all()
			for f in fechas_no_laborables:
				fecha_object = datetime.strptime(f,'%d/%m/%Y').date()
				#Creo la fecha si no existe
				fecha = FechaNoLaborable.objects.filter(fecha = fecha_object).first()
				if not fecha:
					fecha = FechaNoLaborable(fecha = fecha_object)
					fecha.save()

				#Agrego las fechas por centro (Solo si no existen)
				for c in centros:
					if not c.fechas_no_laborables.filter(fecha = fecha_object).first():
						c.fechas_no_laborables.add(fecha)

		respuesta = {
			'valido': valido,
			'error_msg': error_msg
		}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)

class EstablecerHorariosGlobales(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(EstablecerHorariosGlobales, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""
		Vista encargada de establecer los horarios de atención
		para todos los centros
		"""
		valido = True
		error_msg = ''
		hora_apertura_manana = request.POST.get('hora_apertura_manana', None)
		hora_cierre_manana = request.POST.get('hora_cierre_manana', None)
		hora_apertura_tarde = request.POST.get('hora_apertura_tarde', None)
		hora_cierre_tarde = request.POST.get('hora_cierre_tarde', None)

		if hora_apertura_manana or hora_cierre_manana or hora_apertura_tarde or hora_cierre_tarde:
			if hora_apertura_manana:
				hora_apertura_manana = datetime.strptime(hora_apertura_manana, '%H:%M')
			if hora_cierre_manana:
				hora_cierre_manana = datetime.strptime(hora_cierre_manana, '%H:%M')
			if hora_apertura_tarde:
				hora_apertura_tarde = datetime.strptime(hora_apertura_tarde, '%H:%M')
			if hora_cierre_tarde:
				hora_cierre_tarde = datetime.strptime(hora_cierre_tarde, '%H:%M')

			centros = CentroInspeccion.objects.all()
			for c in centros:
				if hora_apertura_manana:
					c.hora_apertura_manana = hora_apertura_manana
				if hora_cierre_manana:
					c.hora_cierre_manana = hora_cierre_manana
				if hora_apertura_tarde:
					c.hora_apertura_tarde = hora_apertura_tarde
				if hora_cierre_tarde:
					c.hora_cierre_tarde = hora_cierre_tarde

				c.save()

		else:
			valido = False
			error_msg = 'No se suministró ningún horario'

		respuesta = {
			'valido': valido,
			'error_msg': error_msg
		}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class GuardarReclamo(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(GuardarReclamo, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""
		Vista encargada de registrar los reclamos de los clientes
		"""
		usuario = request.user
		valido = True
		errores = {}
		motivo = request.POST.get('motivo', None)
		observaciones = request.POST.get('observaciones', None)
		print "HEY",motivo,observaciones,request.POST
		if not motivo.strip():
			valido = False
			errores['motivo'] = 'Este campo es requerido'

		if not observaciones.strip():
			valido = False
			errores['observaciones'] = 'Este campo es requerido'

		if valido:
			Reclamo(usuario=usuario, motivo=motivo, contenido=observaciones).save()

		respuesta = {
			'valido': valido,
			'errores': errores
		}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class BandejaCliente(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(BandejaCliente, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que maneja la bandeja del usuario común """
		usuario = request.user
		tipo_solicitudes = TipoInspeccion.objects.all()
		form = SolicitudInspeccionForm(request.POST)
		poliza = Poliza.objects.filter(usuario = usuario).first()
		solicitudes = SolicitudInspeccion.objects.filter(usuario = usuario, borrada = False).order_by('-numeroorden__fecha_atencion','-numeroorden__hora_atencion')
		notificaciones = NotificacionUsuario.objects.filter(usuario = usuario, borrada = False).order_by('-leida', '-pk')

		u_estado_id = usuario.municipio.estado.pk
		u_municipios = Municipio.objects.filter(estado__id = u_estado_id)
		u_municipio_id = usuario.municipio.pk
		initial_data = {
			'nombres': usuario.nombres,
			'apellidos': usuario.apellidos,
			'cedula': usuario.cedula,
			'estado': usuario.municipio.estado.pk,
			'municipio': usuario.municipio.pk,
			'codigo_postal': usuario.codigo_postal,
			'direccion': usuario.direccion,
			'correo': usuario.correo,
			'sexo': usuario.sexo,
			'telefono_local': usuario.telefono_local,
			'telefono_movil': usuario.telefono_movil,
			'fecha_nacimiento': usuario.fecha_nacimiento,
			'centro_inspeccion': usuario.centro_inspeccion,
		}

		estados_cuenta = Estado.objects.all()
		form_cuenta = CuentasForm.RegistroForm(initial = initial_data)

		for s in solicitudes:
			s.numero_orden = NumeroOrden.objects.filter(solicitud_inspeccion = s).first()

		context = {
		    'usuario': usuario,
		    'tipo_solicitudes': tipo_solicitudes,
		    'estados_cuenta': estados_cuenta,
		    'form': form,
		    'form_cuenta': form_cuenta,
		    'poliza': poliza,
		    'solicitudes': solicitudes,
		    'notificaciones': notificaciones,
		    'u_estado_id': u_estado_id,
		    'u_municipios': u_municipios,
		    'u_municipio_id': u_municipio_id
		}

		return render(request,'cuentas/perfil_cliente.html', context)


class BuscarNotificaciones(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, request, *args, **kwargs):
		return super(BuscarNotificaciones, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista para buscar las notificaciones por el asunto"""
		usuario = request.user
		notificaciones_resp = []
		asunto = request.POST.get('asunto', None)
		notificaciones_usuario = NotificacionUsuario.objects.filter(usuario = usuario)
		if asunto:
			notificaciones_usuario = notificaciones.filter(notificacion__asunto__icontains = asunto)

		for nu in notificaciones_usuario:
			notificaciones_resp.append({
				'id': nu.pk,
				'asunto': nu.notificacion.asunto,
				'leida': nu.leida, 
				'fecha_recibida': '1',
				'tipo': nu.tipo,
			})

		respuesta = {
			'notificaciones': notificaciones_resp
		}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class AdminBandejaCentros(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminAgregarCentro, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Despliega el formulario para crear un centro de inspección"""
		usuario = request.user

		form = CentroInspeccionForm()
		estados = Estado.objects.all()
		peritos = Perito.objects.filter(activo=True)

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
		peritos = Perito.objects.filter(activo=True)
		form = CentroInspeccionForm(request.POST)

		if form.is_valid():
			fechas_no_laborables = request.POST.getlist('fechas_no_laborables', [])
			form.save(fechas_no_laborables)
			return redirect(reverse('admin_centros'))

		else:
			print "MALLLL", form.errors
			peritos_asignados = request.POST.getlist('peritos',[])
			if peritos_asignados:
				peritos_asignados = map(int, peritos_asignados)
				
			c_estado_id = request.POST.get('estado', None)
			c_municipios = []
			c_municipio_id = request.POST.get('municipio', None)
			if c_estado_id:
				c_estado_id = int(c_estado_id)
				c_municipios = Municipio.objects.filter(estado__id = c_estado_id)
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
				'peritos_asignados': peritos_asignados,
			}

			return render(request, 'admin/crear_centro.html', context)


class AdminEditarCentro(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
			peritos = Perito.objects.filter(activo=True)
			peritos_asignados = centro.peritos.filter(activo=True).values_list('id',flat=True)
			fechas_no_laborables_centro = centro.fechas_no_laborables.all()
			fechas_no_laborables = []
			for f in fechas_no_laborables_centro:
				fechas_no_laborables.append(f.fecha.strftime('%d/%m/%Y'))

			context = {
				'admin': True,
				'c_estado_id': c_estado_id,
				'c_municipios': c_municipios,
				'c_municipio_id': c_municipio_id,
				'centro_id': kwargs['centro_id'],
				'editar': True,
				'fechas_no_laborables': fechas_no_laborables,
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
		peritos = Perito.objects.filter(activo=True)
		centro = CentroInspeccion.objects.filter(id=kwargs['centro_id']).first()
		peritos_asignados = centro.peritos.filter(activo=True).values_list('id',flat=True)
		form = CentroInspeccionForm(request.POST, instance = centro)

		if form.is_valid():
			print "HEYYYYY",request.POST.getlist('peritos')
			print form.cleaned_data['municipio']
			fechas_no_laborables = request.POST.getlist('fechas_no_laborables', [])
			form.save(fechas_no_laborables)
			return redirect(reverse('admin_centros'))

		else:
			print "MALLLL", form.errors
			peritos_asignados = request.POST.getlist('peritos',[])
			if peritos_asignados:
				peritos_asignados = map(int, peritos_asignados)

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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
			'seccion_parametros':True,
			'usuarios': usuarios,
			'usuario': usuario,
		}

		return render(request, 'admin/bandeja_usuarios.html', context)


class AdminCrearUsuario(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminCrearUsuario, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que despliega el formulario para la creación de usuarios Taquilla """
		usuario = request. user
		estados = Estado.objects.all()

		form = CuentasForm.RegistroForm(taquilla=1)

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
		form = CuentasForm.RegistroForm(request.POST, taquilla=1)

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
                rol = rol_cliente,
                centro_inspeccion = registro['centro_inspeccion'],
            )
            
			usuario.set_password(registro['password'])
			usuario.save()

			return redirect(reverse('admin_usuarios'))

		else:
			# print "ERRORES",form.errors
			u_estado_id = request.POST.get('estado', None)
			u_municipios = []
			u_centros = []
			u_municipio_id = request.POST.get('municipio', None)
			u_centro_id = request.POST.get('centro_inspeccion', None)
			if u_estado_id:
				u_municipios = Municipio.objects.filter(estado__id = u_estado_id)
				u_estado_id = int(u_estado_id)
			if u_municipio_id:
				u_centros = CentroInspeccion.objects.filter(municipio__id = u_municipio_id)
				u_municipio_id = int(u_municipio_id)
			if u_centro_id:
				u_centro_id = int(u_centro_id)

			context = {
				'admin': True,
				'form': form,
				'u_centros': u_centros,
				'u_centro_id': u_centro_id,
				'u_estado_id': u_estado_id,
				'u_municipios': u_municipios,
				'u_municipio_id': u_municipio_id,
				'estados': estados,
				'seccion_usuarios': True,
				'usuario': usuario,
			}

			return render(request, 'admin/crear_usuario.html', context)


class AdminEditarUsuario(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
			u_centros = CentroInspeccion.objects.filter(municipio__id = u_municipio_id)
			u_centro_id = user.centro_inspeccion.pk
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
				'fecha_nacimiento': user.fecha_nacimiento,
				'centro_inspeccion': user.centro_inspeccion,
			}
			form = CuentasForm.RegistroForm(initial = initial_data, taquilla=1)
			estados = Estado.objects.all()

			context = {
				'admin': True,
				'form': form,
				'u_centros': u_centros,
				'u_centro_id': u_centro_id,
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
		form = CuentasForm.RegistroForm(request.POST, taquilla = 1, id_usuario = user.pk, edicion = 1)

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
			user.centro_inspeccion = registro['centro_inspeccion']

			user.save()

			return redirect(reverse('admin_usuarios'))

		else:
			print "MALLLL", form.errors
			u_estado_id = request.POST.get('estado', None)
			u_municipios = []
			u_centros = []
			u_municipio_id = request.POST.get('municipio', None)
			u_centro_id = request.POST.get('centro_inspeccion', None)
			if u_estado_id:
				u_municipios = Municipio.objects.filter(estado__id = u_estado_id)
				u_estado_id = int(u_estado_id)
			if u_municipio_id:
				u_centros = CentroInspeccion.objects.filter(municipio__id = u_municipio_id)
				u_municipio_id = int(u_municipio_id)
			if u_centro_id:
				u_centro_id = int(u_centro_id)
			context = {
				'admin': True,
				'form': form,
				'u_centro_id': u_centro_id,
				'u_centros': u_centros,
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
			'seccion_parametros': True,
			'usuario': usuario,
		}

		return render(request, 'admin/bandeja_peritos.html', context)


class AdminAgregarPerito(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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


class AdminBandejaPolizas(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminBandejaPolizas, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que lista las Pólizas """
		usuario = request.user

		polizas = Poliza.objects.all()

		paginator = Paginator(polizas, 10, request=request)
		try:
			page = request.GET.get('page', 1)
			polizas = paginator.page(page)
		except PageNotAnInteger:
			polizas = paginator.page(1)
			page = 0
		except EmptyPage:
			polizas = paginator.page(paginator.num_pages)
		
		context = {
			'admin': True,
			'polizas': polizas,
			'seccion_parametros': True,
			'usuario': usuario,
		}

		return render(request, 'admin/bandeja_polizas.html', context)


class AdminBandejaEncuestas(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminAgregarEncuesta, self).dispatch(*args, **kwargs)

	def get_context(self, usuario, form=None):
		form_preg = CrearPreguntaForm()
		form_val = CrearValorForm()

		if not form:
			data_initial = {
				'extra_field_count': 0
			}

			form = CrearEncuestaForm(initial=data_initial)

		tipos_respuesta = TipoRespuesta.objects.all()
		preguntas = Pregunta.objects.all()
		valores = ValorPosible.objects.all()
		tipos_encuesta = TipoEncuesta.objects.all()
		
		aux = Encuesta.objects.filter(tipo_encuesta__codigo="ENC_CONF")
		if aux:
			tipos_encuesta = tipos_encuesta.exclude(codigo="ENC_CONF")

		aux = Encuesta.objects.filter(tipo_encuesta__codigo="ENC_JUST")
		if aux:
			tipos_encuesta = tipos_encuesta.exclude(codigo="ENC_JUST")

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
			'seccion_encuestas': True,
			'usuario': usuario
		}

		return context

	def get(self, request, *args, **kwargs):
		"""Despliega el formulario para crear encuestas"""
		usuario = request.user
		return render(request, 'admin/crear_encuesta.html', self.get_context(usuario))

	def post(self, request, *args, **kwargs):
		"""Crea la encuesta"""
		usuario = request.user
		data = request.POST
		form = CrearEncuestaForm(data, extra=request.POST.get('extra_field_count'))

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
					val_id_list = data.getlist(aux)

					valores_posibles = []
					for v in val_id_list:
						valores_posibles.append(ValorPosible.objects.get(id=v))

					orden = 1
					for v in valores_posibles:
						valor_pregunta_encuesta = ValorPreguntaEncuesta(
							valor = v, 
							pregunta = pregunta,
							encuesta = encuesta,
							orden = orden)

						valor_pregunta_encuesta.save()
						orden = orden + 1

				encuesta.preguntas.add(pregunta)

			return redirect(reverse('admin_encuestas'))

		else:
			print form.errors
			return render(request, 'admin/crear_encuesta.html', self.get_context(usuario, form))


class AdminEditarEncuesta(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminEditarEncuesta, self).dispatch(*args, **kwargs)

	def get_context(self, encuesta, usuario, form=None):
		form_preg = CrearPreguntaForm()
		form_val = CrearValorForm()

		tipos_respuesta = TipoRespuesta.objects.all()
		preguntas = Pregunta.objects.all()
		valores = ValorPosible.objects.all()
		tipos_encuesta = TipoEncuesta.objects.all()
		
		aux = Encuesta.objects.filter(tipo_encuesta__codigo="ENC_CONF")
		

		aux = Encuesta.objects.filter(tipo_encuesta__codigo="ENC_JUST")
		if aux:
			tipos_encuesta = tipos_encuesta.exclude(codigo="ENC_JUST")

		extra_fields = len(encuesta.preguntas.all())
		encuesta_preguntas = encuesta.preguntas.all().order_by('id')
		encuesta_valores = ValorPosible.objects.filter(valor_pregunta__pregunta=encuesta_preguntas)

		valores_pregunta_encuesta = {}
		encuesta_preguntas_def = encuesta_preguntas.exclude(tipo_respuesta__codigo="RESP_INDEF")
		for p in encuesta_preguntas_def:
			aux = ValorPreguntaEncuesta.objects.filter(pregunta=p, encuesta=encuesta).order_by('orden')
			valores_pregunta_encuesta[p.id] = [vals.valor for vals in aux]

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
			'valores_pregunta_encuesta': valores_pregunta_encuesta,
			'seccion_encuestas': True,
			'usuario': usuario
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
		
		data = request.POST
		form = CrearEncuestaForm(data, extra=request.POST.get('extra_field_count'))

		if form.is_valid():
			encuesta_data = form.cleaned_data
			extra_fields = encuesta_data['extra_field_count']
			
			encuesta_preguntas = encuesta.preguntas.all()
			encuesta.nombre = encuesta_data['nombre']
			encuesta.descripcion = encuesta_data['descripcion']
			encuesta.tipo_encuesta = encuesta_data['tipo_encuesta']
			encuesta.save()

			encuesta_preguntas_exclude = []
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
							vpe = ValorPreguntaEncuesta(
								valor = valor, 
								pregunta = pregunta, 
								encuesta = encuesta)
							vpe.save()

					encuesta.preguntas.add(pregunta)
				else:
					if tipo_respuesta.codigo == 'RESP_DEF':
						valores_pregunta = ValorPosible.objects.filter(valor_pregunta_encuesta=pregunta)
						aux = 'valores_posibles_' + str(index + 1)
						val_id_list = data.getlist(aux)

						valores_posibles = []
						for v in val_id_list:
							valores_posibles.append(ValorPosible.objects.get(id=v))

						#valores_posibles = encuesta_data[aux]

						orden = 1
						valores_pregunta_exclude = []
						for valor in valores_posibles:
							if valor not in valores_pregunta:
								vpe = ValorPreguntaEncuesta(
									valor = valor, 
									pregunta = pregunta, 
									encuesta = encuesta,
									orden = orden)
								vpe.save()
							else:
								valor_pregunta_encuesta = ValorPreguntaEncuesta.objects.get(valor=valor, pregunta=pregunta, encuesta=encuesta)
								if valor_pregunta_encuesta.orden != orden:
									valor_pregunta_encuesta.orden = orden
									valor_pregunta_encuesta.save()

							orden = orden + 1
							valores_pregunta_exclude.append(valor.id)

						#Nota: hay que excluir para despues eliminar lo que sobra...
						valores_pregunta = valores_pregunta.exclude(id__in=valores_pregunta_exclude)
						for valor in valores_pregunta:
							vpe = ValorPreguntaEncuesta.objects.get(valor=valor, pregunta=pregunta, encuesta=encuesta)
							vpe.delete()

				encuesta_preguntas_exclude.append(pregunta.id)
			
			#Nota: hay que excluir para despues eliminar lo que sobra...
			encuesta_preguntas = encuesta_preguntas.exclude(id__in=encuesta_preguntas_exclude)
			for pregunta in encuesta_preguntas:
				valores_pregunta = ValorPosible.objects.filter(valor_pregunta_encuesta=pregunta)
				for valor in valores_pregunta:
					vpe = ValorPreguntaEncuesta.objects.get(valor=valor, pregunta=pregunta, encuesta=encuesta)
					vpe.delete()

				encuesta.preguntas.remove(pregunta)

			return redirect(reverse('admin_encuestas'))
		else:
			print form.errors
			return render(request, 'admin/crear_encuesta.html', self.get_context(encuesta, usuario, form))


class AdminEliminarEncuesta(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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
				'mensaje': 'No se suministró el id de la respuesta'
			}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class AdminBandejaNotificaciones(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminBandejaNotificaciones, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que lista las encuestas al administrador"""
		usuario = request.user

		notificaciones = Notificacion.objects.all()

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		paginator = Paginator(notificaciones, 10, request=request)
		notificaciones = paginator.page(page)

		context = {
			'admin': True,
			'seccion_notificaciones':True,
			'notificaciones': notificaciones,
			'usuario': usuario,
		}

		return render(request, 'admin/bandeja_notificaciones.html', context)


class AdminAgregarNotificacion(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminAgregarNotificacion, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Despliega el formulario para crear notificaciones"""
		usuario = request.user
		form = NotificacionForm()
		tipos_notificaciones = TipoNotificacion.objects.all()

		context = {
			'admin': True,
			'usuario': usuario,
			'form': form,
			'seccion_notificaciones': True,
			'tipos_notificaciones': tipos_notificaciones
		}

		return render(request, 'admin/crear_notificacion.html', context) #self.get_context(usuario)

	def post(self, request, *args, **kwargs):
		"""Crea el Perito"""
		usuario = request.user

		form = NotificacionForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect(reverse('admin_notificaciones'))

		else:
			print form.errors

			context = {
				'admin': True,
				'usuario': usuario,
				'form': form,
				'seccion_notificaciones': True
			}

			return render(request, 'admin/crear_notificacion.html', context)


class AdminEditarNotificacion(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminEditarNotificacion, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que despliega el formulario para editar notificaciones"""
		usuario = request.user
		notificacion = Notificacion.objects.filter(id=kwargs['notificacion_id']).first()
		tipos_notificaciones = TipoNotificacion.objects.all()
		
		if notificacion:
			form = NotificacionForm(instance = notificacion)

			context = {
				'admin': True,
				'usuario': usuario,
				'editar': True,
				'form': form,
				'notificacion_id': kwargs['notificacion_id'],
				'seccion_notificaciones': True,
				'tipos_notificaciones': tipos_notificaciones
			}

			return render(request, 'admin/crear_notificacion.html', context)

		else:
			return redirect(reverse('admin_notificaciones'))

	def post(self, request, *args, **kwargs):
		"""Edita la notificación"""
		usuario = request.user
		notificacion = Notificacion.objects.filter(id=kwargs['notificacion_id']).first()
		tipos_notificaciones = TipoNotificacion.objects.all()

		form = NotificacionForm(request.POST, instance = notificacion)

		if form.is_valid():
			form.save()
			return redirect(reverse('admin_notificaciones'))

		else:
			print form.errors
			context = {
				'admin': True,
				'usuario': usuario,
				'editar': True,
				'form': form,
				'perito_id': kwargs['notificaciones_id'],
				'seccion_notificaciones': True,
				'tipos_notificaciones': tipos_notificaciones
			}

			return render(request, 'admin/crear_notificacion.html', context)


class AdminEliminarNotificacion(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminEliminarNotificacion, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista que elimina un Centro de Inspección"""
		page = request.POST.get('page', None)
		print page
		notificacion_id = request.POST.get('notificacion_id', None)
		notificacion = Notificacion.objects.filter(id=notificacion_id)
		if notificacion:
			notificacion.delete()
			redirect_url = reverse('admin_notificaciones')
			if int(page) > 1:
				extra_params = '?page=%s' % page
				redirect_url = '%s%s' % (redirect_url, extra_params)

			return redirect(redirect_url, kwargs={'location': page})
		else:
			return redirect(redirect_url, kwargs={'location': page})


class AdminEnviarNotificacion(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminEnviarNotificacion, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Eliminar respuestas"""
		usuario = request.user
		notificacion_id = request.GET.get('notificacion_id', None)

		respuesta = {}
		if notificacion_id:
			notificacion = Notificacion.objects.get(id=notificacion_id)
			usuarios_clientes = SgtUsuario.objects.filter(rol__codigo = 'cliente')
			for usuario in usuarios_clientes:
				notificacion_usuario = NotificacionUsuario(notificacion=notificacion, usuario=usuario)
				notificacion_usuario.save()
			
			respuesta = {
				'mensaje': 'Notificación enviada exitosamente'
			}
		else:
			respuesta = {
				'mensaje': 'No se suministró el id de la notificación'
			}

		return HttpResponse(
		    json.dumps(respuesta),
		    content_type="application/json"
		)


class AdminReportes(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
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


class AdminEstadisticasEncuestas(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminEstadisticasEncuestas, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Método que muestra una estadística de las respuestas de los usuarios a las encuestas"""
		usuario = request.user
		encuestas = Encuesta.objects.all()

		context = {
			'admin': True,
			'encuestas': encuestas,
			'seccion_reporte': True,
			'usuario': usuario
		}

		return render(request, 'admin/estadisticas_encuestas.html', context)

	def post(self, request, *args, **kwargs):
		usuario = request.user
		encuestas = Encuesta.objects.all()
		encuesta_id = request.POST.get('encuesta', None)
		print "HEY",encuesta_id
		encuesta_seleccionada = Encuesta.objects.filter(id = encuesta_id).first()
		matriz = Encuesta.estadisticas(request.POST)

		context = {
			'admin': True,
			'encuesta_seleccionada': encuesta_seleccionada,
			'encuestas': encuestas,
			'encuesta_id': encuesta_id,
			'matriz': matriz,
			'seccion_reportes': True,
			'usuario': usuario
		}

		return render(request, 'admin/estadisticas_encuestas.html', context)


class EstadisticasEncuestasXls(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(EstadisticasEncuestasXls, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que genera el XLS de las estadísticas de las respuestas por encuesta"""
		filtros = {'encuesta': kwargs['encuesta']}

		matriz = Encuesta.estadisticas(filtros)

		response = HttpResponse(content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename=Consultas_solicitudes.xls'

		xls = Encuesta.generarEstadisticasEncuestasXls(matriz)
		xls.save(response)
		return response


class AdminEncuestasRespondidas(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminEncuestasRespondidas, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Bandeja para ver todas las encuesta resueltas"""
		usuario = request.user
		tipos_encuesta = TipoEncuesta.objects.all()
		encuestas = Encuesta.objects.all()
		url = ''

		encuestas_resueltas = NotificacionUsuario.encuestas_resueltas(request.GET)

		paginator = Paginator(encuestas_resueltas, 10, request=request)
		try:
			page = request.GET.get('page', 1)
			encuestas_resueltas = paginator.page(page)
		except PageNotAnInteger:
			encuestas_resueltas = paginator.page(1)
			page = 0
		except EmptyPage:
			encuestas_resueltas = paginator.page(paginator.num_pages)

		if encuestas_resueltas.object_list:
			usuario_nombres = request.GET.get('usuario_nombres', None)
			usuario_apellidos = request.GET.get('usuario_apellidos', None)
			tipo_encuesta = request.GET.get('tipo_encuesta', None)
			encuesta = request.GET.get('encuesta', None)
			if usuario_nombres:
				url += '&&usuario_nombres=%s' % usuario_nombres
			if usuario_apellidos:
				url += '&&usuario_apellidos=%s' % usuario_apellidos
			if tipo_encuesta:
				url += '&&tipo_encuesta=%s' % tipo_encuesta
			if encuesta:
				url += '&&encuesta=%s' % encuesta

		context = {
			'admin': True,
			'encuestas': encuestas,
			'encuestas_resueltas': encuestas_resueltas,
			'seccion_reportes': True,
			'tipos_encuesta': tipos_encuesta,
			'url': url,
			'usuario': usuario
		}

		return render(request, 'admin/encuestas_respondidas.html', context)

	def post(self, request, *args, **kwargs):
		"""Aplicación de filtros para las encuestas respondidas"""
		usuario = request.user
		tipos_encuesta = TipoEncuesta.objects.all()
		encuestas = Encuesta.objects.all()
		url = ''

		encuestas_resueltas = NotificacionUsuario.encuestas_resueltas(request.POST)

		paginator = Paginator(encuestas_resueltas, 10, request=request)
		try:
			page = request.GET.get('page', 1)
			encuestas_resueltas = paginator.page(page)
		except PageNotAnInteger:
			encuestas_resueltas = paginator.page(1)
			page = 0
		except EmptyPage:
			encuestas_resueltas = paginator.page(paginator.num_pages)

		if encuestas_resueltas.object_list:
			usuario_nombres = request.POST.get('usuario_nombres', None)
			usuario_apellidos = request.POST.get('usuario_apellidos', None)
			tipo_encuesta = request.POST.get('tipo_encuesta', None)
			encuesta = request.POST.get('encuesta', None)
			if usuario_nombres:
				url += '&&usuario_nombres=%s' % usuario_nombres
			if usuario_apellidos:
				url += '&&usuario_apellidos=%s' % usuario_apellidos
			if tipo_encuesta:
				url += '&&tipo_encuesta=%s' % tipo_encuesta
			if encuesta:
				url += '&&encuesta=%s' % encuesta

		context = {
			'admin': True,
			'encuestas': encuestas,
			'encuestas_resueltas': encuestas_resueltas,
			'filtros': request.POST,
			'seccion_reportes': True,
			'tipos_encuesta': tipos_encuesta,
			'url': url,
			'usuario': usuario
		}

		return render(request, 'admin/encuestas_respondidas.html', context)


class AdminVerEncuestaRespondida(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminVerEncuestaRespondida, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista para mostrar la encuesta respondida de un usuario"""
		usuario = request.user
		valores_posibles = {}
		notificacion_usuario_id = kwargs['notificacion_usuario_id']
		notificacion_usuario = NotificacionUsuario.objects.filter(id=notificacion_usuario_id).first()
		if notificacion_usuario and notificacion_usuario.notificacion.encuesta:
			respuestas = {}
			encuesta = notificacion_usuario.notificacion.encuesta
			preguntas = encuesta.preguntas.all()
			valores_preguntas_encuesta = ValorPreguntaEncuesta.objects.filter(encuesta= encuesta, pregunta__in = preguntas).order_by('pregunta','orden')
			for p in preguntas:
				#Para agregar la respuesta
				resp = Respuesta.objects.filter(pregunta = p, usuario = notificacion_usuario.usuario, notificacion_usuario = notificacion_usuario).first()
				print "R--", resp.respuestadefinida_set.all()
				if resp.pregunta.tipo_respuesta.codigo == 'RESP_DEF':
					respuestas[p.pk] = resp.respuestadefinida_set.all().first().valor_definido.pk
				elif resp.pregunta.tipo_respuesta.codigo == 'RESP_INDEF':
					respuestas[p.pk] = resp.respuestaindefinida_set.all().first().valor_indefinido
				
				#Para agregar los valores preguntas encuesta
				valores_posibles[p.pk] = [vp for vp in valores_preguntas_encuesta if vp.pregunta == p]

			print "RESPUESTAS", respuestas
			context = {
				'admin': True,
				'preguntas': preguntas,
				'respuestas': respuestas,
				'seccion_reportes': True,
				'usuario': usuario,
				'valores_posibles': valores_posibles
			}

			return render(request, 'admin/ver_encuesta_respondida.html', context)



class BandejaTaquilla(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(BandejaTaquilla, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Bandeja con las solicitudes para el dia corriente"""
		usuario = request.user
		today = datetime.today().date()
		print usuario,today
		numeros_orden = NumeroOrden.objects.filter(fecha_atencion = today, solicitud_inspeccion__centro_inspeccion = usuario.centro_inspeccion).exclude(solicitud_inspeccion__estatus__codigo = 'solicitud_cancelada').order_by('hora_atencion')
		peritos = Perito.objects.filter(centroinspeccion = usuario.centro_inspeccion)
		print peritos
		context = {
			'numeros_orden': numeros_orden,
			'peritos': peritos,
			'usuario': usuario
		}

		return render(request, 'taquilla/bandeja.html', context)


class TaquillaAccionSolicitud(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(TaquillaAccionSolicitud, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista que cambia el estatus de las solicitudes por la Taquilla"""
		valido = False
		error_msg = None
		tipo_operacion = request.POST.get('tipo_operacion', None)
		id_numero_orden = request.POST.get('id_numero_orden', None)
		id_perito = request.POST.get('id_perito', None)
		numero_orden = NumeroOrden.objects.filter(id=id_numero_orden).first()

		if tipo_operacion == 'confirmar_asistencia':
			perito = Perito.objects.filter(id=id_perito).first()
			if not numero_orden.solicitud_inspeccion.estatus.codigo=='solicitud_en_proceso':
				error_msg = 'Esta solicitud ya fue procesada'
			
			elif numero_orden and perito:
				valido = True
				numero_orden.asistencia = 1
				numero_orden.solicitud_inspeccion.perito = perito
				numero_orden.solicitud_inspeccion.estatus = Estatus.objects.get(codigo = 'solicitud_procesada')
				numero_orden.solicitud_inspeccion.save()
				numero_orden.save()
				#Enviar la notificación de asistencia al usuario
				cliente = numero_orden.solicitud_inspeccion.usuario
				notificacion = Notificacion.objects.filter(encuesta__tipo_encuesta__codigo = 'ENC_CONF').first()
				notificacion_usuario = NotificacionUsuario(notificacion=notificacion, usuario=cliente)
				notificacion_usuario.save()

			else:
				error_msg = 'Falta algún parámetro'

		else:
			if not numero_orden.solicitud_inspeccion.estatus.codigo=='solicitud_en_proceso':
				error_msg = 'Esta solicitud ya fue procesada'

			elif numero_orden:
				valido = True
				numero_orden.solicitud_inspeccion.estatus = Estatus.objects.get(codigo = 'solicitud_no_procesada')
				numero_orden.solicitud_inspeccion.save()

			else:
				error_msg = 'Falta algún parámetro'

		return HttpResponse(
		    json.dumps({
		    	'valido': valido,
		    	'error_msg': error_msg,
		    	'numero_orden': numero_orden.toDict(True) if numero_orden else None
		    }),
		    content_type="application/json"
		)


class ReporteXls(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(ReporteXls, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que genera el XLS de los reportes"""
		filtros = {}
		if request.session.has_key('filtros_reporte'):
			filtros = request.session['filtros_reporte']

		numeros_orden = NumeroOrden.reporte(filtros)

		response = HttpResponse(content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename=Consultas_solicitudes.xls'

		xls = NumeroOrden.generarReporteXls(numeros_orden)
		xls.save(response)
		return response


class CargaMasivaCentros(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(CargaMasivaCentros, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista que se encarga de la carga masiva de centros provenientes de un xls"""
		valido = False
		error_msg = None
		if request.FILES.has_key('archivo_centros'):
			xlsx_centros = request.FILES['archivo_centros']
			if utils.cargar_centros_desde_xls(xlsx_centros):
				valido = True
			else:
				error_msg = 'Ha ocurrido un error con el archivo'

		else:
			error_msg = 'No se ha enviado ningún archivo'

		return HttpResponse(
		    json.dumps({
		    	'valido': valido,
		    	'error_msg': error_msg,
		    }),
		    content_type="application/json"
		)


class CargaMasivaPolizas(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(CargaMasivaPolizas, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Vista que se encarga de la carga masiva de polizas provenientes de un xls"""
		valido = False
		error_msg = None
		if request.FILES.has_key('archivo_polizas'):
			xlsx_polizas = request.FILES['archivo_polizas']
			if utils.cargar_polizas_desde_xls(xlsx_polizas):
				valido = True
			else:
				error_msg = 'Ha ocurrido un error con el archivo'

		else:
			error_msg = 'No se ha enviado ningún archivo'

		return HttpResponse(
		    json.dumps({
		    	'valido': valido,
		    	'error_msg': error_msg,
		    }),
		    content_type="application/json"
		)


class AdminParametros(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, *args, **kwargs):
		return super(AdminParametros, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Vista que muestra el formulario para los parámetros generales de la aplicación"""
		usuario = request.user

		context = {
			'admin': True,
			'seccion_parametros': True,
			'usuario': usuario
		}

		return render(request, 'admin/parametros.html', context)


class ConsultarNotificacion(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, request, *args, **kwargs):
		return super(ConsultarNotificacion, self).dispatch(request, *args, **kwargs)
        
	def get(self, request, *args, **kwargs):
		"""Consultar Notificación"""
		usuario = request.user
		notificacion_usuario_id = request.GET.get('notificacion_usuario_id', None)

		respuesta = {}
		if notificacion_usuario_id:
			notificacion_usuario = NotificacionUsuario.objects.get(id=notificacion_usuario_id)

			if not notificacion_usuario.leida:
				notificacion_usuario.leida = True
				notificacion_usuario.save()

			if notificacion_usuario.notificacion.encuesta:
				encuesta_id = notificacion_usuario.notificacion.encuesta.id
			else:
				encuesta_id = None

			respuesta = {
				'asunto': notificacion_usuario.notificacion.asunto,
				'mensaje':  notificacion_usuario.notificacion.mensaje,
				'encuesta_id':  encuesta_id,
				'fecha_creacion':  notificacion_usuario.fecha_creacion.strftime('%d/%m/%Y'),
 			}

		else:
			respuesta['mensaje'] = 'No se suministró el id de la notificación'


 		return HttpResponse(
			json.dumps(respuesta),
			content_type="application/json"
		)

class ConsultarEncuesta(View):
	@method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
	def dispatch(self, request, *args, **kwargs):
	    return super(ConsultarEncuesta, self).dispatch(request, *args, **kwargs)
	    
	def get(self, request, *args, **kwargs):
	    """Consultar Encuesta"""
	    usuario = request.user
	    encuesta_id = request.GET.get('encuesta_id', None)

	    respuesta = {}
	    if encuesta_id:
	    	encuesta = Encuesta.objects.get(id=encuesta_id)
	    	preguntas = encuesta.preguntas.all()

	    	valores_preguntas_definidas = {}
	    	preguntas_definidas = preguntas.exclude(tipo_respuesta__codigo="RESP_INDEF")
	    	for p in preguntas_definidas:
	    		aux = ValorPreguntaEncuesta.objects.filter(pregunta=p, encuesta=encuesta).order_by('orden')
	    		valores_preguntas_definidas[p.id] = [ {'id': vals.valor.id, 'valor': vals.valor.valor} for vals in aux ]

	    	preguntas = [ {'id': preg.id, 'enunciado': preg.enunciado, 'tipo_respuesta': preg.tipo_respuesta.codigo} for preg in preguntas ]

	    	respuesta = {
	    		'preguntas': preguntas,
	    		'nombre_encuesta': encuesta.nombre, 
	    		'valores_preguntas_definidas': valores_preguntas_definidas,
	        }
	    else:
	        respuesta['mensaje'] = 'No se suministró el id de la notificación'


	    return HttpResponse(
	        json.dumps(respuesta),
	        content_type="application/json"
	    )

	def post(self, request, *args, **kwargs):
		""" Guardar respuestas de la encuesta """
		mensaje = {}
		data = request.POST

		if data:
			usuario = request.user
			encuesta_id = data.get('encuesta')
			encuesta = Encuesta.objects.get(id=encuesta_id)
			notificacion_usuario_id = data.get('notificacion_usuario')
			notificacion_usuario = NotificacionUsuario.objects.get(id=notificacion_usuario_id)

			total_preguntas = data.get('total_preguntas')
			for index in range(int(total_preguntas)):
				aux = 'pregunta_' + str(index + 1)
				pregunta_id = data.get(aux)
				pregunta = Pregunta.objects.get(pk=pregunta_id)
				tipo_respuesta = pregunta.tipo_respuesta.codigo
				respuesta = Respuesta(encuesta=encuesta, pregunta=pregunta, usuario=usuario, notificacion_usuario = notificacion_usuario)
				respuesta.save()

				if tipo_respuesta == "RESP_DEF":
					aux = 'respuesta_def_' + pregunta_id
					valor_def_id = data.get(aux)
					valor_def = ValorPosible.objects.get(id=valor_def_id)
					respuesta_definida = RespuestaDefinida(respuesta=respuesta, valor_definido=valor_def)
					respuesta_definida.save()

				elif tipo_respuesta == "RESP_INDEF":
					aux = 'respuesta_indef_' + pregunta_id
					valor_indef = data.get(aux)
					respuesta_indefinida = RespuestaIndefinida(respuesta=respuesta, valor_indefinido=valor_indef)
					respuesta_indefinida.save()

			# notificacion_usuario = NotificacionUsuario.objects.get(id=notificacion_usuario_id)
			notificacion_usuario.borrada = True
			notificacion_usuario.encuesta_respondida = True
			notificacion_usuario.save()

			mensaje['mensaje'] = 'Respuestas guardadas de manera exitosa'
		else:
			mensaje['mensaje'] = 'No se proporcioron las respuestas solicitadas'

		return HttpResponse(
		    json.dumps(mensaje),
		    content_type="application/json"
		)