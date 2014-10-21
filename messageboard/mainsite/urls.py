from django.conf.urls import url
from mainsite import views

urlpatterns = [
    url(r'^registration', views.registration, name='registration'),
    url(r'^login', views.login, name='login'),
    url(r'^messageboard', views.messageboard, name='messageboard'),
]