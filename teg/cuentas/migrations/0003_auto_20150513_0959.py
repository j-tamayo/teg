# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0002_auto_20150512_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolsgt',
            name='permisos',
            field=models.ManyToManyField(to='cuentas.Permiso'),
        ),
        migrations.AddField(
            model_name='sgtusuario',
            name='codigo_postal',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
