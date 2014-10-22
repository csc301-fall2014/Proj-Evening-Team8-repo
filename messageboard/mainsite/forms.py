from django import forms
from django.contrib.auth.models import User
from mainsite.models import Message, Topic
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email',  'first_name', 'last_name']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ('pub_date','topic', 'creator')
        widgets ={
            'message_content': forms.Textarea(attrs={'cols': 40, 'rows': 3,
                                                     'placeholder': "Write your message here...",
                                                     'required': True})
        }

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        exclude = ('pub_date', 'creator', 'subscriptions')
        fields = ['topic_name']