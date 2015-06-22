# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0007_auto_20150615_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='numeroorden',
            name='hora_atencion',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='numeroorden',
            name='fecha_atencion',
            field=models.DateField(null=True, blank=True),
        ),
    ]
