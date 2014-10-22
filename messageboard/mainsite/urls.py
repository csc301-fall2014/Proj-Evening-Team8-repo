from django.conf.urls import url
from mainsite import views

urlpatterns = [
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^messageboard/$', views.messageboard, name='messageboard'),
    url(r'^messageboard/create/$', views.create_topic, name='create_topic'),
    url(r'^messageboard/(?P<topicid>[0-9]*)/$', views.topic, name='topic'),
    url(r'^messageboard/(?P<topicid>[0-9]*)/subscribe/$', views.subscribe, name="subscribe"),
    url(r'^messageboard/subscriptions/$', views.subscribed_topics, name='subscribed_topics'),

]