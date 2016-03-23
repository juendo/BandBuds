from django.conf.urls import patterns, url
from bba import views
#url patterns
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/', views.my_profile, name='my_profile'),
    url(r'^edit-profile/', views.edit_profile, name='edit-profile'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^gig/(?P<gig_id>[0-9]+)/$', views.gig, name='gig'),
    url(r'^gig/(?P<gig_id>[0-9]+)/buds/(?P<bud_slug>[\w\-]+)/$', views.gig_bud, name='gig_buds'),
    url(r'^logout/$', views.user_logout, name='logout'),

    # ajax requests
    url(r'^ajax/nudge/$', views.nudge, name='nudge'),
    url(r'^ajax/im_going/(?P<gig_id>[0-9]+)/$', views.im_going, name='im_going'),
    url(r'^ajax/load_gigs/(?P<date_param>[\w\-]+)/(?P<with_buds>[tf]{1})/$', views.gigs_on_date, name='gigs_on_date'),
    url(r'^ajax/reload_calendar/(?P<date_param>[0-9-]+)/(?P<with_buds>[tf]{1})/$', views.calendar_json, name='reload_calendar'),
    url(r'^ajax/like_band/$', views.like_band, name='like_band'),
    url(r'^ajax/dislike_band/$', views.dislike_band, name='dislike_band'),
    url(r'^ajax/accept/$', views.accept, name='accept'),
    url(r'^ajax/decline/$', views.decline, name='decline'),
)
