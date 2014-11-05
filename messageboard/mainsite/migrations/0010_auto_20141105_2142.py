# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import awesome_avatar.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0009_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=awesome_avatar.fields.AvatarField(upload_to=b'avatars'),
        ),
    ]
