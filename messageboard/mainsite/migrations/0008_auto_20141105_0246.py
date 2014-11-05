# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0007_group_group_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='school',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='timejoined',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_description',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
