from django.conf.urls.defaults import *

urlpatterns = patterns(
    'locations.views',
    (r'place/(?P<id>\d+)/', 'place_detail'),
    (r'checkin/$', 'checkin'),
    (r'register-place/$', 'register_place'),
    (r'confirm-visit/$', 'confirm_visit'),
)
