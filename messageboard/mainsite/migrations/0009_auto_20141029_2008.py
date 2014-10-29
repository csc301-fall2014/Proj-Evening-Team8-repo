# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0008_auto_20141028_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default=b'picfolder/question_mark.jpg', upload_to=b'picfolder/', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='timejoined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
