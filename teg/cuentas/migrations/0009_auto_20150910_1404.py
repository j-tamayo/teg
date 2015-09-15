# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0008_auto_20150910_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sgtusuario',
            name='codigo_postal',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
