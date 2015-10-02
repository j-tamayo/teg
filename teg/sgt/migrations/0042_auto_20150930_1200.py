# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0041_remove_pregunta_requerida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispositivo',
            name='sistema_operativo',
        ),
        migrations.DeleteModel(
            name='Dispositivo',
        ),
        migrations.DeleteModel(
            name='SistemaOperativo',
        ),
    ]
