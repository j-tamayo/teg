# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0018_auto_20150720_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valorposible',
            name='valor_pregunta_encuesta',
            field=models.ManyToManyField(related_name='valores_pregunta_encuesta', through='sgt.ValorPreguntaEncuesta', to='sgt.Pregunta'),
        ),
    ]
