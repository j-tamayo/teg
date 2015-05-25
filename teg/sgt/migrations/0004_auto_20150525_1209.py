# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0003_auto_20150520_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='centroinspeccion',
            name='codigo',
            field=models.CharField(default='COD', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='telefonos',
            field=models.CharField(default='No posee', max_length=255),
            preserve_default=False,
        ),
    ]
