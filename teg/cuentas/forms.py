# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate

class AutenticacionUsuarioForm(forms.Form):
	""" Formulario para la autenticación de los usuarios """
	correo = forms.EmailField(
        label=u'Correo electrónico',
    )

	password = forms.CharField(
		label=u'Contraseña',
		widget=forms.PasswordInput(render_value=False)
	)

	def clean(self):
	    correo = self.cleaned_data['correo<']
	    password = self.cleaned_data['password']
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