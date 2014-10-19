from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from mainsite.forms import UserForm


def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            return render(request, 'mainsite/registrationcomplete.html', {'data': data})
        else:
            return HttpResponse('Invalid Form Data.' + str(form.errors))
    else:
        form = UserForm(initial={'email': '@mail.utoronto.ca'})
    return render(request, 'mainsite/registration.html', {'form': UserForm()})