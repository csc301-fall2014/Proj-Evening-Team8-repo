# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0010_auto_20141112_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_notified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
