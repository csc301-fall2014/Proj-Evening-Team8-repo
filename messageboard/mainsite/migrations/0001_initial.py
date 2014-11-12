# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=200)),
                ('group_password', models.CharField(max_length=20)),
                ('creator', models.ForeignKey(related_name='groups_created', to=settings.AUTH_USER_MODEL)),
                ('user_set', models.ManyToManyField(related_name='joined_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('message_content', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('tag_name', models.CharField(unique=True, validators=[django.core.validators.RegexValidator(code='invalid_tag', message='Only alphanumeric characters and underscores are allowed.', regex='^[0-9a-zA-Z_]*$')], max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('topic_name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('creator', models.ForeignKey(related_name='topics_created', to=settings.AUTH_USER_MODEL)),
                ('subscriptions', models.ManyToManyField(related_name='subscribed_topics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('activation_key', models.CharField(unique=True, blank=True, max_length=40)),
                ('key_expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_description', models.CharField(default='', blank=True, max_length=200)),
                ('school', models.CharField(null=True, default='', blank=True, max_length=200)),
                ('timejoined', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tag',
            name='tagged_topics',
            field=models.ManyToManyField(related_name='tags', to='mainsite.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='topic',
            field=models.ForeignKey(to='mainsite.Topic'),
            preserve_default=True,
        ),
    ]
