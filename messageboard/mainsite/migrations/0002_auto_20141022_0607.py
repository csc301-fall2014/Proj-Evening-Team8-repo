# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_content',
            field=models.CharField(max_length=10, error_messages={'max_length': 'Please keep messages under 250 characters'}),
        ),
    ]
