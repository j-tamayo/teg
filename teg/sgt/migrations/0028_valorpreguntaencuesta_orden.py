# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0027_respuesta_encuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='valorpreguntaencuesta',
            name='orden',
            field=models.IntegerField(default=0),
        ),
    ]
