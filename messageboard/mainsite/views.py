import hashlib
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from mainsite.forms import UserForm, TopicForm, GroupForm, UserProfileForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login  # Changed name because login is our view function
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from mainsite.models import Topic, Message, UserProfile, Group, Tag, Requests
from datetime import datetime, timedelta


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
    return render(request, 'tableview.html', {'topics': topic_list, 'messages': message_list})


# Not a view, helper function for notices (a richer and more customizable HttpResponse)
def response(request, title, message, link, button):
    return render(request, 'response.html', {
        'title': title,
        'message': message,
        'link': link,
        'button': button})


def registration(request):
    if request.method == 'POST':
        # Registration complete, data submitted via POST
        form = UserForm(request.POST)
        if form.is_valid():  # Calling is_valid on ModelForms calls full_clean
            # Create an inactive User but don't save to database yet
            data = form.cleaned_data
            new_user = User(username=data['username'],
                            email=data['email'],
                            password=make_password(data['password']),
                            first_name=data['first_name'],
                            last_name=data['last_name'],
                            is_active=False)

            # Generate activation key, check for duplicates however astronomically unlikely it would be
            activation_key = None
            while activation_key is None or UserProfile.objects.filter(activation_key=activation_key).exists():
                salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
                activation_key = hashlib.sha1((salt+new_user.email).encode('utf-8')).hexdigest()
            key_expires = timezone.now() + timezone.timedelta(2)  # 48 hours

            # Send activation key
            send_activation_email(new_user, activation_key)

            # E-mail sent, safe to save to database
            new_user.save()

            # Create UserProfile
            new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            return render(request, 'registration/registrationcomplete.html', {'data': data})
        else:
            # Display validation errors
            return response(request,
                            'Invalid Registration Information',
                            str(form.errors),
                            '/mainsite/registration/',
                            'Back')
    else:
        # Registration not completed, initialize form
        return render(request, 'registration/registration.html',
                      {'form': UserForm(initial={'email': '@mail.utoronto.ca'})})


# Not a view, helper function
def send_activation_email(new_user, activation_key):
    email_subject = 'Account Activation'
    email_body = "Dear %s,\n\nThank you for signing up. To complete your registration, access to the link below.\n\n\
http://127.0.0.1:8000/mainsite/activation/%s\n\nYours,\nTeam8s" % (new_user.username, activation_key)
    send_mail(email_subject,
              email_body,
              'no-reply@messageboard.ca',
              [new_user.email],
              fail_silently=False)


def email_activation(request, activation_key):
    # Check if there is a UserProfile that matches activation_key
    try:
        user_profile = UserProfile.objects.get(activation_key=activation_key)
    except UserProfile.DoesNotExist:
        return response(request,
                        'Invalid Activation Link',
                        'The activation link you have provided does not correspond to any account.\n' +
                        'Double check you have the correct link.',
                        '/mainsite/',
                        'Back')

    user = user_profile.user

    # If already activated, do nothing
    if user.is_active:
        return response(request,
                        'Account already activated',
                        'The account is already activated.\n',
                        '/mainsite/',
                        'Back')

    # Check if activation_key has expired
    if user_profile.key_expires < timezone.now():
        user.delete()  # Delete User, dependant UserProfile automatically deleted as well
        return response(request,
                        'Expired Activation Link',
                        'The activation link has expired. Please register again.',
                        '/mainsite/registration/',
                        'Register')

    user.is_active = True
    user.save()
    return response(request,
                    'Account Activated',
                    'Your account has been activated. You may now login.',
                    '/mainsite/login/',
                    'Login')


def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/mainsite/messageboard/')
            else:
                if user.user_profile.key_expires < timezone.now():
                    user.delete()  # Delete User, dependant UserProfile automatically deleted as well
                    return response(request,
                                    'Expired Unactivated Account',
                                    'Account was not activated in time and has been deleted. Please register again.',
                                    '/mainsite/registration/',
                                    'Register')
                else:
                    # Resend activation key
                    send_activation_email(user, user.user_profile.activation_key)
                    return response(request,
                                    'Account Unactivated',
                                    'Account not activated. Another activation e-mail has been sent.',
                                    '/mainsite/login/',
                                    'Back')
        else:
            # Incorrect user or password
            return response(request,
                            'Incorrect Login',
                            'User does not exist or password is incorrect.',
                            '/mainsite/login/',
                            'Back')
    else:
        return render(request, 'registration/login.html', {'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'index.html', {'form': AuthenticationForm()})


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


@login_required(login_url='/mainsite/login')
def create_group(request):
    if request.method == 'POST':
        user = request.user
        try:
            existing_group = Group.objects.get(group_name=request.POST['group_name'])
            group = Group(group_name=request.POST['group_name'],
                          group_password=request.POST['group_password'], creator=request.user)
            group.save()
            group.user_set.add(user)
            user.joined_groups.add(group)
        except Group.DoesNotExist:
            return redirect(reverse('mainsite:messageboard'))    
        return redirect(reverse('mainsite:messageboard'))
    else:
        return render(request, 'groups/create_group.html', {'form': GroupForm})


@login_required(login_url='/mainsite/login')
def group(request, groupid):
    this_group = Group.objects.get(id=groupid)
    if request.method == 'POST':
        if "INVITE" in request.POST:
            return redirect('inviteuser/')
        if "REMOVE" in request.POST:
            this_group.delete()
            return redirect(reverse('mainsite:messageboard'))
        elif "ADDMOD" in request.POST:
            mod_name = request.POST['mod_name']
            try:
                if mod_name != this_group.creator.username:
                    mod_user = this_group.user_set.get(username=mod_name)
                    this_group.mod_set.add(mod_user)
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('mainsite:group', args=(groupid,)))                    
            return HttpResponseRedirect(reverse('mainsite:group', args=(groupid,)))
    else:
        group_creator = this_group.creator
        user_list = this_group.user_set.all()
        mod_list = this_group.mod_set.all()
        topic_list = this_group.viewable_topics.all()
        return render(request, 'groups/group.html', {'group': this_group,
                                                     'creator': group_creator,
                                                     'mods': mod_list,
                                                     'users': user_list,
                                                     'topics': topic_list})

@login_required(login_url='/mainsite/login')
def joined_groups(request):
    user = request.user
    group_list = user.joined_groups.all()
    return render(request, 'groups/joined_groups.html', {'groups': group_list})


@login_required(login_url='/mainsite/login')
def join_group(request):
    all_groups = Group.objects.all()
    if request.method == 'POST':
        # Get the user and group object
        user = request.user
        try:
            this_group = Group.objects.get(group_name=request.POST['group_name'])
        except Group.DoesNotExist:
            return response(request,
                            'Nonexistent Group',
                            'Group does not exist.',
                            '/mainsite/messageboard/joingroup/',
                            'Back')
        # Add the user to the group if the password is correct
        if this_group.group_password == request.POST['group_password']:
            this_group.user_set.add(user)
            user.joined_groups.add(this_group)
        else:
            return response(request,
                            'Incorrect Password',
                            'Password is incorrect.',
                            '/mainsite/messageboard/joingroup/',
                            'Back')
        return redirect(reverse('mainsite:messageboard'))
    else:
        return render(request, 'groups/join_group.html', {'form': GroupForm, 'groups': all_groups})


@login_required(login_url='/mainsite/login')
def userprofile(request, userid):
    user = User.objects.get(id=userid)
    return render(request, 'userprofile/userprofile.html', {'user': user})


@login_required(login_url='/mainsite/login')
def edituserprofile(request, userid):
    args = {}
    user = User.objects.get(id=userid)
    userprofile = user.user_profile
    img = None
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            #get data from form
            data = form.cleaned_data

            userprofile.user_description = data['user_description']
            userprofile.school = data['school']
            userprofile.save()
            return render(request, 'userprofile/userprofile.html', {'user': user})
    else:
        form = UserProfileForm(instance=user,
         initial={'user_description': user.user_profile.user_description, 'school': user.user_profile.school})

    args['form'] = form
    return render(request, "userprofile/edituserprofile.html", args)

#invite users to a specific group
@login_required(login_url='/mainsite/login')
def groupinvite(request, groupid):
    this_group = Group.objects.get(id=groupid)
    group_creator = this_group.creator
    user_list = User.objects.all()
    

    return render(request, 'groups/groupinvite.html', {'group': this_group,
                                                 'creator': group_creator,
                                                 'users': user_list})
#confirm invite
@login_required(login_url='/mainsite/login')
def confirmation(request, groupid, userid):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_to_invite = User.objects.get(id=userid)
    user_to_invite_profile = UserProfile.objects.get(user=user_to_invite)

    this_group = Group.objects.get(id=groupid)
    new_request = Requests(user_profile=user_to_invite_profile,
                                  group=this_group,
                                  user_that_invited=user_profile)
    new_request.save()

    return render(request, 'groups/groupinviteconfirmation.html', {'user': user_to_invite})


#view invites
@login_required(login_url='/mainsite/login')
def viewinvites(request, userid):
    user = request.user
    requests  = Requests.objects.all()
    if request.method == "POST":
        if "accept" in request.POST:
            this_request = request.POST['accept_request']
            this_request = Requests.objects.get(id=this_request)
            this_request.group.user_set.add(user)
            this_request.delete()
            #return render(request, 'groups/groupacceptconfirmation.html',
            # {'group': this_request.group})

    return render(request, 'groups/viewgroupinvites.html', {'user': user, 'requests': requests})

#view dm's
@login_required(login_url='/mainsite/login')
def viewdirectmessages(request, userid):
    user = request.user
    direct_messages_user = user.user_profile.direct_messages.all()
    return render(request, 'topics/direct_message.html', {'user': user, 'directmessages': direct_messages_user})

#create new dm or view existing
@login_required(login_url='/mainsite/login')
def createmessage(request, userid):
    user = request.user
    all_users = User.objects.all()
    if request.method == "POST":
        if "new" in request.POST:
            #create new dm
            new_dm = Topic(topic_name=request.POST['recipient'],
                creator=user,
                subscriptions=user,
                is_direct_message=True)
            new_dm.save
            #save dm to user profile set of dm's
            user.user_profile.direct_messages.add(new_dm)
            user.save
            return redirect(reverse('mainsite:messageboard/directmessages'))    

    return render(request, 'topics/new_direct_message.html', {'user': user, 'all_users': all_users})

