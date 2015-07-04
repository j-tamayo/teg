# -*- coding: utf-8 -*-
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic import View, FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from cuentas.forms import *
from cuentas.models import *

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

        return super(Ingresar, self).form_valid(form)

class Registro(View):
    def dispatch(self, request, *args, **kwargs):
    	return super(Registro, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
    	form = RegistroForm()
    	context = {
    		'form': form,
    	}
    	return render(request,'cuentas/registro.html', context)

    def post(self, request, *args, **kwargs):
    	form = RegistroForm(request.POST)
    	if form.is_valid():
            registro = form.cleaned_data
            rol_cliente = RolSgt.objects.get(codigo="cliente")

            #registro['fecha_nacimiento'] = datetime.strptime(registro['fecha_nacimiento'],'%d/%m/%Y')
            # registro['fecha_nacimiento'] = registro['fecha_nacimiento'].strftime('%Y-%m-%d')
            # print registro['fecha_nacimiento']

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
                rol = rol_cliente)
            
            usuario.set_password(registro['password'])
            usuario.save()

            return HttpResponseRedirect(reverse_lazy('cuentas_login'))

    	else:
            print form.errors
            municipios = Municipio.objects.filter(estado__id = request.POST.get('estado', None))
            mun_sel = request.POST.get('municipio', None)
            if mun_sel:
                mun_sel = int(mun_sel)
            
            context = {
                'form': form,
                'municipios': municipios,
                'mun_sel': mun_sel
            }
            return render(request,'cuentas/registro.html', context)


class Salir(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            #del request.session['usuario_id']
            
            logout(request)
            mensaje = u'¡Ha cerrado sesión correctamente!'
            messages.info(self.request, mensaje)

        return redirect(reverse_lazy('cuentas_login'))


class DetectarUsuario(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        usuario = request.user
        
        if usuario.is_authenticated():
            if usuario.es_cliente():
                return redirect(reverse_lazy('bandeja_cliente'))

            elif usuario.es_admin():
                return redirect(reverse_lazy('admin_centros'))		
            #pass

        elif usuario.is_authenticated() and not usuario.is_active:
            print "NO ACTIVE"

        return redirect(reverse_lazy('cuentas_logout'))