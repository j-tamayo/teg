# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from sgt.models import Estado, Municipio, TipoInspeccion, CentroInspeccion, Perito, Pregunta, TipoRespuesta, ValorPosible
from datetime import datetime

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
	hora_apertura_manana = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control timepicker','required':True,'readonly':True}))
	hora_cierre_manana = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control timepicker','required':True,'readonly':True}))
	hora_apertura_tarde = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control timepicker','required':True,'readonly':True}))
	hora_cierre_tarde = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control timepicker','required':True,'readonly':True}))
	peritos = forms.ModelMultipleChoiceField(queryset=Perito.objects.all(), required=False)

	class Meta:
		model = CentroInspeccion
		fields = ['codigo','nombre','direccion','telefonos','municipio','hora_apertura_manana','hora_cierre_manana','hora_apertura_tarde','hora_cierre_tarde']
		widgets = {
			'codigo': forms.TextInput(
				attrs={
					'class':'form-control',
					'required':'',
					'data-error':'Este campo es obligatorio'
				}
			),
			'nombre': forms.TextInput(
				attrs={
					'class':'form-control', 
					'required':True,
					'data-error':'Este campo es obligatorio'
				}
			),
			'direccion': forms.Textarea(
				attrs={
					'class':'form-control', 
					'required':True
				}
			),
			'telefonos': forms.TextInput(
				attrs={
					'class':'form-control',
					'required':True,
				}
			)
		}

	def save(self):
		instance = forms.ModelForm.save(self)
		print "HEYY",instance.municipio
		peritos = self.cleaned_data.get('peritos', None)
		for perito in peritos:
			instance.peritos.add(perito)

	def clean_hora_apertura_manana(self):
		field = self.cleaned_data.get('hora_apertura_manana', None)
		if field:
			print field
			field = datetime.strptime(field,'%I:%M %p').time()

			return field

	def clean_hora_cierre_manana(self):
		field = self.cleaned_data.get('hora_cierre_manana', None)
		if field:
			print field
			field = datetime.strptime(field,'%I:%M %p').time()

			return field

	def clean_hora_apertura_tarde(self):
		field = self.cleaned_data.get('hora_apertura_tarde', None)
		if field:
			print field
			field = datetime.strptime(field,'%I:%M %p').time()

			return field

	def clean_hora_cierre_tarde(self):
		field = self.cleaned_data.get('hora_cierre_tarde', None)
		if field:
			print field
			field = datetime.strptime(field,'%I:%M %p').time()

			return field


class CrearEncuestaForm(forms.Form):
	nombre = forms.CharField(
		label = u'Nombre',
		widget = forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	descripcion = forms.CharField(
		label = u'Descripción',
		widget = forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	enunciado = forms.ModelMultipleChoiceField(
		label = u'Pregunta',
		queryset = Pregunta.objects.all(),
		widget = forms.Select(attrs={'class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	tipo_respuesta = forms.ModelChoiceField(
		label = u'Tipo de respuesta',
		queryset = TipoRespuesta.objects.all(),
		widget = forms.Select(attrs={'class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	valores_posiples = forms.ModelMultipleChoiceField(
		label = u'Valor',
		queryset = ValorPosible.objects.all(),
		widget = forms.Select(attrs={'class':'form-control'})
	)