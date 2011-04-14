import os
from datetime import date
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from lag.locations.models import Place, Visit
from lag.utils.shortcuts import render_to

@render_to('locations/place_detail.html')
def place_detail(request, id):
    """
    Show the detail for a particular place

    Arguments:
    - `id`:
    """
    place = get_object_or_404(Place, id=id)
    nearby = Place.objects.distance(place.point,
                                    field_name='point').order_by('distance')
    return dict(place=place, nearby=nearby[1:3])


@login_required
def checkin(request):
    """
    Check to see if place exists, if not, create it unnamed

    Then make checkin
    """
    if not request.is_ajax():
        return HttpResponse('No')
    player = request.user.get_profile()
    lat = request.POST['lat']
    lon = request.POST['lon']
    point = Point(x=float(lon), y=float(lat))

    places = Place.objects.distance(point).order_by('distance')[:5]
    try:
        guess = [places[0].pk, places[0].name]
    except IndexError:
        guess = False
    alternatives = []
    for place in places[1:]:
        alternatives.append([place.pk, place.name])
    return HttpResponse(json.dumps(dict(guess=guess,
                                        alternatives=alternatives)))

@login_required
def register_place(request):
    """
    We're going to be registering a new place from user energy
    """
    if not request.is_ajax():
        return HttpResponse('No')
    player = request.user.get_profile()
    name = request.POST['name']
    lat = request.POST['lat']
    lon = request.POST['lon']
    point = Point(x=float(lon), y=float(lat))
    place = Place(lat=lat, lon=lon, point=point, name=name, created_by=player)
    place.save()
    visit = Visit.objects.get_or_create(player=player, place=place)[0]
    visit.last_visited = date.today()
    visit.visits += 1
    visit.save()
    params = dict(
        name=name,
        created_by="You, just now!",
        player_visit_count=visit.visits
        )
    return HttpResponse(json.dumps(params))

    return HttpResponse()

@login_required
def confirm_visit(request):
    """
    The player has confirmed that they're visiting this place.

    Let's give them the relevant stats about it.
    """
    if not request.is_ajax():
        return HttpResponse('No')
    player = request.user.get_profile()
    place_id = request.POST['place_id']
    place = get_object_or_404(Place, pk=place_id)
    visit = Visit.objects.get_or_create(player=player, place=place)[0]
    visit.last_visited = date.today()
    visit.visits += 1
    visit.save()
    place_visits = place.visit_set.all().count()
    params = dict(
        name=place.name,
        created_by=place.created_by.__unicode__(),
        player_visit_count=visit.visits
        )
    return HttpResponse(json.dumps(params))

def logger(request):
    """
    Shall we just serialise everything to a file?
    """
    with open(os.path.join(settings.ROOT, 'post.log'), 'a') as logfile:
        logfile.write(json.dumps(request.POST)+"\n")
    return HttpResponse('Yes')
