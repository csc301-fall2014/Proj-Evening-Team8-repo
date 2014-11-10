# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('group_name', models.CharField(max_length=200)),
                ('group_password', models.CharField(max_length=20)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='groups_created')),
                ('user_set', models.ManyToManyField(related_name='joined_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('tag_name', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Only alphanumeric characters are allowed.', regex='^[0-9a-zA-Z]*$', code='invalid_tag')], unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('topic_name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='topics_created')),
                ('subscriptions', models.ManyToManyField(related_name='subscribed_topics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('activation_key', models.CharField(blank=True, max_length=40, unique=True)),
                ('key_expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_description', models.CharField(blank=True, default='', max_length=200)),
                ('school', models.CharField(null=True, blank=True, default='', max_length=200)),
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
