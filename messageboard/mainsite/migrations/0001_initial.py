# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('message_content', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('tag_name', models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_tag', regex='^[0-9a-zA-Z_]*$', message='Only alphanumeric characters and underscores are allowed.')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('activation_key', models.CharField(max_length=40, unique=True, blank=True)),
                ('key_expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_description', models.CharField(max_length=200, blank=True, default='')),
                ('school', models.CharField(max_length=200, null=True, blank=True, default='')),
                ('timejoined', models.DateTimeField(default=django.utils.timezone.now)),
                ('notification_delay', models.FloatField(default=21600.0)),
                ('last_notified', models.DateTimeField(default=datetime.datetime(1990, 11, 12, 19, 38, 7, 417172))),
                ('notifications_enabled', models.BooleanField(verbose_name='subscription notifications', default=True)),
                ('notification_queue', models.ManyToManyField(to='mainsite.Topic', related_name='users_to_notify')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user_profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tag',
            name='tagged_topics',
            field=models.ManyToManyField(to='mainsite.Topic', related_name='tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='topic',
            field=models.ForeignKey(to='mainsite.Topic'),
            preserve_default=True,
        ),
    ]
