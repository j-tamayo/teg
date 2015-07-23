# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sgt', '0019_auto_20150720_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificacionUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('leida', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='notificacion',
            old_name='texto',
            new_name='mensaje',
        ),
        migrations.RemoveField(
            model_name='notificacion',
            name='fecha_creacion',
        ),
        migrations.RemoveField(
            model_name='notificacion',
            name='leida',
        ),
        migrations.RemoveField(
            model_name='notificacion',
            name='usuario',
        ),
        migrations.AddField(
            model_name='notificacionusuario',
            name='notificacion',
            field=models.ForeignKey(related_name='notificacion', to='sgt.Notificacion'),
        ),
        migrations.AddField(
            model_name='notificacionusuario',
            name='usuario',
            field=models.ForeignKey(related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='notificacion_usuario',
            field=models.ManyToManyField(related_name='notificacion_usuario', through='sgt.NotificacionUsuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
