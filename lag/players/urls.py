from django.conf.urls.defaults import *

urlpatterns = patterns(
    'players.views',
    (r'pickpocket/$', 'pickpocket'),
    (r'profile/$', 'player_detail'),
)
