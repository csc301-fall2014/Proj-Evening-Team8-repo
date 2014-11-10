from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
#from awesome_avatar.fields import AvatarField


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    activation_key = models.CharField(max_length=40, blank=True, unique=True)
    key_expires = models.DateTimeField(default=timezone.now)
    user_description = models.CharField(max_length=200, blank=True, default="")
    school = models.CharField(max_length=200, blank=True, default="", unique=False, null=True)
    timejoined = models.DateTimeField(default=timezone.now)
    #avatar = AvatarField(upload_to='avatars', width=100, height=100)
    
    def __str__(self):
        return self.user.username


class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    creator = models.ForeignKey(User, related_name='topics_created')
    subscriptions = models.ManyToManyField(User, related_name='subscribed_topics')

    def __str__(self):
        return str(self.id) + ": " + str(self.topic_name)


class Message(models.Model):
    message_content = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)
    creator = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)

    def __str__(self):
        return str(self.id)


class Group(models.Model):
    group_name = models.CharField(max_length=200)
    group_password = models.CharField(max_length=20)
    creator = models.ForeignKey(User, related_name='groups_created')
    user_set = models.ManyToManyField(User, related_name='joined_groups')

    def __str__(self):
        return str(self.id) + ": " + str(self.group_name)


class Tag(models.Model):
    alphanumeric = RegexValidator(regex=r'^[0-9a-zA-Z]*$',
                                  message='Only alphanumeric characters are allowed.',
                                  code='invalid_tag')

    tag_name = models.CharField(max_length=200, blank=False, unique=True, validators=[alphanumeric])
    tagged_topics = models.ManyToManyField(Topic, related_name='tags')

    def __str__(self):
        return self.tag_name