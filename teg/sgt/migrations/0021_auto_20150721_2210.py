# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0020_auto_20150721_2207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tiponotificacion',
            old_name='nombre',
            new_name='descripcion',
        ),
    ]
