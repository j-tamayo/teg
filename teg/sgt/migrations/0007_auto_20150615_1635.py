# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0006_solicitudinspeccion_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='centroinspeccion',
            old_name='hora_apertura',
            new_name='hora_apertura_manana',
        ),
        migrations.RenameField(
            model_name='centroinspeccion',
            old_name='hora_cierre',
            new_name='hora_apertura_tarde',
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='hora_cierre_manana',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='hora_cierre_tarde',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
