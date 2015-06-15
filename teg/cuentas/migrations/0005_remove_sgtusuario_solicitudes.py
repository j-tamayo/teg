# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0004_sgtusuario_solicitudes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sgtusuario',
            name='solicitudes',
        ),
    ]
