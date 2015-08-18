from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    # url(r'^snippets/$', views.snippet_list),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'^usuarios/$', views.Usuarios.as_view()),
    url(r'^usuarios-edit/$', views.UsuariosEdit.as_view()),
    url(r'^login/(?P<pk>[0-9]+)$', views.LoginUser.as_view()),
    url(r'^login/$', views.LoginUser.as_view()),
    url(r'^estados/$', views.Estados.as_view()),
    url(r'^municipios/$', views.Municipios.as_view()),
    url(r'^centros/$', views.Centros.as_view()),
    url(r'^centros-sol/$', views.ObtenerCentros.as_view()),
    url(r'^data-inicial/$', views.InitialData.as_view()),
    url(r'^usuario-info/(?P<pk>[0-9]+)/$', views.UserInfo.as_view()),
    url(r'^usuario-info/$', views.UserInfo.as_view()),
    url(r'^horarios/$', views.Horarios.as_view()),
    url(r'^crear-solicitud/$', views.CrearSolicitud.as_view()),
    url(r'^marcar-notificacion/$', views.MarcarNotificacion.as_view()),
    url(r'^guardar-respuestas-encuesta/$', views.GuardarRespuestasEncuesta.as_view()),
    url(r'^guardar-reclamo/$', views.GuardarReclamo.as_view()),
    url(r'^recuperar-clave/$', views.RecuperarClave.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)