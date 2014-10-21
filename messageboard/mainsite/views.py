from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from mainsite.forms import UserForm
from django.contrib.auth import authenticate, login
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
            return render(request, 'mainsite/registrationcomplete.html', {'data': data})
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
            login(request, user)
            # Redirect to a success page
            return render(request, 'mainsite/', {'data': data})

    else:
        return render(request, 'mainsite/login/login.html', {'form': AuthenticationForm()})