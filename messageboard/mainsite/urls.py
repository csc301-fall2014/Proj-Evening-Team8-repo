from django.conf.urls import url
from mainsite import views
from django.conf import settings

urlpatterns = [

    # Registration and login
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^activation/(?P<activation_key>\w+)/', views.email_activation, name='activation'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),

    # Topics and main page
    url(r'^messageboard/$', views.tableview, name='messageboard'),
    url(r'^messageboard/create/$', views.create_topic, name='create_topic'),
    url(r'^messageboard/(?P<topicid>[0-9]*)/$', views.topic, name='topic'),

    # Subscriptions
    url(r'^messageboard/(?P<topicid>[0-9]*)/subscribe/$', views.subscribe, name="subscribe"),
    url(r'^messageboard/subscriptions/$', views.subscribed_topics, name='subscribed_topics'),

    # Groups
    url(r'^messageboard/creategroup/$', views.create_group, name='create_group'),
    url(r'^messageboard/group/(?P<groupid>[0-9]*)/$', views.group, name='group'),
    url(r'^messageboard/joinedgroups/$', views.joined_groups, name='joined_groups'),
    url(r'^messageboard/joingroup/$', views.join_group, name='join_group'),
    url(r'^messageboard/group/(?P<groupid>[0-9]*)/inviteuser/$', views.groupinvite, name='groupinvite'),
    url(r'^messageboard/group/(?P<groupid>[0-9]*)/inviteuser/confirmation/(?P<userid>[0-9]*)/$', views.confirmation, name='confirmation'),
    url(r'^messageboard/viewinvites/(?P<userid>[0-9]*)/$', views.viewinvites, name='view_invites'),


    # User profiles
    url(r'^messageboard/userprofile/(?P<userid>[0-9]*)/$', views.userprofile, name='userprofile'),
    url(r'^messageboard/userprofile/(?P<userid>[0-9]*)/edit/$', views.edituserprofile, name='edituserprofile'),

    #static media
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

]
