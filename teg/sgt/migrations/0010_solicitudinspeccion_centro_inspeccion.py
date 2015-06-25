# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0009_auto_20150623_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudinspeccion',
            name='centro_inspeccion',
            field=models.ForeignKey(default=1, to='sgt.CentroInspeccion'),
            preserve_default=False,
        ),
    ]
