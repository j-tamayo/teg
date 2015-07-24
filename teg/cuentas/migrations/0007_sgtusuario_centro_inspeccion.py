# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0021_auto_20150721_2210'),
        ('cuentas', '0006_remove_sgtusuario_clave'),
    ]

    operations = [
        migrations.AddField(
            model_name='sgtusuario',
            name='centro_inspeccion',
            field=models.ForeignKey(blank=True, to='sgt.CentroInspeccion', null=True),
        ),
    ]
