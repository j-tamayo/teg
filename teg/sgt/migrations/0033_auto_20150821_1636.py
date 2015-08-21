# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0032_respuesta_notificacion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respuesta',
            old_name='notificacion',
            new_name='notificacion_usuario',
        ),
    ]
