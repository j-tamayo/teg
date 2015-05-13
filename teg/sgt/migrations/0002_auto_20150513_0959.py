# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sgt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispositivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marca', models.CharField(max_length=255)),
                ('modelo', models.CharField(max_length=255)),
                ('wifi', models.IntegerField(null=True, blank=True)),
                ('sistema_operativo', models.ForeignKey(to='sgt.SistemaOperativo')),
            ],
        ),
        migrations.CreateModel(
            name='Poliza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('numero', models.IntegerField()),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='numeroorden',
            name='centro_inspeccion',
        ),
        migrations.AddField(
            model_name='encuesta',
            name='usuarios',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='numeroorden',
            name='solicitud_inspeccion',
            field=models.ForeignKey(default=1, to='sgt.SolicitudInspeccion'),
            preserve_default=False,
        ),
    ]
