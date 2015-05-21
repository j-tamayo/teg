# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0002_auto_20150513_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='centroinspeccion',
            name='capacidad',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='tiempo_atencion',
            field=models.IntegerField(default=0),
        ),
    ]
