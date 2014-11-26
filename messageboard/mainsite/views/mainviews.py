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
from mainviews import *
from groupsviews import *
from registrationviews import *
from topicsviews import *
from userprofileviews import *

def index(request):
    return render(request, 'index.html')

@login_required(login_url='/mainsite/login')
def messageboard(request):
    topic_list = Topic.objects.all()
    if request.method == 'POST':
        tag_name = request.POST['tag_name']
        if tag_name:
            try:
                tag = Tag.objects.get(tag_name=tag_name)
                topic_list = tag.tagged_topics.all()
            except Tag.DoesNotExist:
                return response(request,
                                'Nonexistent Tag',
                                'Tag does not exist.',
                                '/mainsite/messageboard/',
                                'Back')

    return render(request, 'messageboard.html', {'topics': topic_list})


@login_required(login_url='/mainsite/login')
def tableview(request):
    topic_list = Topic.objects.all()
    message_list = Message.objects.all()
    # Filtering for private topics
    user = request.user
    rm = True
    # In each topic, check if it is private
    for topic in topic_list:
        if topic.group_set.exists():
            # In each group, check if the user belongs to it.
            for group in topic.group_set.all():
                if group.user_set.filter(id=user.id).exists():
                    rm = False
                    break
            # If they are not in the right group, exclude this topic
            if rm:
                topic_list = topic_list.exclude(id=topic.id)

    if "POST_post" in request.POST:
        post_message(request.POST['message_content'], Topic.objects.get(id=request.POST['topic_id']), request.user)
        return HttpResponseRedirect(reverse('mainsite:messageboard'))
    elif "POST_subscribe" in request.POST:
        current_topic = Topic.objects.get(id=request.POST['topic_id'])
        # If subscribed, unsubscribe
        if current_topic.subscriptions.filter(username=request.user.username).exists():
            # Need to remove both sides of the relation manually
            current_topic.subscriptions.remove(request.user)
            request.user.subscribed_topics.remove(current_topic)
        # If not subscribed, subscribe
        else:
            # No need to add to both sides of the relation
            current_topic.subscriptions.add(request.user)
        return HttpResponseRedirect(reverse('mainsite:messageboard'))
    elif "POST_add_tag" in request.POST:
        tag_name = request.POST['tag_name']
        current_topic = Topic.objects.get(id=request.POST['topic_id'])
        if tag_name:
            try:
                tag = Tag.objects.get(tag_name=tag_name)
                # No need to add to both sides of the relation
                current_topic.tags.add(tag)
            except Tag.DoesNotExist:
                tag = Tag()
                tag.tag_name = tag_name
                try:
                    tag.full_clean()  # Validate tag, not done automatically
                    tag.save()
                    current_topic.tags.add(tag)
                except ValidationError as e:
                    return response(request,
                                    'Invalid Tag',
                                    str(e.message_dict['tag_name'])[2:-2],  # Trim [' and ']
                                    '/mainsite/messageboard/',
                                    'Back')
        return HttpResponseRedirect(reverse('mainsite:messageboard'))
    elif "POST_remove_tag" in request.POST:
        tag_name = request.POST['tag_name']
        current_topic = Topic.objects.get(id=request.POST['topic_id'])
        if tag_name:
            try:
                tag = Tag.objects.get(tag_name=tag_name)
                current_topic.tags.remove(tag)

                # Need to remove both sides of the relation manually
                current_topic.tags.remove(tag)
                tag.tagged_topics.remove(current_topic)

                # Delete tag if not in use
                if not tag.tagged_topics.all():
                    tag.delete()
            except Tag.DoesNotExist:
                pass  # Do nothing is tag doesn't exist
        return HttpResponseRedirect(reverse('mainsite:messageboard'))
    elif "POST_filter" in request.POST:
        tag_name = request.POST['tag_name']
        # If tag field is not empty, filter by tag if it exists.
        if tag_name:
            try:
                tag = Tag.objects.get(tag_name=tag_name)
                topic_list = tag.tagged_topics.all()
            except Tag.DoesNotExist:
                topic_list = []
        # If 'subscriptions only' checked, (further) filter by subscribed only.
        if "subscribed" in request.POST:
            topic_list = topic_list & request.user.subscribed_topics.all()
        return render(request, 'tableview.html', {
            'topics': topic_list,
            'messages': message_list})

    # Get all subscribed topics from previously filtered topics
    subscribed_ids = user.subscribed_topics.values_list('id', flat=True)
    topic_sublist = topic_list.filter(id__in=subscribed_ids)

    # Get all unsubscribed topics from previously filtered topics
    topic_nsublist = Topic.objects.exclude(id__in=subscribed_ids)
    topic_list2 = chain(topic_sublist, topic_nsublist)
    
    return render(request, 'tableview.html', {'topics': topic_list2, 'subIDs': subscribed_ids, 'messages': message_list})


# Not a view, helper function for notices (a richer and more customizable HttpResponse)
def response(request, title, message, link, button):
    return render(request, 'response.html', {
        'title': title,
        'message': message,
        'link': link,
        'button': button})
