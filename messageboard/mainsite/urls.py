from django.conf.urls import url
from mainsite import views

urlpatterns = [
    url(r'^registration', views.registration, name='registration'),
]