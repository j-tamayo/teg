# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0031_auto_20150819_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='notificacion',
            field=models.ForeignKey(default=1, to='sgt.NotificacionUsuario'),
            preserve_default=False,
        ),
    ]
