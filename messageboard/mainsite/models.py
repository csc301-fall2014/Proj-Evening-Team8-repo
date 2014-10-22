from django.db import models


class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return str(self.id) + ": " + str(self.topic_name)

class Message(models.Model):
    message_content = models.TextField()
    pub_date = models.DateTimeField('date published')
    topic = models.ForeignKey(Topic)

    def __str__(self):
        return str(self.id)
