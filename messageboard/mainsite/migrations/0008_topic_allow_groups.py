# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0007_group_group_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='allow_groups',
            field=models.ManyToManyField(related_name='private_topics', to='mainsite.Group'),
            preserve_default=True,
        ),
    ]
