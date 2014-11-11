# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0009_userprofile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='avatar',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(max_length=200, blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_description',
            field=models.CharField(max_length=200, blank=True, default=''),
        ),
    ]
