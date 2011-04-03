from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^home/$', 'players.views.home'),
    (r'^edit-profile/$', 'players.views.edit_profile'),
    (r'^logger/$', 'locations.views.logger'),
    (r'^locations/', include('locations.urls')),
    (r'^$', 'lag.views.homepage'),
    (r'^accounts/', include('registration.urls')),
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                 serve,
                                 {'document_root': settings.MEDIA_ROOT}))
        del(_media_url, serve)
