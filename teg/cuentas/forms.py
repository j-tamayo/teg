# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate

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
		print self.cleaned_data
		correo = self.cleaned_data.get('correo')
		password = self.cleaned_data.get('password')
		usuario = authenticate(correo=correo, password=password)
		# print usuario
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
	nombres = forms.CharField(
		label=u'Nombre',
		widget=forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	apellidos = forms.CharField(
		label=u'Apellidos',
		widget=forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)

	cedula = forms.CharField(
		label=u'Cédula',
		widget=forms.TextInput(attrs={'class':'form-control','required':'','data-error':'Este campo es obligatorio'})
	)