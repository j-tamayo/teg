# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0022_notificacion_encuesta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encuesta',
            name='usuarios',
        ),
        migrations.AddField(
            model_name='notificacionusuario',
            name='borrada',
            field=models.BooleanField(default=False),
        ),
    ]
