from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from cuentas import views

urlpatterns = \
    patterns('',
        url(r'^$',
         RedirectView.as_view(url=reverse_lazy('cuentas_login'))),

        url(r'^ingresar/$',
         views.Ingresar.as_view(),
         name='cuentas_login'),

        url(r'^salir/$',
         views.Salir.as_view(),
         name='cuentas_logout'),

        # # Activar cuenta de PST
        # url(
        #  r'^activar/(?P<activation_key>[a-f0-9]{40})/$',
        #  views.ActivarCuentaView.as_view(),
        #  name='cuentas_activar_cuenta'
        # ),
        # url(
        #     r'^usuarios$',
        #     views.ListadoUsuarios.as_view(),
        #     name='listado_usuarios'
        # ),
        # url(
        #     r'^agregar_usuario$',
        #     views.AgregarUsuario.as_view(),
        #     name='agregar_usuario'
        # ),  
        # url(
        #     r'^modificar_usuario/(?P<id>\d+)$',
        #     views.ModificarUsuario.as_view(),
        #     name='modificar_usuario'
        # ), 
        # url(
        #     r'^ver_perfil$',
        #     views.VerPerfil.as_view(),
        #     name='ver_perfil'
        # ),
        # url(
        #     r'^activar_desactivar_usuario/(?P<id>\d+)$',
        #     views.ActivarDesactivarUsuario.as_view(),
        #     name='activar_desactivar_usuario'
        # ),
        # url(
        #     r'^usuario_nuevo_asignacion_clave/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        #     views.UsuarioNuevaClave.as_view(),
        #     name='usuario_nuevo_asignacion_clave'
        # ),
        # url(
        #     r'^recuperar_clave$',
        #     views.RecuperarClave.as_view(),
        #     name='recuperar_clave'
        # ),
        # url(
        #     r'^usuario_asignar_nueva_clave/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        #     views.AsignarNuevaClave.as_view(),
        #     name='usuario_asignar_nueva_clave'
        # ),

        # url(
        #     r'^ayuda/$',
        #     views.AyudaView.as_view(),
        #     name = 'ayuda'
        # ),

        # url(
        #     r'^reenviar_correo_activacion/(?P<id>\d+)$',
        #     views.ReenviarCorreoActivacion.as_view(),
        #     name = 'reenviar_correo_activacion'
        # )
)