# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_notified',
            field=models.DateTimeField(default=datetime.datetime(1990, 11, 12, 14, 6, 32, 138361)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notification_delay',
            field=models.FloatField(default=21600.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notification_queue',
            field=models.ManyToManyField(to='mainsite.Topic', related_name='users_to_notify'),
            preserve_default=True,
        ),
    ]
