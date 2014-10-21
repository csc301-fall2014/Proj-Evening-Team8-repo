from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from mainsite.forms import UserForm
from django.contrib.auth import authenticate, logout
#imported login and changed the name because login is also our view function
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def registration(request):
    if request.method == 'POST':
        # Registration complete, data submitted via POST
        form = UserForm(request.POST)
        if form.is_valid():
            # Accept data and display confirmation
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            return render(request, 'mainsite/registration/registrationcomplete.html', {'data': data})
        else:
            # Display validation errors
            return HttpResponse('Invalid Form Data.' + str(form.errors))
    else:
        # Registration not completed, initialize form
        return render(request, 'mainsite/registration/registration.html', {'form': UserForm(initial={'email': '@mail.utoronto.ca'})})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #login the user
            auth_login(request, user)
            #redirect
            return render(request, 'mainsite/messageboard.html')
        else:
            # Display validation errors
            return HttpResponse('Invalid Form Data.')
    else:
        return render(request, 'mainsite/registration/login.html', {'form': AuthenticationForm()})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'mainsite/index.html', {'form': AuthenticationForm()})


def index(request):
    return render(request, 'mainsite/index.html')

def messageboard(request):
    #if our user is not a real user
    if not request.user.is_authenticated():
        return HttpResponse('Invalid Form Data.' + str(form.errors))
    else:
        return render(request, 'mainsite/messageboard.html')
    