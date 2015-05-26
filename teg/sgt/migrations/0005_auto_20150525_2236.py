# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0004_auto_20150525_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='centroinspeccion',
            name='hora_apertura',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='hora_cierre',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
