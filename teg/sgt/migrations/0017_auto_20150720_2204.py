# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0016_remove_perito_tiempo_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValorPreguntaEncuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('encuesta', models.ForeignKey(related_name='encuesta', to='sgt.Encuesta')),
                ('pregunta', models.ForeignKey(related_name='pregunta_encuesta', to='sgt.Pregunta')),
            ],
        ),
        migrations.RemoveField(
            model_name='valorposible',
            name='valor_pregunta',
        ),
        migrations.AddField(
            model_name='valorpreguntaencuesta',
            name='valor',
            field=models.ForeignKey(related_name='valor_pregunta', to='sgt.ValorPosible'),
        ),
        migrations.AddField(
            model_name='valorposible',
            name='valor_pregunta_encuesta',
            field=models.ManyToManyField(related_name='valores__pregunta_encuesta', through='sgt.ValorPreguntaEncuesta', to='sgt.Pregunta'),
        ),
    ]
