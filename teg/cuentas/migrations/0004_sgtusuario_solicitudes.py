# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0005_auto_20150525_2236'),
        ('cuentas', '0003_auto_20150513_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='sgtusuario',
            name='solicitudes',
            field=models.ManyToManyField(to='sgt.SolicitudInspeccion'),
        ),
    ]
