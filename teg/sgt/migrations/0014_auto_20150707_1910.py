# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0013_auto_20150707_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoEncuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='encuesta',
            name='tipo_encuesta',
            field=models.ForeignKey(to='sgt.TipoEncuesta', null=True),
        ),
    ]
