# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0037_auto_20150914_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numeroorden',
            name='codigo',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
