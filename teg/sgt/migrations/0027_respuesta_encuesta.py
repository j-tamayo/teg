# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0026_centrostiemposatencion_parametrosgenerales'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='encuesta',
            field=models.ForeignKey(default=None, to='sgt.Encuesta'),
        ),
    ]
