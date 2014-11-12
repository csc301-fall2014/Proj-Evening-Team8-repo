# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0011_auto_20141112_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_notified',
            field=models.DateTimeField(default=datetime.datetime(1990, 11, 12, 1, 19, 10, 904668)),
        ),
    ]
