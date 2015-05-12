# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SgtUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('apellidos', models.CharField(max_length=200)),
                ('cedula', models.CharField(max_length=100)),
                ('clave', models.CharField(max_length=255)),
                ('correo', models.CharField(db_index=True, unique=True, max_length=255, error_messages={b'unique': b'Ya existe un usuario registrado con este correo electr\xc3\xb3nico.'})),
                ('direccion', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('nombres', models.CharField(max_length=200)),
                ('sexo', models.IntegerField()),
                ('telefono_local', models.CharField(max_length=100)),
                ('telefono_movil', models.CharField(max_length=100)),
                ('municipio', models.ForeignKey(blank=True, to='sgt.Municipio', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RolSgt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='sgtusuario',
            name='rol',
            field=models.ForeignKey(to='cuentas.RolSgt'),
        ),
    ]
