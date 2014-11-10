# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(validators=[django.core.validators.RegexValidator(code='invalid_tag', message='Only alphanumeric characters and underscores are allowed.', regex='^[0-9a-zA-Z_]*$')], max_length=200, unique=True),
        ),
    ]
