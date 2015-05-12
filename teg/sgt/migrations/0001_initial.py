# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CentroInspeccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ColaAtencion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orden', models.IntegerField()),
                ('centro_inspeccion', models.ForeignKey(to='sgt.CentroInspeccion')),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('estado', models.ForeignKey(to='sgt.Estado')),
            ],
        ),
        migrations.CreateModel(
            name='NumeroOrden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asistencia', models.IntegerField(default=0)),
                ('codigo', models.CharField(max_length=50)),
                ('fecha_atencion', models.DateTimeField(null=True, blank=True)),
                ('centro_inspeccion', models.ForeignKey(to='sgt.CentroInspeccion')),
            ],
        ),
        migrations.CreateModel(
            name='Perito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apellidos', models.CharField(max_length=200)),
                ('cedula', models.CharField(max_length=100)),
                ('fecha_ingreso', models.DateField()),
                ('nombres', models.CharField(max_length=200)),
                ('sexo', models.IntegerField()),
                ('tiempo_empresa', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('pregunta', models.CharField(max_length=255)),
                ('respuesta', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SistemaOperativo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudInspeccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_culminacion', models.DateTimeField(null=True, blank=True)),
                ('perito', models.ForeignKey(blank=True, to='sgt.Perito', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoInspeccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='solicitudinspeccion',
            name='tipo_inspeccion',
            field=models.ForeignKey(to='sgt.TipoInspeccion'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='preguntas',
            field=models.ManyToManyField(to='sgt.Pregunta'),
        ),
        migrations.AddField(
            model_name='colaatencion',
            name='numero_orden',
            field=models.ForeignKey(to='sgt.NumeroOrden'),
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='municipio',
            field=models.ForeignKey(to='sgt.Municipio'),
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='numero_orden',
            field=models.ManyToManyField(to='sgt.NumeroOrden', through='sgt.ColaAtencion'),
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='peritos',
            field=models.ManyToManyField(to='sgt.Perito'),
        ),
    ]
