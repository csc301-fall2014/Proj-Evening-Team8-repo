import hashlib
import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mainsite.forms import UserForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login  # Changed name because login is our view function
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from mainsite.models import UserProfile
from mainsite.views import helperviews

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

            #extra form data
            isStudent = False
            isTeacher = False
            if data['role'][0] == 'student':
                isStudent = True
            else:
                isTeacher = True

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
            if isStudent == True:
                new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      key_expires=key_expires,
                                      student=True)
            else:
                new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      key_expires=key_expires,
                                      teacher=True)
            new_profile.save()

            return render(request, 'registration/registrationcomplete.html', {'data': data})
        else:
            # Display validation errors
            return helperviews.response(request,
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
        return helperviews.response(request,
                        'Invalid Activation Link',
                        'The activation link you have provided does not correspond to any account.\n' +
                        'Double check you have the correct link.',
                        '/mainsite/',
                        'Back')

    user = user_profile.user

    # If already activated, do nothing
    if user.is_active:
        return helperviews.response(request,
                        'Account already activated',
                        'The account is already activated.\n',
                        '/mainsite/',
                        'Back')

    # Check if activation_key has expired
    if user_profile.key_expires < timezone.now():
        user.delete()  # Delete User, dependant UserProfile automatically deleted as well
        return helperviews.response(request,
                        'Expired Activation Link',
                        'The activation link has expired. Please register again.',
                        '/mainsite/registration/',
                        'Register')

    user.is_active = True
    user.save()
    return helperviews.response(request,
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
                    return helperviews.response(request,
                                    'Expired Unactivated Account',
                                    'Account was not activated in time and has been deleted. Please register again.',
                                    '/mainsite/registration/',
                                    'Register')
                else:
                    # Resend activation key
                    send_activation_email(user, user.user_profile.activation_key)
                    return helperviews.response(request,
                                    'Account Unactivated',
                                    'Account not activated. Another activation e-mail has been sent.',
                                    '/mainsite/login/',
                                    'Back')
        else:
            # Incorrect user or password
            return helperviews.response(request,
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
