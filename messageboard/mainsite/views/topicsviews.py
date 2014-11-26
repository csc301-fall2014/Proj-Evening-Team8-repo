import hashlib
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from mainsite.forms import UserForm, TopicForm, GroupForm, UserProfileForm, DirectMessageForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login  # Changed name because login is our view function
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from mainsite.models import Topic, Message, UserProfile, Group, Tag, Requests, Conversation, DirectMessage
from datetime import datetime, timedelta
from itertools import chain

@login_required(login_url='/mainsite/login')
def create_topic(request):
    form = TopicForm(request.user)
    if request.method == 'POST':
        topic = Topic(topic_name=request.POST['topic_name'], creator=request.user)
        topic.save()
        if "group_set" in request.POST:
            for group in request.POST['group_set']:
                topic.group_set.add(group)
            topic.save()
        return redirect('/mainsite/messageboard/')
    else:
        return render(request, 'topics/create_topic.html',
                        {'form': form})


@login_required(login_url='/mainsite/login')
def topic(request, topicid):
    this_topic = Topic.objects.get(id=topicid)
    tag_error = ""
    if request.method == 'POST':

        # Post a message to the topic.
        if "POST" in request.POST:
            post_message(request.POST['message_content'], Topic.objects.get(id=topicid), request.user)
            return HttpResponseRedirect(reverse('mainsite:topic', args=(topicid,)))

        # Edit a message.
        elif "save" in request.POST:
            message = get_object_or_404(Message, pk=request.POST['msgID'])
            message.message_content = request.POST['message_content']
            message.save()
            return HttpResponseRedirect(reverse('mainsite:topic', args=(topicid,)))

        # Delete a message.
        elif "REMOVE" in request.POST:
            message = get_object_or_404(Message, pk=request.POST['msgID'])
            message.delete()
            return HttpResponseRedirect(reverse('mainsite:topic', args=(topicid,)))
        elif "add_tag" in request.POST:
            tag_name = request.POST['tag_name']
            if tag_name:
                try:
                    tag = Tag.objects.get(tag_name=tag_name)
                    this_topic.tags.add(tag)
                except Tag.DoesNotExist:
                    tag = Tag()
                    tag.tag_name = tag_name
                    try:
                        tag.full_clean()  # Validate tag, not done automatically
                        tag.save()
                        this_topic.tags.add(tag)
                    except ValidationError as e:
                        tag_error = str(e.message_dict['tag_name'])[2:-2]  # Trim [' and ']
            return HttpResponseRedirect(reverse('mainsite:topic', args=(topicid,)))
        elif "remove_tag" in request.POST:
            tag_name = request.POST['tag_name']
            if tag_name:
                try:
                    tag = Tag.objects.get(tag_name=tag_name)
                    this_topic.tags.remove(tag)

                    # Remove both sides of the relation
                    this_topic.tags.remove(tag)
                    tag.tagged_topics.remove(this_topic)

                    # Delete tag if not in use
                    if not tag.tagged_topics.all():
                        tag.delete()
                except Tag.DoesNotExist:
                    pass  # Do nothing is tag doesn't exist
            return HttpResponseRedirect(reverse('mainsite:topic', args=(topicid,)))
    messagelist = Message.objects.filter(topic__id=this_topic.id)
    return render(request, 'topics/topic.html', {
        'messages': messagelist,
        'topic': this_topic,
        'tags': this_topic.tags.all,
        'tag_error': tag_error})

def post_message(content, topic, creator):
    message = Message()
    message.creator = creator
    message.topic = topic
    message.message_content = content
    message.save()

    # Hand out subscription notifications (currently synchronous)
    subscribers = topic.subscriptions.all()
    for subscriber in subscribers:
        if subscriber != message.creator:
            notify_subscriber(topic, subscriber)



# Helper function for subscription notifications.
# No loginrequired header is needed here, its not an actual view function.
def notify_subscriber(topic, subscriber):
    profile = subscriber.user_profile

    if not profile.notifications_enabled:
        return

    # Add a topic to the user's notification queue.
    profile.notification_queue.add(topic)
    profile.save()

    # Check if its been long enough since the last email.
    if datetime.now() > (profile.last_notified.replace(tzinfo=None) + timedelta(seconds=profile.notification_delay)):

        # Start composing the email.
        email_subject = 'Subscription Update!'
        email_body = "Dear %s,\n\nA new message has been posted to a topic you're subscribed to!\n\n" \
                     % subscriber.username

        # Dump all the topic links into the email.
        for t in profile.notification_queue.all():
            email_body += "http://127.0.0.1:8000/mainsite/messageboard/%d\n" % t.id
        email_body += "\n\nYours,\nTeam8s"
        send_mail(email_subject, email_body, 'no-reply@messageboard.com', [subscriber.email], fail_silently=False)

        # Clear the notification queue, set the last_notified time.
        profile.notification_queue.clear()
        profile.last_notified = timezone.now()
        profile.save()


@login_required(login_url='/mainsite/login')
def subscribe(request, topicid):
    # Associate the topic and user to create a subscription
    user = request.user
    user.subscribed_topics.add(Topic.objects.get(id=topicid))
    # After subscribing, redirect to the user's subscription list.
    return redirect(reverse('mainsite:topic', args=(topicid,)))


@login_required(login_url='/mainsite/login')
def subscribed_topics(request):
    if "POST" in request.POST:
            message = Message()
            message.creator = request.user
            current_topic = Topic.objects.get(id=request.POST['topic'])
            message.topic = current_topic
            message.message_content = request.POST['message_content']
            message.save()
            return HttpResponseRedirect(reverse('mainsite:subscriptions'))
    user = request.user
    topic_list = user.subscribed_topics.all()
    message_list = Message.objects.filter(topic__in=topic_list)
    return render(request, 'topics/subscribed_topics.html', {'topics': topic_list,
                                                             'messages':message_list})