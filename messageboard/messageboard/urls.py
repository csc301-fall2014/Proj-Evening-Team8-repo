from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainsite import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'messageboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^mainsite/', include('mainsite.urls', namespace="mainsite")),
    url(r'^mainsite/', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
