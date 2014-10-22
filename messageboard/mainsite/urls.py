from django.conf.urls import url
from mainsite import views

urlpatterns = [
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^messageboard/$', views.messageboard, name='messageboard'),
    url(r'^messageboard/(?P<topicname>\w*)/$', views.topic, name='messageboard'),
]