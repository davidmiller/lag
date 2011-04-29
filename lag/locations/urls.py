from django.conf.urls.defaults import *

urlpatterns = patterns(
    'locations.views',
    (r'placetypes/', 'place_types'),
    (r'checkin/$', 'checkin'),
    (r'register-place/$', 'register_place'),
    (r'visit/$', 'visit'),
    (r'acquire-item', 'acquire_item'),
    (r'wall/$', 'wall'),
)
