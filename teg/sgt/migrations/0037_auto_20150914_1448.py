# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0036_auto_20150914_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='cedula_cliente',
            field=models.CharField(default='v-1', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poliza',
            name='usuario',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
