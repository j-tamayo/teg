# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0007_sgtusuario_centro_inspeccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sgtusuario',
            name='cedula',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sgtusuario',
            name='direccion',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sgtusuario',
            name='fecha_nacimiento',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sgtusuario',
            name='sexo',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
