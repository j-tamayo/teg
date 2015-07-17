# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from sgt.models import Estado, Municipio, TipoInspeccion, CentroInspeccion, Perito, TipoEncuesta, Pregunta, TipoRespuesta, ValorPosible
from datetime import datetime
from django.core.exceptions import ValidationError

import string

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
		peritos = self.cleaned_data.get('peritos', [])
		peritos_viejos = instance.peritos.all()
		peritos_to_del = set(peritos_viejos).difference(set(peritos))
		peritos_to_add = set(peritos).difference(set(peritos_viejos))
		#Eliminamos los peritos removidos en el formulario
		for p in peritos_to_del:
			# print "perito elim",p.pk,p
			instance.peritos.remove(p)

		# print peritos
		#Agregamos los peritos nuevos
		for perito in peritos_to_add:
			instance.peritos.add(perito)
			# print perito.pk,perito.nombres

	def clean_hora_apertura_manana(self):
		field = self.cleaned_data.get('hora_apertura_manana', None)
		if field:
			print field
			field = datetime.strptime(field,'%H:%M').time()

			return field

	def clean_hora_cierre_manana(self):
		field = self.cleaned_data.get('hora_cierre_manana', None)
		if field:
			print field
			field = datetime.strptime(field,'%H:%M').time()

			return field

	def clean_hora_apertura_tarde(self):
		field = self.cleaned_data.get('hora_apertura_tarde', None)
		if field:
			print field
			field = datetime.strptime(field,'%H:%M').time()

			return field

	def clean_hora_cierre_tarde(self):
		field = self.cleaned_data.get('hora_cierre_tarde', None)
		if field:
			print field
			field = datetime.strptime(field,'%H:%M').time()

			return field


class PeritoForm(forms.ModelForm):
	fecha_ingreso = forms.DateField(
		widget=forms.DateInput(
			format = '%d/%m/%Y',
			attrs={'class':'col-xs-11','readonly':True}
		)
	)

	class Meta:
		model = Perito
		fields = ['nombres','apellidos','cedula','fecha_ingreso','sexo']
		widgets = {
			'nombres':forms.TextInput(
				attrs = {'class':'form-control'}
			),
			'apellidos':forms.TextInput(
				attrs = {'class':'form-control'}
			),
			'cedula':forms.TextInput(
				attrs = {'class':'form-control'}
			)
		}

	# def clean_fecha_ingreso(self):
	# 	field = self.cleaned_data.get('fecha_ingreso', None)
	# 	if field:
	# 		field = datetime.strptime(field, '%d/%m/%Y').date()

	# 		return field


def validate_extra_field(value):

	if string.atoi(value) <= 0:
		raise ValidationError('Debe agregar al menos 1 pregunta')

class CrearEncuestaForm(forms.Form):
	nombre = forms.CharField(
		label = u'Nombre',
		widget = forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	descripcion = forms.CharField(
		label = u'Descripción',
		widget = forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	tipo_encuesta = forms.ModelChoiceField(
		label = u'Tipo de encuesta',
		queryset = TipoEncuesta.objects.all(),
		empty_label = None,
		widget = forms.Select(attrs={'class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)
	
	extra_field_count = forms.CharField(widget=forms.HiddenInput(), required=True, validators=[validate_extra_field])
	
	def __init__(self, *args, **kwargs):
		extra_fields = kwargs.pop('extra', 0)
		print extra_fields

		super(CrearEncuestaForm, self).__init__(*args, **kwargs)
		self.fields['extra_field_count'].initial = extra_fields

		for index in range(int(extra_fields)):
			self.fields['pregunta_{index}'.format(index=index+1)] = forms.ModelChoiceField(
				label = u'Pregunta:',
				queryset = Pregunta.objects.all(), 
				required = True,
				empty_label = None,
				widget = forms.Select(attrs={
					'id': 'id_pregunta_{index}'.format(index=index+1), 
					'class': 'form-control chosen-select pregunta_select',
					'required': '',
					'data-error': 'Este campo es obligatorio',
					'data-placeholder': 'Seleccione una pregunta...'
				})
			)

			self.fields['tipo_respuesta_{index}'.format(index=index+1)] = forms.ModelChoiceField(
				label = u'Tipo de respuesta:',
				queryset = TipoRespuesta.objects.all(), 
				required = True,
				empty_label = None, 
				widget = forms.Select(attrs={
					'id': 'id_tipo_respuesta_{index}'.format(index=index+1), 
					'class': 'form-control tipo_respuesta_select',
					'required': '',
					'data-error': 'Este campo es obligatorio',
					'target': 'id_pregunta_{index} id_respuestas_definidas_{index}'.format(index=index+1)
				})
			)

			self.fields['valores_posibles_{index}'.format(index=index+1)] = forms.ModelMultipleChoiceField(
				label = u'Respuesta:',
				queryset = ValorPosible.objects.all(), 
				required = False,
				widget=forms.SelectMultiple(attrs={
					'id': 'id_valor_{index}'.format(index=index+1), 
					'class': 'form-control select-mul respuesta_select',
					'data-error': 'Este campo es obligatorio',
					'data-placeholder': 'Seleccione la respuesta...' 
				})
			)

	def clean(self):
		extra_fields = self.cleaned_data.get('extra_field_count', 0)
		
		for index in range(int(extra_fields)):
			aux = 'tipo_respuesta_' + str(index + 1)
			tipo_respuesta = self.cleaned_data.get(aux)

			aux = 'valores_posibles_' + str(index + 1)
			valores_posibles = self.cleaned_data.get(aux)

			if tipo_respuesta.codigo == 'RESP_DEF' and not valores_posibles:
				msg = u'Las preguntas con respuestas definidas deben tener al menos una respuesta asignada'
				raise forms.ValidationError(msg)

		return self.cleaned_data


class CrearPreguntaForm(forms.Form):
	enunciado = forms.CharField(
		label = u'Pregunta',
		widget = forms.TextInput(attrs={'id':'nueva_pregunta', 'class':'form-control', 'required':'', 'data-error':'Este campo es obligatorio'})
	)

	tipo_respuesta = forms.ModelChoiceField(
		label = u'Tipo de respuesta',
		queryset = TipoRespuesta.objects.all(),
		widget = forms.Select(attrs={'class':'form-control', 'required': '', 'data-error':'Este campo es obligatorio'})
	)

class CrearValorForm(forms.Form):
	valor = forms.CharField(
		label = u'Respuesta',
		widget = forms.TextInput(attrs={'id':'nuevo_valor', 'class':'form-control', 'required':'', 'data-error':'Este campo es obligatorio'})
	)