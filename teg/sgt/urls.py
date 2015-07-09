from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from sgt import views

urlpatterns = \
    patterns('',

        url(
            r'^obtener-municipios/(?P<estado_id>\d+)$',
            views.ObtenerMunicipios.as_view(),
            name='obtener_municipios'
        ),

        url(
            r'^obtener-numero/(?P<centro_id>\d+)$',
            views.GenerarNumeroOrden.as_view(),
            name='obtener_numero'
        ),

        url(
            r'^obtener-centros$',
            views.ObtenerCentroInspeccion.as_view(),
            name='obtener_centros'
        ),

        url(
            r'^bandeja-cliente$',
            views.BandejaCliente.as_view(),
            name='bandeja_cliente'
        ),

        url(
            r'^crear-solicitud$',
            views.CrearSolicitudInspeccion.as_view(),
            name='crear_solicitud'
        ),

        url(
            r'^admin/centros$',
            views.AdminBandejaCentros.as_view(),
            name='admin_centros'
        ),

        url(
            r'^admin/crear-centro$',
            views.AdminAgregarCentro.as_view(),
            name='admin_crear_centro'
        ),

        url(
            r'^admin/editar-centro/(?P<centro_id>\d+)$',
            views.AdminEditarCentro.as_view(),
            name='admin_editar_centro'
        ),

        url(
            r'^admin/eliminar-centro$',
            views.AdminEliminarCentro.as_view(),
            name='admin_eliminar_centro'
        ),

        url(
            r'^admin/usuarios$',
            views.AdminBandejaUsuarios.as_view(),
            name='admin_usuarios'
        ),

        url(
            r'^admin/crear-usuario$',
            views.AdminCrearUsuario.as_view(),
            name='admin_crear_usuario'
        ),

        url(
            r'^admin/editar-usuario/(?P<user_id>\d+)$',
            views.AdminEditarUsuario.as_view(),
            name='admin_editar_usuario'
        ),

        url(
            r'^admin/deshabilitar-usuario$',
            views.AdminDeshabilitarUsuario.as_view(),
            name='admin_deshabilitar_usuario'
        ),

        url(
            r'^admin/peritos$',
            views.AdminBandejaPeritos.as_view(),
            name='admin_peritos'
        ),

        url(
            r'^admin/agregar-perito$',
            views.AdminBandejaPeritos.as_view(),
            name='admin_crear_perito'
        ),

        url(
            r'^admin/editar-perito/(?P<perito_id>\d+)$',
            views.AdminBandejaPeritos.as_view(),
            name='admin_editar_perito'
        ),

        url(
            r'^admin/encuestas$',
            views.AdminBandejaEncuestas.as_view(),
            name='admin_encuestas'
        ),

        url(
            r'^admin/crear-encuesta$',
            views.AdminAgregarEncuesta.as_view(),
            name='admin_crear_encuesta'
        ),
)