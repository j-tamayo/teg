# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from sgt.models import CentroInspeccion, Estado, Municipio, TipoInspeccion
from cuentas.models import SgtUsuario
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
import threading
from django.conf import settings

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
	id = None
	edicion = 0
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
		widget=forms.TextInput(attrs={'class':'form-control'}),
		required = False
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
		widget = forms.TextInput(attrs={'class':'form-control'}),
		required = False
	)

	direccion = forms.CharField(
		label = u'Dirección',
		widget = forms.Textarea(attrs={'class':'form-control'}),
		required = False
	)

	correo = forms.EmailField(
		label = u'Correo',
		widget = forms.EmailInput(attrs={'class':'form-control','required':'','data-error':'El formato de correo es inválido'})
	)

	password = forms.CharField(
		label = u'Contraseña',
		widget = forms.PasswordInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'}),
		required = False
	)

	password_confirm = forms.CharField(
		label = u'Contraseña',
		widget = forms.PasswordInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'}),
		required = False
	)

	sexo = forms.ChoiceField(
		label  = u'Sexo',
		choices = sex_choices,
		widget = forms.RadioSelect(attrs={'class':'form-control'}),
		required = False
	)

	telefono_local = forms.CharField(
		label = u'Teléfono local',
		widget = forms.TextInput(attrs={'class':'form-control'}),
		required = False
	)

	telefono_movil = forms.CharField(
		label = u'Teléfono móvil',
		widget = forms.TextInput(attrs={'class':'form-control'}),
		required = False
	)

	fecha_nacimiento = forms.DateField(
		label = u'Fecha de nacimiento',
		widget = forms.DateInput(
			format = '%d/%m/%Y',
			attrs={'class':'col-xs-9'},
		),
		required = False
	)

	centro_inspeccion = forms.ModelChoiceField(
		label = u'Centro de inspección',
		queryset = CentroInspeccion.objects.all().order_by('nombre'),
		widget = forms.Select(attrs={'class':'form-control'}),
		required = False
	)

	def __init__(self, *args, **kwargs):
		self.taquilla = kwargs.pop('taquilla', 0)
		self.id = kwargs.pop('id_usuario', None)
		self.edicion = kwargs.pop('edicion', 0)
		super(RegistroForm, self).__init__(*args, **kwargs)

	def clean_password_confirm(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password_confirm')

		if self.edicion == 0:
			if not password2:
				raise forms.ValidationError(u'Este campo es obligatorio')

			if password1 != password2:
				raise forms.ValidationError(u'Las contraseñas deben conincidir')

		return password2

	# def clean_correo(self):
	# 	correo = self.cleaned_data.get('correo')
	# 	usuario = SgtUsuario.objects.filter(correo = correo)
	# 	if self.id:
	# 		if usuario and usuario.pk !=self.id:
	# 			raise forms.ValidationError(u'Este correo ya está asociado a otro usuario')

	# 	else:
	# 		if usuario:
	# 			raise forms.ValidationError(u'Este correo ya está registrado')

	# 	return correo

	def clean(self):
		cleaned_data = super(RegistroForm, self).clean()
		centro_inspeccion = cleaned_data.get('centro_inspeccion', None)
		cedula = cleaned_data.get('cedula', None)
		codigo_postal = cleaned_data.get('codigo_postal', None)
		direccion = cleaned_data.get('direccion', None)
		sexo = cleaned_data.get('sexo', None)
		fecha_nacimiento = cleaned_data.get('fecha_nacimiento', None)
		if self.taquilla > 0:
			if not centro_inspeccion:
				self.add_error('centro_inspeccion', u'Este campo es obligatorio')
			if not cedula:
				self.add_error('cedula', u'Este campo es obligatorio')
			if not codigo_postal:
				self.add_error('codigo_postal', u'Este campo es obligatorio')
			if not direccion:
				self.add_error('direccion', u'Este campo es obligatorio')
			if not sexo:
				self.add_error('sexo', u'Este campo es obligatorio')
			if not fecha_nacimiento:
				self.add_error('fecha_nacimiento', u'Este campo es obligatorio')

		correo = self.cleaned_data.get('correo')
		usuario = SgtUsuario.objects.filter(correo = correo).first()
		if self.id:
			if usuario and usuario.pk !=self.id:
				self.add_error('correo', u'Este correo ya está asociado a otro usuario')

		else:
			if usuario:
				self.add_error('correo', u'Este correo ya está registrado')



class RecuperarClaveForm(forms.Form):
	"""Formulario para recuperar la contraseña"""
	correo = forms.EmailField(
		label = u'Correo',
		widget = forms.EmailInput(attrs={'class':'form-control'})
	)

	def clean(self):
		correo = self.cleaned_data.get('correo')
		usuario = SgtUsuario.objects.filter(correo = correo).first()
		if correo and not usuario:
			raise forms.ValidationError(u'Este correo no se encuentra registrado')

		return self.cleaned_data

	def correoRecuperacion(self, contenido):
	    correo = self.cleaned_data.get('correo')
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