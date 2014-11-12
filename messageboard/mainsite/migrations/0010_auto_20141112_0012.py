# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0009_auto_20141111_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_notified',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 11, 18, 12, 27, 907709)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notification_delay',
            field=models.FloatField(default=21600.0),
            preserve_default=True,
        ),
    ]
