# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0013_auto_20141112_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='poll_id',
            field=models.IntegerField(default=99999),
            preserve_default=True,
        ),
    ]
