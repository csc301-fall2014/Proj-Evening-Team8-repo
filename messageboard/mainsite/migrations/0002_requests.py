# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('group', models.ForeignKey(related_name='invited_group', to='mainsite.Group')),
                ('user_profile', models.ForeignKey(related_name='user_profile', to='mainsite.UserProfile')),
                ('user_that_invited', models.ForeignKey(related_name='user_that_invited', to='mainsite.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
