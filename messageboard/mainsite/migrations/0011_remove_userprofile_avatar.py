# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0010_auto_20141105_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='avatar',
        ),
    ]
