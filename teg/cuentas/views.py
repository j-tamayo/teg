# -*- coding: utf-8 -*-
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic import View, FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from cuentas.forms import *

# Create your views here.
class Ingresar(FormView):
	# TODO mostrar mensaje de bienvenida al Sistema
	form_class = AutenticacionUsuarioForm
	template_name = 'cuentas/ingresar.html'
	success_url = reverse_lazy('cuentas_detectar_usuario')

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			print request.user
			return redirect(reverse_lazy('cuentas_logout'))

		return super(Ingresar, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		correo = form.cleaned_data['correo']
		password = form.cleaned_data['password']

		usuario = authenticate(correo=correo, password=password)
		login(self.request, usuario)

		return super(IngresarView, self).form_valid(form)


class Registro(View):
    def dispatch(self, request, *args, **kwargs):
    	return super(Registro, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
    	return render(request,'cuentas/registro.html')

    def post(self, request, *args, **kwargs):
    	pass


class Salir(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
            mensaje = u'¡Ha cerrado sesión correctamente!'
            messages.info(self.request, mensaje)

        return redirect(reverse_lazy('cuentas_login'))


class DetectarUsuario(LoginRequiredMixin, View):
	def dispatch(self, request, *args, **kwargs):
		usuario = request.user

		if usuario.is_authenticated():
			pass

		elif usuario.is_authenticated() and not usuario.is_active:
			pass

		return redirect(reverse_lazy('cuentas_logout'))