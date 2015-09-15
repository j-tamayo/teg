# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0034_auto_20150827_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colaatencion',
            name='centro_inspeccion',
        ),
        migrations.RemoveField(
            model_name='colaatencion',
            name='numero_orden',
        ),
        migrations.RemoveField(
            model_name='centroinspeccion',
            name='numero_orden',
        ),
        migrations.DeleteModel(
            name='ColaAtencion',
        ),
    ]
