# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0033_auto_20150821_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacionusuario',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
