from django.conf.urls import url
from mainsite import views

urlpatterns = [
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^activation/(?P<activation_key>\w+)/', views.email_activation, name='activation'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^messageboard/$', views.messageboard, name='messageboard'),
    url(r'^messageboard/create/$', views.create_topic, name='create_topic'),
    url(r'^messageboard/(?P<topicid>[0-9]*)/$', views.topic, name='topic'),

 

    url(r'^messageboard/(?P<topicid>[0-9]*)/subscribe/$', views.subscribe, name="subscribe"),
    url(r'^messageboard/subscriptions/$', views.subscribed_topics, name='subscribed_topics'),
    url(r'^messageboard/creategroup/$', views.create_group, name='create_group'),
    url(r'^messageboard/group/(?P<groupid>[0-9]*)/$', views.group, name='group'),
    url(r'^messageboard/joinedgroups/$', views.joined_groups, name='joined_groups'),
    url(r'^messageboard/myview/$', views.myview, name='myview'),
   
]
