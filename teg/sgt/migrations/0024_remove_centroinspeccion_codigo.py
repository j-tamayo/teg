# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0023_auto_20150729_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='centroinspeccion',
            name='codigo',
        ),
    ]
