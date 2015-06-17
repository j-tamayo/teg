# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from sgt.models import *
from sgt.forms import *
from sgt.helpers import solicitudes,dates

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

		fecha_asistencia = dates.convert(fecha_asistencia, '%d/%m/%Y', '%Y-%m-%d')
		#Falta calcular Informacion para generar numero de orden y hora de asistencia...
		horarios = solicitudes.generar_horarios(centro_inspeccion)

		centro.append({
			'nombre': centro_inspeccion.nombre,
			'estado': centro_inspeccion.municipio.estado.nombre,
			'municipio': centro_inspeccion.municipio.nombre,
			#'fecha_asistencia': ,
			#'numer_orden': ,
			#'hora_asistencia':
		})
		centro = json.dumps(centro)
		print centro

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
		form = SolicitudInspeccionForm(request.GET)
		if form.is_valid():
			datos = form.cleaned_data
			


class BandejaCliente(View):
	def dispatch(self, *args, **kwargs):
		return super(BandejaCliente, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		""" Vista que maneja la bandeja del usuario común """
		usuario = request.user
		tipo_solicitudes = TipoInspeccion.objects.all()
		form = SolicitudInspeccionForm(request.POST)
		poliza = Poliza.objects.filter(usuario = usuario).first()

		context = {
		    'usuario': usuario,
		    'tipo_solicitudes': tipo_solicitudes,
		    'form': form,
		    'poliza': poliza
		}

		return render(request,'cuentas/perfil_cliente.html', context)