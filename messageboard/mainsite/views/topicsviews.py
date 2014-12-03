from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from mainsite.forms import TopicForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from mainsite.models import Topic, Message, Tag
from mainsite.views import helperviews

@login_required(login_url='/mainsite/login')
def create_topic(request):
    form = TopicForm(request.user)
    if request.method == 'POST':
        topic = Topic(topic_name=request.POST['topic_name'], creator=request.user)
        topic.save()
        if "group_set" in request.POST:
            for group in request.POST.getlist('group_set'):
                topic.group_set.add(group)
            topic.save()
        return redirect('/mainsite/messageboard/')
    else:
        return render(request, 'topics/create_topic.html',
                        {'form': form})


@login_required(login_url='/mainsite/login')
def topic(request, topicid):
    this_topic = Topic.objects.get(id=topicid)
    subscribed_ids = request.user.subscribed_topics.values_list('id', flat=True)
    tag_error = ""
    if request.method == 'POST':

        # Post a message to the topic.
        if "POST" in request.POST:
            helperviews.post_message(request.POST['message_content'], Topic.objects.get(id=topicid), request.user)
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
            return HttpResponseRedirect(reverse('mainsite:topic', args=(topicid,)))

    messagelist = Message.objects.filter(topic__id=this_topic.id)
    return render(request, 'topics/topic.html', {
        'messages': messagelist,
        'topic': this_topic,
        'tags': this_topic.tags.all,
        'tag_error': tag_error,
        'subIDs': subscribed_ids})


@login_required(login_url='/mainsite/login')
def subscribed_topics(request):
    user = request.user
    topic_list = user.subscribed_topics.all()
    if "POST" in request.POST:
            message = Message()
            message.creator = user
            current_topic = Topic.objects.get(id=request.POST['topic'])
            message.topic = current_topic
            message.message_content = request.POST['message_content']
            message.save()
            return HttpResponseRedirect(reverse('mainsite:subscribed_topics'))
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
        return HttpResponseRedirect(reverse('mainsite:subscribed_topics'))
    elif "POST_filter" in request.POST:
        tag_name = request.POST['tag_name']
        # If tag field is not empty, filter by tag if it exists.
        if tag_name:
            try:
                tag = Tag.objects.get(tag_name=tag_name)
                topic_list = tag.tagged_topics.all()
            except Tag.DoesNotExist:
                topic_list = []

    message_list = Message.objects.filter(topic__in=topic_list)
    return render(request, 'topics/subscribed_topics.html', {'topics': topic_list,
                                                             'messages':message_list})
