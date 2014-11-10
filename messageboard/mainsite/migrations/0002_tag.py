# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=200)),
                ('tagged_topics', models.ManyToManyField(related_name='tags', to='mainsite.Topic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
