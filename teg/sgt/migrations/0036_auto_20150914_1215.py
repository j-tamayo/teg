# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0035_auto_20150910_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poliza',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='poliza',
            name='fecha_fin_vigencia',
            field=models.DateField(default=datetime.datetime(2015, 9, 14, 16, 45, 10, 169575, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poliza',
            name='fecha_inicio_vigencia',
            field=models.DateField(default=datetime.datetime(2015, 9, 14, 16, 45, 15, 939472, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
