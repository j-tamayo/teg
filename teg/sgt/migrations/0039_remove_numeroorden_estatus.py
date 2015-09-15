# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0038_auto_20150914_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='numeroorden',
            name='estatus',
        ),
    ]
