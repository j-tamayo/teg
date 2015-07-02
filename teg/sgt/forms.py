# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from sgt.models import Estado, Municipio, TipoInspeccion, CentroInspeccion

class SolicitudInspeccionForm(forms.Form):
	""" Formulario para la solicitud de inspecciones """
	centros_inspeccion = CentroInspeccion.objects.all()

	tipo_solicitud = forms.ModelChoiceField(
		label = u'Tipo de solicitud',
		queryset = TipoInspeccion.objects.all().order_by('nombre'),
		widget = forms.Select(attrs={'class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	fecha_asistencia = forms.DateField(
		label = u'Fecha de solicitud',
		widget = forms.TextInput(attrs={'class':'col-xs-10','required':'','readonly':'','data-error':'Este campo es obligatorio'})
	)

	estado = forms.ModelChoiceField(
		label = u'Estado',
		queryset = Estado.objects.filter(municipio__centroinspeccion__in = centros_inspeccion).distinct('nombre').order_by('nombre'),
		widget = forms.Select(attrs={'id':'select_solicitud_estado','class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	municipio = forms.ModelChoiceField(
		label = u'Municipio',
		queryset = Municipio.objects.all(),
		widget = forms.Select(attrs={'class':'form-control'})
	)

	centro_inspeccion = forms.ModelChoiceField(
		label = u'Centro de inspección',
		queryset = CentroInspeccion.objects.filter(),
		widget = forms.Select(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)


class CentroInspeccionForm(forms.ModelForm):
	class Meta:
		model = CentroInspeccion
		fields = ['codigo','nombre','direccion','telefonos','municipio','peritos','hora_apertura_manana','hora_cierre_manana','hora_apertura_tarde','hora_cierre_tarde']
		widgets = {
			'codigo': forms.TextInput(attrs={'class':'form-control'}),
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'hora_apertura_manana': forms.TextInput(attrs={'class':'timepicker','readonly':True})
		}