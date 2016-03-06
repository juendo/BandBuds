from django.conf.urls import patterns, url
from bba import views
#url patterns
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^calendar/(?P<month_string>[0-9]{4}-[0-9]{2})/$', views.calendar, name='calendar'),
    url(r'^user/(?P<user_name_slug>[\w\-]+)/$', views.user, name='user'),
    url(r'^user/register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user/(?P<buddy_slug>[\w\-]+)/$', views.index, name='user_buddy'),
    url(r'^user/(?P<attended_gig_slug>[\w\-]+)/$', views.index, name='user_gig'),
    url(r'^gig/(?P<gig_id>[0-9]+)/$', views.gig, name='gig'),
    url(r'^gig/(?P<gig_id>[0-9]+)/(?P<bud_slug>[\w\-]+)/$', views.gig_bud, name='gig_bud'),
)

print 'got here url is '