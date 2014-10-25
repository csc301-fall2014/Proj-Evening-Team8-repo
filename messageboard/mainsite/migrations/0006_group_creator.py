# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainsite', '0005_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(related_name='groups_created', to=settings.AUTH_USER_MODEL, default=0),
            preserve_default=False,
        ),
    ]
