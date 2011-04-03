import os
from datetime import date
import json
import pickle

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from lag.locations.models import Place, Checkin

@login_required
def checkin(request):
    """
    Check to see if place exists, if not, create it unnamed

    Then make checkin
    """
    if not request.is_ajax:
        return HttpResponse('No')
    player = request.user.get_profile()
    lat = request.POST['lat']
    lon = request.POST['lon']
    place = Place.objects.get_or_create(lat=lat, lon=lon)[0]
    checkin = Checkin.objects.get_or_create(player=player, place=place)[0]
    checkin.visits += 1
    checkin.last_visited = date.today()
    checkin.save()
    params = dict(place=place.name, creator=place.created_by,
                  visit_count=checkin.visits,
                  last_visited=checkin.last_visited.strftime("%Y-%m-%d"))
    return HttpResponse(json.dumps(params))

def logger(request):
    """
    Shall we just serialise everything to a file?
    """
    with open(os.path.join(settings.ROOT, 'post.log'), 'a') as logfile:
        logfile.write(json.dumps(request.POST)+"\n")
    return HttpResponse('Yes')
