# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0021_auto_20150721_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='encuesta',
            field=models.ForeignKey(blank=True, to='sgt.Encuesta', null=True),
        ),
    ]
