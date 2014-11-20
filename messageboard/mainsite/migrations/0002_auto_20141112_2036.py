# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='mod_set',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='moderated_groups'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_notified',
            field=models.DateTimeField(default=datetime.datetime(1990, 11, 12, 20, 36, 7, 451664)),
        ),
    ]
