# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='group_set',
            field=models.ManyToManyField(related_name='viewable_topics', blank=True, to='mainsite.Group'),
            preserve_default=True,
        ),
    ]
