# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('group_name', models.CharField(max_length=200)),
                ('group_password', models.CharField(max_length=20)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='groups_created')),
                ('user_set', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='joined_groups')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('message_content', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('topic_name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='topics_created')),
                ('subscriptions', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='subscribed_topics')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('activation_key', models.CharField(max_length=40, unique=True, blank=True)),
                ('key_expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_description', models.CharField(max_length=200, default='', blank=True)),
                ('school', models.CharField(null=True, max_length=200, default='', blank=True)),
                ('timejoined', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='topic',
            field=models.ForeignKey(to='mainsite.Topic'),
            preserve_default=True,
        ),
    ]
