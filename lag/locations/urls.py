from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^a/checkin/$', 'locations.views.checkin'),
)
