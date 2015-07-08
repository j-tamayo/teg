# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sgt', '0012_auto_20150706_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='RespuestaDefinida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaIndefinida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor_indefinido', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ValorPosible',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='pregunta',
            old_name='pregunta',
            new_name='enunciado',
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='respuesta',
        ),
        migrations.RemoveField(
            model_name='respuesta',
            name='tipo_respuesta',
        ),
        migrations.AddField(
            model_name='pregunta',
            name='requerida',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pregunta',
            name='tipo_respuesta',
            field=models.ForeignKey(to='sgt.TipoRespuesta', null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='valorposible',
            name='valor_pregunta',
            field=models.ManyToManyField(to='sgt.Pregunta'),
        ),
        migrations.AddField(
            model_name='respuestaindefinida',
            name='respuesta',
            field=models.ForeignKey(to='sgt.Respuesta'),
        ),
        migrations.AddField(
            model_name='respuestadefinida',
            name='respuesta',
            field=models.ForeignKey(to='sgt.Respuesta'),
        ),
        migrations.AddField(
            model_name='respuestadefinida',
            name='valor_definido',
            field=models.ForeignKey(to='sgt.ValorPosible'),
        ),
    ]
