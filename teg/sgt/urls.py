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
            views.AdminAgregarPerito.as_view(),
            name='admin_crear_perito'
        ),

        url(
            r'^admin/editar-perito/(?P<perito_id>\d+)$',
            views.AdminEditarPerito.as_view(),
            name='admin_editar_perito'
        ),

        url(
            r'^admin/deshabilitar-perito$',
            views.AdminDeshabilitarPerito.as_view(),
            name='admin_deshabilitar_perito'
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

        url(
            r'^admin/editar-encuesta/(?P<encuesta_id>\d+)$',
            views.AdminEditarEncuesta.as_view(),
            name='admin_editar_encuesta'
        ),

        url(
            r'^admin/eliminar-encuesta$',
            views.AdminEliminarEncuesta.as_view(),
            name='admin_eliminar_encuesta'
        ),

        url(
            r'^admin/crear-pregunta/(?P<tipo_respuesta_id>\d+)$',
            views.AdminAgregarPregunta.as_view(),
            name='admin_crear_pregunta'
        ),

        url(
            r'^admin/crear-pregunta$',
            views.AdminAgregarPregunta.as_view(),
            name='admin_crear_pregunta'
        ),

        url(
            r'^admin/eliminar-pregunta$',
            views.AdminEliminarPregunta.as_view(),
            name='admin_eliminar_pregunta'
        ),

        url(
            r'^admin/crear-respuesta$',
            views.AdminAgregarRespuesta.as_view(),
            name='admin_crear_respuesta'
        ),

        url(
            r'^admin/eliminar-respuesta$',
            views.AdminEliminarRespuesta.as_view(),
            name='admin_eliminar_respuesta'
        ),

        url(
            r'^admin/notificaciones$',
            views.AdminBandejaNotificaciones.as_view(),
            name='admin_notificaciones'
        ),

        url(
            r'^admin/crear-notificacion$',
            views.AdminAgregarNotificacion.as_view(),
            name='admin_crear_notificacion'
        ),

        url(
            r'^admin/editar-notificacion/(?P<notificacion_id>\d+)$',
            views.AdminEditarNotificacion.as_view(),
            name='admin_editar_notificacion'
        ),

        url(
            r'^admin/eliminar-notificacion$',
            views.AdminEliminarNotificacion.as_view(),
            name='admin_eliminar_notificacion'
        ),

        url(
            r'^admin/enviar-notificacion$',
            views.AdminEnviarNotificacion.as_view(),
            name='admin_enviar_notificacion'
        ),

        url(
            r'^admin/consultas$',
            views.AdminReportes.as_view(),
            name='admin_reportes'
        ),

        url(
            r'^taquilla$',
            views.BandejaTaquilla.as_view(),
            name='bandeja_taquilla'
        ),

        url(
            r'^taquilla-accion$',
            views.TaquillaAccionSolicitud.as_view(),
            name='taquilla_accion_solicitud'
        ),

        url(
            r'^exportar-consulta-xls$',
            views.ReporteXls.as_view(),
            name='exportar_reporte_xls'
        ),

        url(
            r'^carga-masiva-centros$',
            views.CargaMasivaCentros.as_view(),
            name='carga_masiva_centros'
        ),

        url(
            r'^admin/parametros-configuracion$',
            views.AdminParametros.as_view(),
            name='admin_parametros'
        ),

        url(
            r'^consultar-notificacion$',
            views.ConsultarNotificacion.as_view(),
            name='consultar_notificacion'
        ),

        url(
            r'^consultar-encuesta$',
            views.ConsultarEncuesta.as_view(),
            name='consultar_encuesta'
        ),

)