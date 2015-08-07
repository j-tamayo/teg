# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0024_remove_centroinspeccion_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='asunto',
            field=models.CharField(default=b'Sin Asunto', max_length=255),
        ),
    ]
