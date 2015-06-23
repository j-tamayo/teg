# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0008_auto_20150622_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='numeroorden',
            name='estatus',
            field=models.ForeignKey(default=1, to='sgt.Estatus'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitudinspeccion',
            name='estatus',
            field=models.ForeignKey(default=1, to='sgt.Estatus'),
            preserve_default=False,
        ),
    ]
