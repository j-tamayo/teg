# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0011_auto_20150630_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('respuesta', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoRespuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='encuesta',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='respuesta',
        ),
        migrations.AddField(
            model_name='respuesta',
            name='pregunta',
            field=models.ForeignKey(to='sgt.Pregunta'),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='tipo_respuesta',
            field=models.ForeignKey(to='sgt.TipoRespuesta'),
        ),
    ]
