# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0017_auto_20150720_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valorposible',
            name='valor_pregunta_encuesta',
            field=models.ManyToManyField(db_constraint=b'Encuesta', through='sgt.ValorPreguntaEncuesta', to='sgt.Pregunta', related_name='valores_pregunta_encuesta'),
        ),
    ]
