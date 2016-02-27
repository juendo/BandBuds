from django.conf.urls import patterns, url
from bba import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_name_slug>[\w\-]+)/$', views.user, name='user'),
    url(r'^user/(?P<buddy_slug>[\w\-]+)/$', views.index, name='user_buddy'),
    url(r'^user/(?P<attended_gig_slug>[\w\-]+)/$', views.index, name='user_gig'),
)