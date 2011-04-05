from django.conf.urls.defaults import *

urlpatterns = patterns(
    'locations.views',
    (r'checkin/$', 'checkin'),
    (r'register-place/$', 'register_place'),
    (r'confirm-visit/$', 'confirm_visit'),
)
