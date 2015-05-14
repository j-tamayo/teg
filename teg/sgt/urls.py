from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from sgt import views

urlpatterns = \
    patterns('',
        url(r'^$',
         RedirectView.as_view(url=reverse_lazy('cuentas_login'))),

)