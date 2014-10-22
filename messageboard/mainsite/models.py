from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    creator = models.ForeignKey(User, related_name='topics_created')
    subscriptions = models.ManyToManyField(User, related_name='subscribed_topics')

    def __str__(self):
        return str(self.id) + ": " + str(self.topic_name)

class Message(models.Model):
    message_content = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now())
    creator = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)

    def __str__(self):
        return str(self.id)
