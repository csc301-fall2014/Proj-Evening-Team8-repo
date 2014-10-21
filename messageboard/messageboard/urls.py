from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainsite import views

urlpatterns = patterns('',
	#check for login/registration urls
    url(r'^mainsite/', include('mainsite.urls', namespace="mainsite")),
    #check if it is landing page
    url(r'^mainsite/', views.index, name='index'),
    #check for admin
    url(r'^admin/', include(admin.site.urls)),
)
