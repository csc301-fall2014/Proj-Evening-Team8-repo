# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0012_auto_20141112_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='notification_queue',
            field=models.ManyToManyField(related_name='users_to_notify', to='mainsite.Topic'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_notified',
            field=models.DateTimeField(default=datetime.datetime(1990, 11, 12, 1, 45, 57, 546562)),
        ),
    ]
