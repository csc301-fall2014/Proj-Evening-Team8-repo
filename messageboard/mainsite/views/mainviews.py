from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from mainsite.models import Topic, Message, Tag
from mainsite.views import helperviews
from itertools import chain


def index(request):
    return render(request, 'index.html')


@login_required(login_url='/mainsite/login')
def tableview(request):
    topic_list = Topic.objects.all()
    message_list = Message.objects.all()
    # Filtering for private topics
    user = request.user
    # In each topic, check if it is private
    for topic in topic_list:
        rm = True
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
        helperviews.post_message(request.POST['message_content'], Topic.objects.get(id=request.POST['topic_id']), request.user)
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
                    return helperviews.response(request,
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

    subscribed_ids = user.subscribed_topics.values_list('id', flat=True)
    
    if topic_list != []:
    # Get all subscribed topics from previously filtered topics
        topic_sublist = topic_list.filter(id__in=subscribed_ids)
    # Get all unsubscribed topics from previously filtered topics
        topic_nsublist = topic_list.exclude(id__in=subscribed_ids)
        topic_list = chain(topic_sublist, topic_nsublist)
    
    return render(request, 'tableview.html', {'topics': topic_list, 'subIDs': subscribed_ids, 'messages': message_list})

