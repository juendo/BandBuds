from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import * 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BandBuds.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('bba.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH}),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )