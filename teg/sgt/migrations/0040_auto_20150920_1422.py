# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0039_remove_numeroorden_estatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='FechaNoLaborable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='centroinspeccion',
            name='fechas_no_laborables',
            field=models.ManyToManyField(to='sgt.FechaNoLaborable'),
        ),
    ]
