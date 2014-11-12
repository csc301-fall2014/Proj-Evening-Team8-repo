# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_auto_20141112_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='notifications_enabled',
            field=models.BooleanField(verbose_name='enable notifications', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_notified',
            field=models.DateTimeField(default=datetime.datetime(1990, 11, 12, 15, 7, 3, 842083)),
        ),
    ]
