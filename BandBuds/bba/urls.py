from django.conf.urls import patterns, url
from bba import views
#url patterns
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^user/(?P<user_name_slug>[\w\-]+)/$', views.user, name='user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user/(?P<buddy_slug>[\w\-]+)/$', views.index, name='user_buddy'),
    url(r'^user/(?P<attended_gig_slug>[\w\-]+)/$', views.index, name='user_gig'),
    url(r'^gig/(?P<gig_id>[0-9]+)/$', views.gig, name='gig'),
    url(r'^load_gigs/(?P<query>[\w\-]+)/$', views.gigs_on_date, name='gigs_on_date'),
    url(r'^im_going/(?P<gig_id>[0-9]+)/$', views.im_going, name='im_going'),
    url(r'^bud_profile/(?P<budSlug>[\w\-]+)/$', views.bud_profile, name='bud_profile'),
    url(r'^profile/(?P<user_name_slug>[\w\-]+)/$', views.profile, name='profile'),
)
