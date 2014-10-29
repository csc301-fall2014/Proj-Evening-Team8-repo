# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0006_group_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_password',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
