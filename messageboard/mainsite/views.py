from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from mainsite.forms import UserForm, MessageForm, TopicForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login  # Changed name because login is our view function
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
import datetime, hashlib, random
from mainsite.models import Topic, Message, UserProfile


def registration(request):
    if request.method == 'POST':
        # Registration complete, data submitted via POST
        form = UserForm(request.POST)
        if form.is_valid():  # Cleans form data as well
            # Accept data and display confirmation
            data = form.cleaned_data
            new_user = User.objects.create_user(data['username'], data['email'], data['password'])
            new_user.first_name = data['first_name']
            new_user.last_name = data['last_name']
            new_user.is_active = False  # Not active until e-mail activation
            new_user.save()

            # Generate activation key and UserProfile
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            activation_key = hashlib.sha1((salt+new_user.email).encode('utf-8')).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)  # 48 hours

            new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            #Send activation key
            email_subject = 'Account Activation'
            email_body = "Dear %s,\nThank you for signing up. To complete your registration, click the link below.\n\n \
http://127.0.0.1:8000/mainsite/activation/%s\n\nYours,\nTeam8s" % (new_user.username, activation_key)

            send_mail(email_subject,
                      email_body,
                      'no-reply@messageboard.com',
                      [new_user.email],
                      fail_silently=False)

            return render(request, 'registration/registrationcomplete.html', {'data': data})
        else:
            # Display validation errors
            return HttpResponse('Invalid registration information.' + str(form.errors))
    else:
        # Registration not completed, initialize form
        return render(request, 'registration/registration.html', {'form': UserForm(initial={'email': '@mail.utoronto.ca'})})


def email_activation(request, activation_key):
    # Check for UserProfile that matches activation_key
    try:
        user_profile = UserProfile.objects.get(activation_key=activation_key)
    except UserProfile.DoesNotExist:
        return HttpResponse('Invalid activation link.')

    user = user_profile.user

    # Check if already activated
    if user.is_active:
        return HttpResponse('Account already activated.')

    # Check if activation_key has expired
    if user_profile.key_expires < timezone.now():
        user.delete()  # Delete User, dependant UserProfile automatically deleted as well
        return HttpResponse('Key has expired. Please register again.')

    user.is_active = True
    user.save()
    return HttpResponse('Account has been activated.')


def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            #login the user
            auth_login(request, user)
            #redirect
            return redirect('/mainsite/messageboard/')
        else:
            # Display validation errors
            return HttpResponse('User does not exist or password is incorrect.')
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
    return render(request, 'messageboard.html', {'topics': topic_list})


@login_required(login_url='/mainsite/login')
def create_topic(request):
    if request.method == 'POST':
        topic = Topic(topic_name=request.POST['topic_name'], creator=request.user)
        topic.save()
        return redirect('/mainsite/messageboard/')
    else:
        return render(request, 'topics/create_topic.html',
                        {'form': TopicForm})


@login_required(login_url='/mainsite/login')
def topic(request, topicid):
    if request.method == 'POST':
        filledForm = MessageForm(request.POST)
        if filledForm.is_valid():
            data = filledForm.cleaned_data
            message = Message()
            message.creator = request.user
            message.topic = Topic.objects.get(id=topicid)
            message.message_content = data['message_content']
            message.save()
    thisTopic = Topic.objects.get(id=topicid)
    messagelist = Message.objects.filter(topic__id=thisTopic.id)
    return render(request, 'topics/topic.html', {'messages': messagelist, 'topic': thisTopic, 'form': MessageForm()})


@login_required(login_url='/mainsite/login')
def subscribe(request, topicid):
    # Associate the topic and user to create a subscription
    user = request.user
    user.subscribed_topics.add(Topic.objects.get(id=topicid))
    # After subscribing, redirect to the user's subscription list.
    return redirect('/mainsite/messageboard/subscriptions')


@login_required(login_url='/mainsite/login')
def subscribed_topics(request):
    user = request.user
    topic_list = user.subscribed_topics.all()
    return render(request, 'topics/subscribed_topics.html', {'topics': topic_list})