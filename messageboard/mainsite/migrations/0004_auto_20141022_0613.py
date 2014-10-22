# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_auto_20141022_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_content',
            field=models.TextField(),
        ),
    ]
