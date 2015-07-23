# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from sgt.models import CentroInspeccion, Estado, Municipio, TipoInspeccion

class AutenticacionUsuarioForm(forms.Form):
	""" Formulario para la autenticación de los usuarios """
	correo = forms.EmailField(
        label=u'Correo electrónico',
        widget=forms.EmailInput(
        	attrs={
        		'class':'form-control', 
        		'placeholder': 'Correo electrónico...', 
        		'required':'',
        		'data-error':'El formato de correo es inválido'
        	}
        )
    )

	password = forms.CharField(
		label=u'Contraseña',
		widget=forms.PasswordInput(
			render_value=False,
			attrs={'class':'form-control', 'placeholder': 'Contraseña...'}
		)
	)

	def clean(self):
		correo = self.cleaned_data.get('correo')
		password = self.cleaned_data.get('password')
		usuario = authenticate(correo=correo, password=password)
		if not usuario:
			msg = u'La combinación correo electrónico y contraseña son incorrectos.'
			raise forms.ValidationError(msg)

		elif not usuario.is_active and usuario.activation_key:
		    msg = u'La cuenta que esta intentando utilizar aún no se ha activado ' \
		          u'por favor ingrese a su correo para conocer los detalles para activar la misma'
		    raise forms.ValidationError(msg)

		elif not usuario.is_active:
		    msg = u'La cuenta que esta intentando utilizar se encuentra desactivada ' \
		          u'por favor contacte al personal administrativo para resolver este incidente.'
		    raise forms.ValidationError(msg)

		return self.cleaned_data


class RegistroForm(forms.Form):
	""" Formulario para el registro de usuarios """
	sex_choices = [('0','Masculino'),('1','Femenino')]
	taquilla = forms.DecimalField(widget=forms.HiddenInput(), required = False)

	nombres = forms.CharField(
		label = u'Nombre',
		widget=forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	apellidos = forms.CharField(
		label = u'Apellidos',
		widget=forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	cedula = forms.CharField(
		label = u'Cédula',
		widget=forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	estado = forms.ModelChoiceField(
		label = u'Estado',
		queryset = Estado.objects.all().order_by('nombre'),
		widget = forms.Select(attrs={'class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	municipio = forms.ModelChoiceField(
		label = u'Municipio',
		queryset = Municipio.objects.all(),
		widget = forms.Select(attrs={'class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	codigo_postal = forms.IntegerField(
		label = u'Código postal',
		widget = forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	direccion = forms.CharField(
		label = u'Dirección',
		widget = forms.Textarea(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	correo = forms.EmailField(
		label = u'Correo',
		widget = forms.EmailInput(attrs={'class':'form-control','required':'','data-error':'El formato de correo es inválido'})
	)

	password = forms.CharField(
		label = u'Contraseña',
		widget = forms.PasswordInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	password_confirm = forms.CharField(
		label = u'Contraseña',
		widget = forms.PasswordInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	sexo = forms.ChoiceField(
		label  = u'Sexo',
		choices = sex_choices,
		widget = forms.RadioSelect(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	telefono_local = forms.CharField(
		label = u'Teléfono local',
		widget = forms.TextInput(attrs={'class':'form-control'})
	)

	telefono_movil = forms.CharField(
		label = u'Teléfono móvil',
		widget = forms.TextInput(attrs={'class':'form-control'})
	)

	fecha_nacimiento = forms.DateField(
		label = u'Fecha de nacimiento',
		widget = forms.DateInput(
			format = '%d/%m/%Y',
			attrs={'class':'col-xs-10','required':'','readonly':'','data-error':'Este campo es obligatorio'},
		)
	)

	centro_inspeccion = forms.ModelChoiceField(
		label = u'Centro de inspección',
		queryset = CentroInspeccion.objects.all().order_by('nombre'),
		widget = forms.Select(attrs={'class':'form-control'}),
		required = False
	)

	def __init__(self, *args, **kwargs):
		self.taquilla = kwargs.pop('taquilla', 0)
		super(RegistroForm, self).__init__(*args, **kwargs)

	def clean_password_confirm(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password_confirm')

		if not password2:
			raise forms.ValidationError(u'Este campo es obligatorio')

		if password1 != password2:
			raise forms.ValidationError(u'Las contraseñas deben conincidir')

		return password2

	def clean(self):
		cleaned_data = super(RegistroForm, self).clean()
		centro_inspeccion = cleaned_data.get('centro_inspeccion', None)
		if self.taquilla > 0 and not centro_inspeccion:
			self.add_error('centro_inspeccion', 'Este campo es obligatorio')


class SolicitudInspeccionForm(forms.Form):
	""" Formulario para la solicitud de inspecciones """
	tipo_solicitud = forms.ModelChoiceField(
		label = u'Tipo de solicitud',
		queryset = TipoInspeccion.objects.all().order_by('nombre'),
		widget = forms.Select(attrs={'class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	estado = forms.ModelChoiceField(
		label = u'Estado',
		queryset = Estado.objects.all().order_by('nombre'),
		widget = forms.Select(attrs={'id':'select_solicitud_estado','class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	municipio = forms.ModelChoiceField(
		label = u'Municipio',
		queryset = Municipio.objects.all(),
		widget = forms.Select(attrs={'class':'form-control','required': '','data-error':'Este campo es obligatorio'})
	)

	fecha_asistencia = forms.DateField(
		label = u'Fecha de asistencia',
		widget = forms.TextInput(attrs={'class':'col-xs-10','required':'','readonly':'','data-error':'Este campo es obligatorio'})
	)

	centros_inspeccion = forms.ChoiceField(
		choices = CentroInspeccion.objects.all(),
		widget = forms.RadioSelect(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)