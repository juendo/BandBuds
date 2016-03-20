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
    url(r'^gig/(?P<gig_id>[0-9]+)/buds/(?P<bud_slug>[\w\-]+)/$', views.gig_bud, name='gig_buds'),
    url(r'^bud_profile/(?P<budSlug>[\w\-]+)/$', views.bud_profile, name='bud_profile'),
    #url(r'^profile/(?P<user_name_slug>[\w\-]+)/like_band/$', views.like_band, name='like_band'),
    url(r'^profile/like_band/$', views.like_band, name='like_band'),
    url(r'^profile/dislike_band/$', views.dislike_band, name='dislike_band'),
    url(r'^profile/(?P<user_name_slug>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profile/', views.my_profile, name='my_profile'),

    # ajax requests
    url(r'^ajax/im_going/(?P<gig_id>[0-9]+)/$', views.im_going, name='im_going'),
    url(r'^ajax/load_gigs/(?P<date_param>[\w\-]+)/(?P<with_buds>[tf]{1})/$', views.gigs_on_date, name='gigs_on_date'),
    url(r'^ajax/reload_calendar/(?P<date_param>[0-9-]+)/(?P<with_buds>[tf]{1})/$', views.calendar_json, name='reload_calendar'),
    url(r'^ajax/nudge/(?P<user_slug>[\w\-]+)/(?P<gig_id>[0-9]+)$', views.nudge, name='nudge'),
)
