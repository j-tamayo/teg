# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0040_auto_20150920_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pregunta',
            name='requerida',
        ),
    ]
