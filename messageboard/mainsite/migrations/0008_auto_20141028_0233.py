# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0007_auto_20141025_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timejoined',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
