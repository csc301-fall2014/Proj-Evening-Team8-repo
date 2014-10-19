from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from mainsite.forms import UserForm


def registration(request):
    return render(request, 'mainsite/registration.html', {'form': UserForm()})


def register(request):
    new_user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    return render(request, 'mainsite/register.html', {'new_user': new_user})
