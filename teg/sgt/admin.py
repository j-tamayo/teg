from django.contrib import admin
from django.apps import apps
#from django.db.models import get_models, get_app

# Register your models here.
# for model in get_models(get_app('cuentas')):
#     admin.site.register(model)
# for model in get_models(get_app('sgt')):
# 	admin.site.register(model)
sgt = apps.get_app_config('sgt')
cuentas = apps.get_app_config('cuentas')

for model in sgt.get_models():
	admin.site.register(model)

for model in cuentas.get_models():
	admin.site.register(model)