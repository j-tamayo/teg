# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0025_notificacion_asunto'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentrosTiemposAtencion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('tiempo_atencion', models.IntegerField()),
                ('centro_inspeccion', models.ForeignKey(to='sgt.CentroInspeccion')),
            ],
        ),
        migrations.CreateModel(
            name='ParametrosGenerales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=255)),
            ],
        ),
    ]
