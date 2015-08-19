# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0030_auto_20150814_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacionusuario',
            name='encuesta_respondida',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudinspeccion',
            name='borrada',
            field=models.BooleanField(default=False),
        ),
    ]
