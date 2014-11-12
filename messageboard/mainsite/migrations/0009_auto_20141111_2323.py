# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0008_auto_20141105_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(default='', null=True, blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_description',
            field=models.CharField(default='', blank=True, max_length=200),
        ),
    ]
