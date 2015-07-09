# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0014_auto_20150707_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='perito',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
