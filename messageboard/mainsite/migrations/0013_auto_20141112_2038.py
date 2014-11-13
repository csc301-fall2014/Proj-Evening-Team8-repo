# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0012_auto_20141112_1726'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Question',
            new_name='Poll',
        ),
        migrations.RenameField(
            model_name='choice',
            old_name='question',
            new_name='poll',
        ),
    ]
