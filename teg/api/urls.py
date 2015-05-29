from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    # url(r'^snippets/$', views.snippet_list),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'^usuarios/$', views.Usuarios.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


