# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0029_reclamo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacionusuario',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True),
        ),
    ]
