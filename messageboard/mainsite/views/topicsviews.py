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
            print(topic.group_set.all())
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
    messagelist = Message.objects.filter(topic__id=this_topic.id)
    return render(request, 'topics/topic.html', {
        'messages': messagelist,
        'topic': this_topic,
        'tags': this_topic.tags.all,
        'tag_error': tag_error})

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
